def leaf_handler(self,*args):
        '''#leaf child handler'''
        desc = self.desc
        pdesc = self.pdesc
        desc['leaf'] = True
        desc['sons_count'] = 0
        pdesc['leaf_son_paths'].append(copy.deepcopy(desc['path']))
        pdesc['leaf_descendant_paths'].append(copy.deepcopy(desc['path']))