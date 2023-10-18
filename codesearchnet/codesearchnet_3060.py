def _set_name(self, name):
        '''name is py type'''
        if self.own.get('name'):
            self.func_name = name
            self.own['name']['value'] = Js(name)