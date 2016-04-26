from autotest.server import utils, autotest_remote, hosts, subcommand, test
from autotest.client.shared import error
import re, logging, traceback, time, sys, uuid

try:
    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import SubElement
except ImportError:
    try:
        import elementtree.ElementTree as ET
        from elementtree.ElementTree import SubElement
    except ImportError:
        print "failed=True msg='ElementTree python module unavailable'"

try:
    import libvirt
except ImportError:
    print "failed=True msg='libvirt python module unavailable'"
    sys.exit(1)


class repair_nodes(test.test):
    """
    soft : just restart the vm
    hard : change the boot kernel image
    force: use extern kernel image&initrd to start the vm, and install the
           latest kernel to repair the vm
    """
    version = 1
    vm_host = None
    vm_nodes_list = []
    force_repair = False
    ext_kernel = ""
    ext_initrd = ""
    ext_cmdline_dict = dict()
    grub = "grub"

    def initialize(self, vm_nodes, vm_host,
                   force_repair=False,
                   kernel="",
                   initrd="",
                   cmdline="",
                   grub="grub"):
        logging.info("Repair nodes initializing...")
        self.grub = grub
        if len(vm_host):
            try:
                self.vm_host = hosts.create_host(vm_host)
            except Exception, e:
                raise error.TestError("failed to create host :" + str(e))
            if not self.vm_host.is_up():
                raise error.TestError("Host is not up")

        logging.info("start creating vm nodes...")
        for node in vm_nodes:
            try:
                vm_node = hosts.create_host(node)
            except Exception, e:
                logging.warning("Failed to create.\n" + str(e))
            self.vm_nodes_list.append(vm_node)
            self.ext_cmdline_dict[vm_node.hostname] = cmdline

        self.force_repair = force_repair
        if self.force_repair:
            if (not len(kernel)) or (not len(initrd)):
                # no kernel img or initrd, clear force repair
                self.force_repair = False
            else:
                img_exists = self.validate_files_on_host(self.vm_host, kernel, initrd)
                if img_exists:
                    self.ext_kernel = kernel
                    self.ext_initrd = initrd
                else:
                    self.force_repair = False

    def qemu_start_conn(self):
        try:
            if self.vm_host is None:
                conn = libvirt.open("qemu:///system")
            else:
                conn = libvirt.open("qemu+ssh://root@%s/system" % self.vm_host.hostname)
        except Exception, e:
            logging.error("Failed to start con:\n %s \n %s" %
                          (str(e), traceback.format_exc()))
            raise error.TestError("Failed to connnect to qemu...")
        return conn

    def repair_prepare(self):
        try:
            if self.vm_host is None:
                ret = utils.run('type virt-copy-in', ignore_status=True)
                if ret.exit_status is not 0:
                    utils.run('yum install libguestfs-tools-c -y')
            else:
                ret = self.vm_host.run('type virt-copy-in', ignore_status=True)
                if ret.exit_status is not 0:
                    self.vm_host.run('yum install libguestfs-tools-c -y')
        except Exception, e:
            logging.error("Failed to prepare:\n %s \n %s" %
                          (str(e), traceback.format_exc()))

    def soft_repair_vm(self, vm_domain):
        """
        vm's hostname should be the same as the domain name
        soft means restart/reset the vm domain
        """
        domain_name = vm_domain.hostname
        conn = self.qemu_start_conn()
        domain = conn.lookupByName(domain_name)

        if domain.isActive():
            if domain.reboot():
                time.sleep(60)
                if vm_domain.is_up():
                    conn.close()
                    return True
            else:
                domain.destroy()
        if domain.create():
            time.sleep(60)
            if vm_domain.is_up():
                conn.close()
                return True
        conn.close()
        return False

    def vm_start_and_check(self, vm_domain):
        domain_name = vm_domain.hostname
        conn = self.qemu_start_conn()
        domain = conn.lookupByName(domain_name)
        try:
            new_vm = domain.create()
        except Exception, e:
            logging.error("Failed to start domain [%s]:\n %s \n %s" %
                          (domain_name, str(e), traceback.format_exc()))
            conn.close()
            return False
        if new_vm:
            time.sleep(60)
            if vm_domain.is_up():
                conn.close()
                return True
        else:
            conn.close()
            return False

    def hard_repair_vm(self, vm_node):
        file_name = "/tmp/grub.conf"
        domain_name = vm_node.hostname
        cmd_copy_out = "virt-copy-out -d %s /boot/grub/grub.conf %s" % (domain_name, "/tmp")
        cmd_copy_in = "virt-copy-in -d %s %s /boot/grub/" % (domain_name, file_name)
        conn = self.qemu_start_conn()
        domain = conn.lookupByName(domain_name)
        if domain.isActive():
            domain.destroy()
        conn.close()
        try:
            if self.vm_host is None:
                utils.run(cmd_copy_out)
            else:
                self.vm_host.run(cmd_copy_out)
                self.vm_host.get_file(file_name, file_name)
        except Exception, e:
            logging.error("Failed to copy out grub.cfg of domain [%s].\n %s \n %s" %
                          (domain_name, str(e), traceback.format_exc()))
        try:
            fd = open(file_name, "r")
            image_index = -1
            lustre_img_index = -1
            old_boot_index = -1
            lines = fd.readlines()
            print lines
            default_line_index = -1
            for i in range(len(lines)):
                line = lines[i]
                if line.strip().startswith("default="):
                    default_line_index = i
                    old_boot_index = int(re.search('(default)=(\S+)',
                                                   line.strip()).group(2))
                    continue
                if line.strip().startswith("kernel "):
                    if not len(self.ext_cmdline_dict[domain_name]):
                        cmd_line = line.strip().split(' ', 2)[2]
                        self.ext_cmdline_dict[domain_name] = cmd_line
                    image_index += 1
                    kernel_options = line.split()
                    kernel_img = kernel_options[1]
                    if re.search("lustre", kernel_img):
                        lustre_img_index = image_index
            print "default_line_index:%d, image_index:%d, old_boot_index:%d" % \
                  (default_line_index, image_index, old_boot_index)
            if (default_line_index < 0) or (image_index < 0) or (old_boot_index < 0):
                logging.error("Invalid grub.conf!\n")
                fd.close()
                exit(-1)
            if image_index == 0 and lustre_img_index == 0:
                logging.error("No other valid kernel image!\n")
                fd.close()
                exit(0)

            for index in range(image_index + 1):
                if index not in [lustre_img_index, old_boot_index]:
                    fd = open(file_name, "w")
                    lines[default_line_index] = "default=%d\n" % index
                    # print lines
                    fd.writelines(lines)
                    fd.close()
                    try:
                        if self.vm_host is None:
                            utils.run(cmd_copy_in)
                        else:
                            self.vm_host.send_file(file_name, file_name)
                            self.vm_host.run(cmd_copy_in)
                    except Exception, e:
                        logging.error("Failed to copy in grub.cfg to domain [%s].\n %s \n %s" %
                                      (domain_name, str(e), traceback.format_exc()))
                    if self.vm_start_and_check(vm_node):
                        break
        except Exception, e:
            print "Failed, error [%s]\n" % e
            print traceback.format_exc()

    def force_repair_vm(self, vm_node):
        """
        fork a transient and run install kernel in it to repair the target vm
        :param vm_node:
        :return:
        """
        domain_name = vm_node.hostname
        vm_uuid = str(uuid.uuid1())

        try:
            conn = self.qemu_start_conn()
            domain = conn.lookupByName(domain_name)
            if not domain.isActive():
                domain.create()

            doc = ET.fromstring(domain.XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE))
            domain.destroy()
            #doc = ET.fromstring(domain.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE))
            #print doc

            #conn.close()
            #return True
        except Exception, e:
            logging.error("Failed to launch xml of domain[%s] on host[%s].\n%s" %
                          (vm_node.hostname,
                           self.vm_host.hostname if self.vm_host else "",
                           str(e)))
            return False
        try:
            ### OS Boot info
            name_el = doc.find('name')
            name_el.text = name_el.text + "_repair"
            uuid_el = doc.find('uuid')
            uuid_el.text = vm_uuid
            os = doc.find('os')
            kernel_el = os.find('kernel')
            initrd_el = os.find('initrd')
            cmdline_el = os.find('cmdline')
        except Exception, e:
            logging.error("Failed to find section from xml.\n%s\n%s" %
                          (str(e), traceback.format_exc()))
            return False

        if kernel_el is not None:
            if kernel_el.text != self.ext_kernel:
                kernel_el.text = self.ext_kernel
        else:
            kernel_el = SubElement(os, 'kernel')
            kernel_el.text = self.ext_kernel

        if initrd_el is not None:
            if initrd_el.text != self.ext_initrd:
                initrd_el.text = self.ext_initrd
        else:
            initrd_el = SubElement(os, 'initrd')
            initrd_el.text = self.ext_initrd

        if cmdline_el is not None:
            if cmdline_el.text != self.ext_cmdline_dict[domain_name]:
                cmdline_el.text = self.ext_cmdline_dict[domain_name]
        else:
            cmdline_el = SubElement(os, 'cmdline')
            cmdline_el.text = self.ext_cmdline_dict[domain_name]

        logging.info("#####\nkernel:%s\ninitrd:%s\ncmdline:%s\n%s####" %
                     (self.ext_kernel, self.ext_initrd,
                      self.ext_cmdline_dict[domain_name], ET.tostring(doc)))
        # conn.defineXML()
        # start a transient vm
        try:
            domain_t = conn.createXML(ET.tostring(doc), 0)
        except Exception, e:
            logging.error("Failed to create vm form xml:\n[%s]\n%s\n%s" % (doc, str(e), traceback.format_exc()))
            conn.close()
            return False

        time.sleep(60)
        if vm_node.is_up():
            try:
                vm_node.run('yum reinstall kernel -y')
            except Exception, err:
                logging.error("Failed to install kernel in transient vm[%s]\n%s\n%s" %
                      (name_el.text, str(err), traceback.format_exc()))
                domain_t.destroy()
                conn.close()
                return False

            domain_t.destroy()
            # TODO :need change grub boot id after install kernel?
            # start the original vm
            try:
                domain.create()
            except Exception, e:
                logging.error("Failed to start vm after repair xml:\n[%s]\n%s" %
                              (str(e), traceback.format_exc()))
                conn.close()
                return False
            time.sleep(120)
            return vm_node.is_up()
        else:
            #domain_t.destroy()
            conn.close()
            return False

    def validate_files_on_host(self, host, *files):
        if host:
            if not host.is_up():
                logging.warning("Host %s is not up!\n" % host.hostname)
                return False
            for f in files:
                result = host.run('test -f %s' % f, ignore_status=True)
                if result.exit_status is not 0:
                    logging.error("Not found file:%s on host[%s]." %
                                  (f, host.hostname))
                    return False
            return True
        else:
            for f in files:
                result = utils.run('test -f %s' % f, ignore_status=True)
                if result.exit_status is not 0:
                    logging.error("Not found file:%s on host[%s]." %
                                  (f, host.hostname))
                    return False
        return True

    def run_once(self):
        logging.info("starting repair")
        need_hard_repair = []
        need_force_repair = []

        try:
            self.repair_prepare()
        except Exception, err:
            logging.error("failed to prepare: %s, %s" %
                          (str(err), traceback.format_exc()))
            raise error.JobError("failed to prepare")

        for vm_node in self.vm_nodes_list:
            try:
                if not self.soft_repair_vm(vm_node):
                    need_hard_repair.append(vm_node)
            except Exception, err:
                logging.error("failed to soft repair domain[%s]: %s, %s" %
                              (vm_node.hostname, str(err), traceback.format_exc()))
                raise error.JobError("failed to soft repair domain[%s]" % vm_node.hostname)

        if not len(need_hard_repair):
            return True

        for vm_node in need_hard_repair:
            try:
                if not self.hard_repair_vm(vm_node):
                    need_force_repair.append(vm_node)
            except Exception, err:
                logging.error("failed to hard repair domain[%s]: %s, %s" %
                              (vm_node.hostname, str(err), traceback.format_exc()))
                raise error.JobError("failed to hard repair domain[%s]" % vm_node.hostname)

        if not len(need_force_repair):
            return True

        if self.force_repair:
            for vm_node in need_force_repair:
                print "#####%s" % self.ext_cmdline_dict
                if not len(self.ext_cmdline_dict[vm_node.hostname]):
                    logging.warning("Skip force repair vm[%s], no cmdline provided.\n" % vm_node.hostname)
                    continue
                try:
                    if not self.force_repair_vm(vm_node):
                        logging.warning("failed to force repair domain[%s]" % vm_node.hostname)
                except Exception, err:
                    logging.error("failed to force repair domain[%s]: %s, %s" %
                                  (vm_node.hostname, str(err), traceback.format_exc()))
                    raise error.JobError("failed to force repair domain[%s]" % vm_node.hostname)
        logging.info("End repair")
