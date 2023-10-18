def read_file(self, filename): 
        """
        Guess the filetype and read the file into row sets
        """
        #print("Reading file", filename)

        try:
            fh = open(filename, 'rb')
            table_set = any_tableset(fh) # guess the type...
        except:
            #traceback.print_exc()
            # Cannot find the schema.
            table_set = None
            
        return table_set