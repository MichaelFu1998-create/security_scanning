def load_table(self, table):
        """
        Load the file contents into the supplied Table using the
        specified key and filetype. The input table should have the
        filenames as values which will be replaced by the loaded
        data. If data_key is specified, this key will be used to index
        the loaded data to retrive the specified item.
        """
        items,  data_keys = [], None
        for key, filename in table.items():
            data_dict = self.filetype.data(filename[0])
            current_keys = tuple(sorted(data_dict.keys()))
            values = [data_dict[k] for k in current_keys]
            if data_keys is None:
                data_keys = current_keys
            elif data_keys != current_keys:
                raise Exception("Data keys are inconsistent")
            items.append((key, values))

        return Table(items, kdims=table.kdims, vdims=data_keys)