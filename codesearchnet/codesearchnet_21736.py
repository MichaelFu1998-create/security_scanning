def child_begin_handler(self,scache,*args):
        '''
            _creat_child_desc
            update depth,parent_breadth_path,parent_path,sib_seq,path,lsib_path,rsib_path,lcin_path,rcin_path
        '''
        pdesc = self.pdesc
        depth = scache.depth
        sib_seq = self.sib_seq
        sibs_len = self.sibs_len
        pdesc_level = scache.pdesc_level
        desc = copy.deepcopy(pdesc)
        desc = reset_parent_desc_template(desc)
        desc['depth'] = depth
        desc['parent_breadth_path'] = copy.deepcopy(desc['breadth_path'])
        desc['sib_seq'] = sib_seq
        desc['parent_path'] = copy.deepcopy(desc['path'])
        desc['path'].append(sib_seq)
        update_desc_lsib_path(desc)
        update_desc_rsib_path(desc,sibs_len)
        if(depth == 1):
            pass
        else:
            update_desc_lcin_path(desc,pdesc_level)
            update_desc_rcin_path(desc,sibs_len,pdesc_level)
        return(desc)