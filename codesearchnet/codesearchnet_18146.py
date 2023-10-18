def pack_args(self):
        """
        Pack the parameters into the form necessary for the integration
        routines above.  For example, packs for calculate_linescan_psf
        """
        mapper = {
            'psf-kfki': 'kfki',
            'psf-alpha': 'alpha',
            'psf-n2n1': 'n2n1',
            'psf-sigkf': 'sigkf',
            'psf-sph6-ab': 'sph6_ab',
            'psf-laser-wavelength': 'laser_wavelength',
            'psf-pinhole-width': 'pinhole_width'
        }
        bads = [self.zscale, 'psf-zslab']

        d = {}
        for k,v in iteritems(mapper):
            if k in self.param_dict:
                d[v] = self.param_dict[k]

        d.update({
            'polar_angle': self.polar_angle,
            'normalize': self.normalize,
            'include_K3_det':self.use_J1
        })

        if self.polychromatic:
            d.update({'nkpts': self.nkpts})
            d.update({'k_dist': self.k_dist})

        if self.do_pinhole:
            d.update({'nlpts': self.num_line_pts})

        d.update({'use_laggauss': True})
        return d