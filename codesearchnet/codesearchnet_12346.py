def init_options(self):
        """ Initialize the underlying map options.

        """
        self.options = GoogleMapOptions()
        d = self.declaration
        self.set_map_type(d.map_type)
        if d.ambient_mode:
            self.set_ambient_mode(d.ambient_mode)
        if (d.camera_position or d.camera_zoom or
                d.camera_tilt or d.camera_bearing):
            self.update_camera()
        if d.map_bounds:
            self.set_map_bounds(d.map_bounds)
        if not d.show_compass:
            self.set_show_compass(d.show_compass)
        if not d.show_zoom_controls:
            self.set_show_zoom_controls(d.show_zoom_controls)
        if not d.show_toolbar:
            self.set_show_toolbar(d.show_toolbar)
        if d.lite_mode:
            self.set_lite_mode(d.lite_mode)
        if not d.rotate_gestures:
            self.set_rotate_gestures(d.rotate_gestures)
        if not d.scroll_gestures:
            self.set_scroll_gestures(d.scroll_gestures)
        if not d.tilt_gestures:
            self.set_tilt_gestures(d.tilt_gestures)
        if not d.zoom_gestures:
            self.set_zoom_gestures(d.zoom_gestures)
        if d.min_zoom:
            self.set_min_zoom(d.min_zoom)
        if d.max_zoom:
            self.set_max_zoom(d.max_zoom)