def _insert_to_array(self, start, results):
        """ inputs results from workers into hdf4 array """
        qrts, wgts, qsts = results
        #qrts, wgts = results
        #print(qrts)

        with h5py.File(self.database.output, 'r+') as out:
            chunk = self._chunksize
            out['quartets'][start:start+chunk] = qrts
            ##out['weights'][start:start+chunk] = wgts

            ## entered as 0-indexed !
            if self.checkpoint.boots:
                key = "qboots/b{}".format(self.checkpoint.boots-1)
                out[key][start:start+chunk] = qsts
            else:
                out["qstats"][start:start+chunk] = qsts