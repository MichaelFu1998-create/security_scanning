def gmx_resid(self, resid):
        """Returns resid in the Gromacs index by transforming with offset."""
        try:
            gmx_resid = int(self.offset[resid])
        except (TypeError, IndexError):
            gmx_resid = resid + self.offset
        except KeyError:
            raise KeyError("offset must be a dict that contains the gmx resid for {0:d}".format(resid))
        return gmx_resid