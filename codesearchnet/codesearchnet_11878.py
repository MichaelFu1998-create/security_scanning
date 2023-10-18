def init_ubuntu_disk(self, yes=0):
        """
        Downloads the latest Ubuntu image and writes it to a microSD card.

        Based on the instructions from:

            https://wiki.ubuntu.com/ARM/RaspberryPi

        For recommended SD card brands, see:

            http://elinux.org/RPi_SD_cards

        Note, if you get an error like:

            Kernel panic-not syncing: VFS: unable to mount root fs

        that means the SD card is corrupted. Try re-imaging the card or use a different card.
        """
        self.assume_localhost()

        yes = int(yes)

        if not self.dryrun:
            device_question = 'SD card present at %s? ' % self.env.sd_device
            inp = raw_input(device_question).strip()
            print('inp:', inp)
            if not yes and inp and not inp.lower().startswith('y'):
                return

        r = self.local_renderer

        # Confirm SD card is present.
        r.local('ls {sd_device}')

        # Download image.
        r.env.ubuntu_image_fn = os.path.abspath(os.path.split(self.env.ubuntu_download_url)[-1])
        r.local('[ ! -f {ubuntu_image_fn} ] && wget {ubuntu_download_url} || true')

        # Ensure SD card is unmounted.
        with self.settings(warn_only=True):
            r.sudo('[ -d "{sd_media_mount_dir}" ] && umount {sd_media_mount_dir}')
        with self.settings(warn_only=True):
            r.sudo('[ -d "{sd_media_mount_dir2}" ] && umount {sd_media_mount_dir2}')

        r.pc('Writing the image onto the card.')
        r.sudo('xzcat {ubuntu_image_fn} | dd bs=4M of={sd_device}')

        # Flush all writes to disk.
        r.run('sync')