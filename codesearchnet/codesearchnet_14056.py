def _makeColorableInstance(self, clazz, args, kwargs):
        """
        Create an object, if fill, stroke or strokewidth
        is not specified, get them from the _canvas

        :param clazz:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs = dict(kwargs)

        fill = kwargs.get('fill', self._canvas.fillcolor)
        if not isinstance(fill, Color):
            fill = Color(fill, mode='rgb', color_range=1)
        kwargs['fill'] = fill

        stroke = kwargs.get('stroke', self._canvas.strokecolor)
        if not isinstance(stroke, Color):
            stroke = Color(stroke, mode='rgb', color_range=1)
        kwargs['stroke'] = stroke

        kwargs['strokewidth'] = kwargs.get('strokewidth', self._canvas.strokewidth)
        inst = clazz(self, *args, **kwargs)
        return inst