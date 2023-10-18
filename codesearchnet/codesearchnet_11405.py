def mem_size(self):
        '''used when allocating memory ingame'''

        data_len = self._data_mem_size
        node_count = len(list(self.xml_doc.iter(tag=etree.Element)))

        if self.compressed:
            size = 52 * node_count + data_len + 630
        else:
            tags_len = 0
            for e in self.xml_doc.iter(tag=etree.Element):
                e_len = max(len(e.tag), 8)
                e_len = (e_len + 3) & ~3
                tags_len += e_len

            size = 56 * node_count + data_len + 630 + tags_len

        # debugging
        #print('nodes:{} ({}) data:{} ({})'.format(node_count,hex(node_count), data_len, hex(data_len)))

        return (size + 8) & ~7