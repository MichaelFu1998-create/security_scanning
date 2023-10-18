def non_leaf_handler(self,lcache):
        '''#nonleaf child handler'''
        desc = self.desc
        pdesc = self.pdesc
        desc['leaf'] = False
        pdesc['non_leaf_son_paths'].append(copy.deepcopy(desc['path']))
        pdesc['non_leaf_descendant_paths'].append(copy.deepcopy(desc['path']))
        lcache.ndata.append(self.data)
        lcache.ndesc.append(desc)