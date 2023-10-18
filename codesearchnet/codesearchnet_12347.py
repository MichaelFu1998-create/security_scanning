def init_map(self):
        """ Add markers, polys, callouts, etc.."""
        d = self.declaration
        if d.show_location:
            self.set_show_location(d.show_location)
        if d.show_traffic:
            self.set_show_traffic(d.show_traffic)
        if d.show_indoors:
            self.set_show_indoors(d.show_indoors)
        if d.show_buildings:
            self.set_show_buildings(d.show_buildings)

        #: Local ref access is faster
        mapview = self.map
        mid = mapview.getId()

        #: Connect signals
        #: Camera
        mapview.onCameraChange.connect(self.on_camera_changed)
        mapview.onCameraMoveStarted.connect(self.on_camera_move_started)
        mapview.onCameraMoveCanceled.connect(self.on_camera_move_stopped)
        mapview.onCameraIdle.connect(self.on_camera_move_stopped)
        mapview.setOnCameraChangeListener(mid)
        mapview.setOnCameraMoveStartedListener(mid)
        mapview.setOnCameraMoveCanceledListener(mid)
        mapview.setOnCameraIdleListener(mid)

        #: Clicks
        mapview.onMapClick.connect(self.on_map_clicked)
        mapview.setOnMapClickListener(mid)
        mapview.onMapLongClick.connect(self.on_map_long_clicked)
        mapview.setOnMapLongClickListener(mid)

        #: Markers
        mapview.onMarkerClick.connect(self.on_marker_clicked)
        mapview.setOnMarkerClickListener(self.map.getId())
        mapview.onMarkerDragStart.connect(self.on_marker_drag_start)
        mapview.onMarkerDrag.connect(self.on_marker_drag)
        mapview.onMarkerDragEnd.connect(self.on_marker_drag_end)
        mapview.setOnMarkerDragListener(mid)

        #: Info window
        mapview.onInfoWindowClick.connect(self.on_info_window_clicked)
        mapview.onInfoWindowLongClick.connect(self.on_info_window_long_clicked)
        mapview.onInfoWindowClose.connect(self.on_info_window_closed)
        mapview.setOnInfoWindowClickListener(mid)
        mapview.setOnInfoWindowCloseListener(mid)
        mapview.setOnInfoWindowLongClickListener(mid)

        #: Polys
        mapview.onPolygonClick.connect(self.on_poly_clicked)
        mapview.onPolylineClick.connect(self.on_poly_clicked)
        mapview.setOnPolygonClickListener(mid)
        mapview.setOnPolylineClickListener(mid)

        #: Circle
        mapview.onCircleClick.connect(self.on_circle_clicked)
        mapview.setOnCircleClickListener(mid)