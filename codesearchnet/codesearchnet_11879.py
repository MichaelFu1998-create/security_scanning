def init_raspbian_vm(self):
        """
        Creates an image for running Raspbian in a QEMU virtual machine.

        Based on the guide at:

            https://github.com/dhruvvyas90/qemu-rpi-kernel/wiki/Emulating-Jessie-image-with-4.1.x-kernel
        """

        r = self.local_renderer

        r.comment('Installing system packages.')
        r.sudo('add-apt-repository ppa:linaro-maintainers/tools')
        r.sudo('apt-get update')
        r.sudo('apt-get install libsdl-dev qemu-system')

        r.comment('Download image.')
        r.local('wget https://downloads.raspberrypi.org/raspbian_lite_latest')
        r.local('unzip raspbian_lite_latest.zip')
        #TODO:fix name?
        #TODO:resize image?

        r.comment('Find start of the Linux ext4 partition.')
        r.local(
            "parted -s 2016-03-18-raspbian-jessie-lite.img unit B print | "
            "awk '/^Number/{{p=1;next}}; p{{gsub(/[^[:digit:]]/, "", $2); print $2}}' | sed -n 2p", assign_to='START')

        r.local('mkdir -p {raspbian_mount_point}')
        r.sudo('mount -v -o offset=$START -t ext4 {raspbian_image} $MNT')

        r.comment('Comment out everything in ld.so.preload')
        r.local("sed -i 's/^/#/g' {raspbian_mount_point}/etc/ld.so.preload")

        r.comment('Comment out entries containing /dev/mmcblk in fstab.')
        r.local("sed -i '/mmcblk/ s?^?#?' /etc/fstab")

        r.sudo('umount {raspbian_mount_point}')

        r.comment('Download kernel.')
        r.local('wget https://github.com/dhruvvyas90/qemu-rpi-kernel/blob/master/{raspbian_kernel}?raw=true')
        r.local('mv {raspbian_kernel} {libvirt_images_dir}')

        r.comment('Creating libvirt machine.')
        r.local('virsh define libvirt-raspbian.xml')

        r.comment('You should now be able to boot the VM by running:')
        r.comment('')
        r.comment('    qemu-system-arm -kernel {libvirt_boot_dir}/{raspbian_kernel} '
            '-cpu arm1176 -m 256 -M versatilepb -serial stdio -append "root=/dev/sda2 rootfstype=ext4 rw" '
            '-hda {libvirt_images_dir}/{raspbian_image}')
        r.comment('')
        r.comment('Or by running virt-manager.')