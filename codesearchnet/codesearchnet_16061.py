def split_capillary_id(self):
        '''Gets the prefix and suffix of an name of a capillary read, e.g. xxxxx.p1k or xxxx.q1k. Returns a tuple (prefix, suffx)'''
        try:
            a = self.id.rsplit('.', 1)
            if a[1].startswith('p'):
                dir = 'fwd'
            elif a[1].startswith('q'):
                dir = 'rev'
            else:
                dir = 'unk'

            return {'prefix': a[0], 'dir': dir, 'suffix':a[1]}
        except:
            raise Error('Error in split_capillary_id() on ID', self.id)