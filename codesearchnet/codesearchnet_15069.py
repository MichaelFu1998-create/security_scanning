def connect_to(self, other_mesh):
        """Create a connection to an other mesh.

        .. warning:: Both meshes need to be disconnected and one needs to be
          a consumed and the other a produced mesh. You can check if a
          connection is possible using :meth:`can_connect_to`.

        .. seealso:: :meth:`is_consumed`, :meth:`is_produced`,
          :meth:`can_connect_to`
        """
        other_mesh.disconnect()
        self.disconnect()
        self._connect_to(other_mesh)