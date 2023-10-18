def _render_closure(self):
        '''Use a closure so that draw attributes can be saved'''
        fillcolor = self.fill
        strokecolor = self.stroke
        strokewidth = self.strokewidth

        def _render(cairo_ctx):
            '''
            At the moment this is based on cairo.

            TODO: Need to work out how to move the cairo specific
                  bits somewhere else.
            '''
            # Go to initial point (CORNER or CENTER):
            transform = self._call_transform_mode(self._transform)

            if fillcolor is None and strokecolor is None:
                # Fixes _bug_FillStrokeNofillNostroke.bot
                return

            cairo_ctx.set_matrix(transform)
            # Run the path commands on the cairo context:
            self._traverse(cairo_ctx)
            # Matrix affects stroke, so we need to reset it:
            cairo_ctx.set_matrix(cairo.Matrix())

            if fillcolor is not None and strokecolor is not None:
                if strokecolor[3] < 1:
                    # Draw onto intermediate surface so that stroke
                    # does not overlay fill
                    cairo_ctx.push_group()

                    cairo_ctx.set_source_rgba(*fillcolor)
                    cairo_ctx.fill_preserve()

                    e = cairo_ctx.stroke_extents()
                    cairo_ctx.set_source_rgba(*strokecolor)
                    cairo_ctx.set_operator(cairo.OPERATOR_SOURCE)
                    cairo_ctx.set_line_width(strokewidth)
                    cairo_ctx.stroke()

                    cairo_ctx.pop_group_to_source()
                    cairo_ctx.paint()
                else:
                    # Fast path if no alpha in stroke
                    cairo_ctx.set_source_rgba(*fillcolor)
                    cairo_ctx.fill_preserve()

                    cairo_ctx.set_source_rgba(*strokecolor)
                    cairo_ctx.set_line_width(strokewidth)
                    cairo_ctx.stroke()
            elif fillcolor is not None:
                cairo_ctx.set_source_rgba(*fillcolor)
                cairo_ctx.fill()
            elif strokecolor is not None:
                cairo_ctx.set_source_rgba(*strokecolor)
                cairo_ctx.set_line_width(strokewidth)
                cairo_ctx.stroke()

        return _render