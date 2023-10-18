def parent_handler(self,lcache,i,*args):
        '''
            _update_pdesc_sons_info
        '''
        pdesc = lcache.desc[i]
        pdesc['sons_count'] = self.sibs_len
        pdesc['leaf_son_paths'] = []
        pdesc['non_leaf_son_paths'] = []
        pdesc['leaf_descendant_paths'] = []
        pdesc['non_leaf_descendant_paths'] = []
        return(pdesc)