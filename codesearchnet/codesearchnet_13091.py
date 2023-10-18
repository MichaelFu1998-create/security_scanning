def _insert_to_array(self, chunk, results):
        """
        Enters results arrays into the HDF5 database.
        """

        ## two result arrs
        chunksize = self._chunksize
        qrts, invs = results

        ## enter into db
        with h5py.File(self.database.output, 'r+') as io5:
            io5['quartets'][chunk:chunk+chunksize] = qrts

            ## entered as 0-indexed !
            if self.params.save_invariants:
                if self.checkpoint.boots:
                    key = "invariants/boot{}".format(self.checkpoint.boots)
                    io5[key][chunk:chunk+chunksize] = invs
                else:
                    io5["invariants/boot0"][chunk:chunk+chunksize] = invs