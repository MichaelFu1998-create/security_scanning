def emit_to_room(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in six.iteritems(self.socket.server.sockets):
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms'] and self.socket != socket:
                socket.send_packet(pkt)