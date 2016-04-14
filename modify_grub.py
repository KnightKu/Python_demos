import re, logging, traceback

file_name="/tmp/grub.conf"
domain_name="atest-vmXXX"
copy_out="virt-copy-out -d %s /boot/grub/grub.conf %s" % (domain_name, "/tmp")
copy_in="virt-copy-in -d %s %s /boot/grub/" % (domain_name, file_name)

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
            old_boot_index = int(re.search('(default)=(\S+)', line.strip()).group(2))
            continue
        if line.strip().startswith("kernel "):
            image_index += 1
            kernel_options = line.split()
            kernel_img = kernel_options[1]
            if re.search("lustre", kernel_img):
                lustre_img_index = image_index
    print "default_line_index:%d, image_index:%d, old_boot_index:%d" % (default_line_index, image_index, old_boot_index)
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
            #print lines
            fd.writelines(lines)
            fd.close()
            # copy into vm, and test
            break
except Exception, e:
    print "Failed, error [%s]\n" % e
    print traceback.format_exc()


