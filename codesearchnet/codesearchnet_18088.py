def get_update_io_tiles(self, params, values):
        """
        Get the tiles corresponding to a particular section of image needed to
        be updated. Inputs are the parameters and values. Returned is the
        padded tile, inner tile, and slicer to go between, but accounting for
        wrap with the edge of the image as necessary.
        """
        # get the affected area of the model image
        otile = self.get_update_tile(params, values)
        if otile is None:
            return [None]*3
        ptile = self.get_padding_size(otile) or util.Tile(0, dim=otile.dim)

        otile = util.Tile.intersection(otile, self.oshape)

        if (otile.shape <= 0).any():
            raise UpdateError("update triggered invalid tile size")

        if (ptile.shape < 0).any() or (ptile.shape > self.oshape.shape).any():
            raise UpdateError("update triggered invalid padding tile size")

        # now remove the part of the tile that is outside the image and pad the
        # interior part with that overhang. reflect the necessary padding back
        # into the image itself for the outer slice which we will call outer
        outer = otile.pad((ptile.shape+1)//2)
        inner, outer = outer.reflect_overhang(self.oshape)
        iotile = inner.translate(-outer.l)

        outer = util.Tile.intersection(outer, self.oshape)
        inner = util.Tile.intersection(inner, self.oshape)
        return outer, inner, iotile