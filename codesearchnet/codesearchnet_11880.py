def create_raspbian_vagrant_box(self):
        """
        Creates a box for easily spinning up a virtual machine with Vagrant.

        http://unix.stackexchange.com/a/222907/16477
        https://github.com/pradels/vagrant-libvirt
        """

        r = self.local_renderer

        r.sudo('adduser --disabled-password --gecos "" vagrant')

        #vagrant user should be able to run sudo commands without a password prompt

        r.sudo('echo "vagrant ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vagrant')
        r.sudo('chmod 0440 /etc/sudoers.d/vagrant')

        r.sudo('apt-get update')
        r.sudo('apt-get install -y openssh-server')

        #put ssh key from vagrant user

        r.sudo('mkdir -p /home/vagrant/.ssh')
        r.sudo('chmod 0700 /home/vagrant/.ssh')
        r.sudo('wget --no-check-certificate https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub -O /home/vagrant/.ssh/authorized_keys')
        r.sudo('chmod 0600 /home/vagrant/.ssh/authorized_keys')
        r.sudo('chown -R vagrant /home/vagrant/.ssh')

        #open sudo vi /etc/ssh/sshd_config and change

        #PubKeyAuthentication yes
        #PermitEmptyPasswords no
        r.sudo("sed -i '/AuthorizedKeysFile/s/^#//g' /etc/ssh/sshd_config")
        #PasswordAuthentication no
        r.sudo("sed -i '/PasswordAuthentication/s/^#//g' /etc/ssh/sshd_config")
        r.sudo("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")

        #restart ssh service using

        #sudo service ssh restart

        #install additional development packages for the tools to properly compile and install
        r.sudo('apt-get upgrade')
        r.sudo('apt-get install -y gcc build-essential')
        #TODO:fix? throws dpkg: error: fgets gave an empty string from `/var/lib/dpkg/triggers/File'
        #r.sudo('apt-get install -y linux-headers-rpi')

        #do any change that you want and shutdown the VM . now , come to host machine on which guest VM is running and goto
        #the /var/lib/libvirt/images/ and choose raw image in which you did the change and copy somewhere for example /test

        r.sudo('mkdir /tmp/test')
        r.sudo('cp {libvirt_images_dir}/{raspbian_image} /tmp/test')
        r.sudo('cp {libvirt_boot_dir}/{raspbian_kernel} /tmp/test')

        #create two file metadata.json and Vagrantfile in /test do entry in metadata.json
        r.render_to_file('rpi/metadata.json', '/tmp/test/metadata.json')
        r.render_to_file('rpi/Vagrantfile', '/tmp/test/Vagrantfile')

        #convert test.img to qcow2 format using
        r.sudo('qemu-img convert -f raw -O qcow2  {libvirt_images_dir}/{raspbian_image}  {libvirt_images_dir}/{raspbian_image}.qcow2')

        #rename ubuntu.qcow2 to box.img
        r.sudo('mv {libvirt_images_dir}/{raspbian_image}.qcow2 {libvirt_images_dir}/box.img')

        #Note: currently,libvirt-vagrant support only qcow2 format. so , don't change the format just rename to box.img.
        #because it takes input with name box.img by default.
        #create box

        r.sudo('cd /tmp/test; tar cvzf custom_box.box ./metadata.json ./Vagrantfile ./{raspbian_kernel} ./box.img')