import re, logging, traceback, time, sys

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


def force_repair_vm(kernel, initrd, cmdline):

    try:
        conn = libvirt.open("qemu:///system")
        domain = conn.lookupByName("ltest1")

        doc = ET.fromstring(domain.XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE))
    except Exception, e:
        logging.error("Failed to launch xml of domain[%s] on host[%s].\n%s" %
                      ("aaa", "bbb", str(e)))
        return False
    try:
        ### OS Boot info
        os = doc.find('os')
        kernel_el = os.find('kernel')
        initrd_el = os.find('initrd')
        cmdline_el = os.find('cmdline')
    except Exception, e:
        logging.error("Failed to find section from xml.\n%s\n%s" %
                      (str(e), traceback.format_exc()))
        return False
    print "orxml:\n" + ET.tostring(doc)

    if kernel_el is not None:
        if kernel_el.text != kernel:
            kernel_el.text = kernel
    else:
        kernel_el = SubElement(os, 'kernel')
        kernel_el.text = kernel

    if initrd_el is not None:
        if initrd_el.text != initrd:
            initrd_el.text = initrd
    else:
        initrd_el = SubElement(os, 'initrd')
        initrd_el.text = initrd

    if cmdline_el is not None:
        if cmdline_el.text != cmdline:
            cmdline_el.text = cmdline
    else:
        cmdline_el = SubElement(os, 'cmdline')
        cmdline_el.text = cmdline

    print ET.tostring(os)

    print "finxml:\n" + ET.tostring(doc)

if __name__ == "__main__":
    force_repair_vm("AA", "BB", "CC")