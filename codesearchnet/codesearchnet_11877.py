def init_raspbian_disk(self, yes=0):
        """
        Downloads the latest Raspbian image and writes it to a microSD card.

        Based on the instructions from:

        https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
        """
        self.assume_localhost()

        yes = int(yes)
        device_question = 'SD card present at %s? ' % self.env.sd_device
        if not yes and not raw_input(device_question).lower().startswith('y'):
            return

        r = self.local_renderer
        r.local_if_missing(
            fn='{raspbian_image_zip}',
            cmd='wget {raspbian_download_url} -O raspbian_lite_latest.zip')

        r.lenv.img_fn = \
            r.local("unzip -l {raspbian_image_zip} | sed -n 4p | awk '{{print $4}}'", capture=True) or '$IMG_FN'
        r.local('echo {img_fn}')
        r.local('[ ! -f {img_fn} ] && unzip {raspbian_image_zip} {img_fn} || true')
        r.lenv.img_fn = r.local('readlink -f {img_fn}', capture=True)
        r.local('echo {img_fn}')

        with self.settings(warn_only=True):
            r.sudo('[ -d "{sd_media_mount_dir}" ] && umount {sd_media_mount_dir} || true')
        with self.settings(warn_only=True):
            r.sudo('[ -d "{sd_media_mount_dir2}" ] && umount {sd_media_mount_dir2} || true')

        r.pc('Writing the image onto the card.')
        r.sudo('time dd bs=4M if={img_fn} of={sd_device}')

        # Flush all writes to disk.
        r.run('sync')