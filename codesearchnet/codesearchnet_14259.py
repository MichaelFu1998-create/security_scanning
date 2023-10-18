def output_closure(self, target, file_number=None):
        '''
        Function to output to a cairo surface

        target is a cairo Context or filename
        if file_number is set, then files will be numbered
        (this is usually set to the current frame number)
        '''
        def output_context(ctx):
            target_ctx = target
            target_ctx.set_source_surface(ctx.get_target())
            target_ctx.paint()
            return target_ctx

        def output_surface(ctx):
            target_ctx = cairo.Context(target)
            target_ctx.set_source_surface(ctx.get_target())
            target_ctx.paint()
            return target_ctx

        def output_file(ctx):
            root, extension = os.path.splitext(target)
            if file_number:
                filename = '%s_%04d%s' % (root, file_number, extension)
            else:
                filename = target

            extension = extension.lower()
            if extension == '.png':
                surface = ctx.get_target()
                surface.write_to_png(target)
            elif extension == '.pdf':
                target_ctx = cairo.Context(cairo.PDFSurface(filename, *self.size_or_default()))
                target_ctx.set_source_surface(ctx.get_target())
                target_ctx.paint()
            elif extension in ('.ps', '.eps'):
                target_ctx = cairo.Context(cairo.PSSurface(filename, *self.size_or_default()))
                if extension == '.eps':
                    target_ctx.set_eps(extension='.eps')
                target_ctx.set_source_surface(ctx.get_target())
                target_ctx.paint()
            elif extension == '.svg':
                target_ctx = cairo.Context(cairo.SVGSurface(filename, *self.size_or_default()))
                target_ctx.set_source_surface(ctx.get_target())
                target_ctx.paint()
            return filename

        if isinstance(target, cairo.Context):
            return output_context
        elif isinstance(target, cairo.Surface):
            return output_surface
        else:
            return output_file