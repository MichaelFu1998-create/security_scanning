def get_kernel_available(self):
        """
            Get a list of kernels available
        """

        kernels = list()
        data = self.get_data("droplets/%s/kernels/" % self.id)
        while True:
            for jsond in data[u'kernels']:
                kernel = Kernel(**jsond)
                kernel.token = self.token
                kernels.append(kernel)
            try:
                url = data[u'links'][u'pages'].get(u'next')
                if not url:
                        break
                data = self.get_data(url)
            except KeyError:  # No links.
                break

        return kernels