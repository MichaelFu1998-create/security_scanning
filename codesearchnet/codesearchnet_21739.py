def child_end_handler(self,scache):
        '''
            _upgrade_breadth_info
            update breadth, breadth_path, and add desc to desc_level
        '''
        desc = self.desc
        desc_level = scache.desc_level
        breadth = desc_level.__len__()
        desc['breadth'] = breadth
        desc['breadth_path'].append(breadth)
        desc_level.append(desc)