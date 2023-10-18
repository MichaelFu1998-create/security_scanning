def get_stack_data(self, frame, traceback, event_type):
        """Get the stack frames data at each of the hooks above (Ie. for each
        line of the Python code)"""
        heap_data = Heap(self.options)
        stack_data = StackFrames(self.options)
        stack_frames, cur_frame_ind = self.get_stack(frame, traceback)

        for frame_ind, (frame, lineno) in enumerate(stack_frames):
            skip_this_stack = False

            # Skip the self.run calling frame (first frame)
            if frame_ind == 0:
                continue

            # Skip stack after a certain stack frame depth
            if len(stack_data) > self.options.depth:
                skip_this_stack = True
                break

            # Skip stack when frames dont belong to the current notebook or
            # current cell, I.e. frames in another global scope altogether
            # or frames in other cells
            if (not self.is_notebook_frame(frame) or
                    self.is_other_cell_frame(frame)):
                if not self.options.step_all:
                    skip_this_stack = True
                    break
                lineno = 0  # So line markers dont display for these frames
            else:
                lineno += 1  # Because cell magic is actually line 1

            # Filter out ignored names from the frame locals
            user_locals = filter_dict(
                frame.f_locals,
                ignore_vars + list(self.ipy_shell.user_ns_hidden.keys())
            )

            # Add frame and heap data
            stack_data.add(frame, lineno, event_type, user_locals)
            heap_data.add(user_locals)

        if not skip_this_stack and not stack_data.is_empty():
            self.trace_history.append(
                    stack_data,
                    heap_data,
                    self.stdout.getvalue()
            )