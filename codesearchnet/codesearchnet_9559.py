def baselevels(self):
        """
        Optional baselevels configuration.

        baselevels:
            min: <zoom>
            max: <zoom>
            lower: <resampling method>
            higher: <resampling method>
        """
        if "baselevels" not in self._raw:
            return {}
        baselevels = self._raw["baselevels"]
        minmax = {k: v for k, v in baselevels.items() if k in ["min", "max"]}

        if not minmax:
            raise MapcheteConfigError("no min and max values given for baselevels")
        for v in minmax.values():
            if not isinstance(v, int) or v < 0:
                raise MapcheteConfigError(
                    "invalid baselevel zoom parameter given: %s" % minmax.values()
                )

        zooms = list(range(
            minmax.get("min", min(self.zoom_levels)),
            minmax.get("max", max(self.zoom_levels)) + 1)
        )

        if not set(self.zoom_levels).difference(set(zooms)):
            raise MapcheteConfigError("baselevels zooms fully cover process zooms")

        return dict(
            zooms=zooms,
            lower=baselevels.get("lower", "nearest"),
            higher=baselevels.get("higher", "nearest"),
            tile_pyramid=BufferedTilePyramid(
                self.output_pyramid.grid,
                pixelbuffer=self.output_pyramid.pixelbuffer,
                metatiling=self.process_pyramid.metatiling
            )
        )