def snapshot(self, target=None, defer=None, autonumber=False):
        '''Save the contents of current surface into a file or cairo surface/context

        :param filename: Can be a filename or a Cairo surface.
        :param defer: If true, buffering/threading may be employed however output will not be immediate.
        :param autonumber: If true then a number will be appended to the filename.
        '''
        if autonumber:
            file_number = self._frame
        else:
            file_number = None

        if isinstance(target, cairo.Surface):
            # snapshot to Cairo surface
            if defer is None:
                self._canvas.snapshot(surface, defer)
                defer = False
            ctx = cairo.Context(target)
            # this used to be self._canvas.snapshot, but I couldn't make it work.
            # self._canvas.snapshot(target, defer)
            # TODO: check if this breaks when taking more than 1 snapshot
            self._canvas._drawqueue.render(ctx)
            return
        elif target is None:
            # If nothing specified, use a default filename from the script name
            script_file = self._namespace.get('__file__')
            if script_file:
                target = os.path.splitext(script_file)[0] + '.svg'
                file_number = True

        if target:
            # snapshot to file, target is a filename
            if defer is None:
                defer = True
            self._canvas.snapshot(target, defer=defer, file_number=file_number)
        else:
            raise ShoebotError('No image saved')