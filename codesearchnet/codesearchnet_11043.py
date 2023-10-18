def keyboard_event(self, key, action, modifier):
        """
        Handles the standard keyboard events such as camera movements,
        taking a screenshot, closing the window etc.

        Can be overriden add new keyboard events. Ensure this method
        is also called if you want to keep the standard features.

        Arguments:
            key: The key that was pressed or released
            action: The key action. Can be `ACTION_PRESS` or `ACTION_RELEASE`
            modifier: Modifiers such as holding shift or ctrl
        """
        # The well-known standard key for quick exit
        if key == self.keys.ESCAPE:
            self.close()
            return

        # Toggle pause time
        if key == self.keys.SPACE and action == self.keys.ACTION_PRESS:
            self.timer.toggle_pause()

        # Camera movement
        # Right
        if key == self.keys.D:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_right(True)
            elif action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_right(False)
        # Left
        elif key == self.keys.A:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_left(True)
            elif action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_left(False)
        # Forward
        elif key == self.keys.W:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_forward(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_forward(False)
        # Backwards
        elif key == self.keys.S:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_backward(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_backward(False)

        # UP
        elif key == self.keys.Q:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_down(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_down(False)

        # Down
        elif key == self.keys.E:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_up(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_up(False)

        # Screenshots
        if key == self.keys.X and action == self.keys.ACTION_PRESS:
            screenshot.create()

        if key == self.keys.R and action == self.keys.ACTION_PRESS:
            project.instance.reload_programs()

        if key == self.keys.RIGHT and action == self.keys.ACTION_PRESS:
            self.timer.set_time(self.timer.get_time() + 10.0)

        if key == self.keys.LEFT and action == self.keys.ACTION_PRESS:
            self.timer.set_time(self.timer.get_time() - 10.0)

        # Forward the event to the timeline
        self.timeline.key_event(key, action, modifier)