def configure_camera(self):
        """
        Enables access to the camera.

            http://raspberrypi.stackexchange.com/questions/14229/how-can-i-enable-the-camera-without-using-raspi-config
            https://mike632t.wordpress.com/2014/06/26/raspberry-pi-camera-setup/

        Afterwards, test with:

            /opt/vc/bin/raspistill --nopreview --output image.jpg

        Check for compatibility with:

            vcgencmd get_camera

        which should show:

            supported=1 detected=1

        """
        #TODO:check per OS? Works on Raspbian Jessie
        r = self.local_renderer
        if self.env.camera_enabled:
            r.pc('Enabling camera.')
            #TODO:fix, doesn't work on Ubuntu, which uses commented-out values

            # Set start_x=1
            #r.sudo('if grep "start_x=0" /boot/config.txt; then sed -i "s/start_x=0/start_x=1/g" /boot/config.txt; fi')
            #r.sudo('if grep "start_x" /boot/config.txt; then true; else echo "start_x=1" >> /boot/config.txt; fi')
            r.enable_attr(
                filename='/boot/config.txt',
                key='start_x',
                value=1,
                use_sudo=True,
            )

            # Set gpu_mem=128
#             r.sudo('if grep "gpu_mem" /boot/config.txt; then true; else echo "gpu_mem=128" >> /boot/config.txt; fi')
            r.enable_attr(
                filename='/boot/config.txt',
                key='gpu_mem',
                value=r.env.gpu_mem,
                use_sudo=True,
            )

            # Compile the Raspberry Pi binaries.
            #https://github.com/raspberrypi/userland
            r.run('cd ~; git clone https://github.com/raspberrypi/userland.git; cd userland; ./buildme')
            r.run('touch ~/.bash_aliases')
            #r.run("echo 'PATH=$PATH:/opt/vc/bin\nexport PATH' >> ~/.bash_aliases")
            r.append(r'PATH=$PATH:/opt/vc/bin\nexport PATH', '~/.bash_aliases')
            #r.run("echo 'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/vc/lib\nexport LD_LIBRARY_PATH' >> ~/.bash_aliases")
            r.append(r'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/vc/lib\nexport LD_LIBRARY_PATH', '~/.bash_aliases')
            r.run('source ~/.bashrc')
            r.sudo('ldconfig')

            # Allow our user to access the video device.
            r.sudo("echo 'SUBSYSTEM==\"vchiq\",GROUP=\"video\",MODE=\"0660\"' > /etc/udev/rules.d/10-vchiq-permissions.rules")
            r.sudo("usermod -a -G video {user}")

            r.reboot(wait=300, timeout=60)

            self.test_camera()

        else:
            r.disable_attr(
                filename='/boot/config.txt',
                key='start_x',
                use_sudo=True,
            )
            r.disable_attr(
                filename='/boot/config.txt',
                key='gpu_mem',
                use_sudo=True,
            )
            r.reboot(wait=300, timeout=60)