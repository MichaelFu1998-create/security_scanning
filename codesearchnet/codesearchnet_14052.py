def _set_initial_defaults(self):
        '''Set the default values. Called at __init__ and at the end of run(),
        do that new draw loop iterations don't take up values left over by the
        previous one.'''
        DEFAULT_WIDTH, DEFAULT_HEIGHT = self._canvas.DEFAULT_SIZE
        self.WIDTH = self._namespace.get('WIDTH', DEFAULT_WIDTH)
        self.HEIGHT = self._namespace.get('HEIGHT', DEFAULT_WIDTH)
        if 'WIDTH' in self._namespace or 'HEIGHT' in self._namespace:
            self.size(w=self._namespace.get('WIDTH'), h=self._namespace.get('HEIGHT'))

        self._transformmode = Bot.CENTER

        self._canvas.settings(
            fontfile="assets/notcouriersans.ttf",
            fontsize=16,
            align=Bot.LEFT,
            lineheight=1,
            fillcolor=self.color(.2),
            strokecolor=None,
            strokewidth=1.0,
            background=self.color(1, 1, 1))