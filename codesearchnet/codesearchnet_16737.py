def del_space(self, name):
        """Delete a space."""
        if name not in self.spaces:
            raise ValueError("Space '%s' does not exist" % name)

        if name in self.static_spaces:
            space = self.static_spaces[name]
            if space.is_derived:
                raise ValueError(
                    "%s has derived spaces" % repr(space.interface)
                )
            else:
                self.static_spaces.del_item(name)
                self.model.spacegraph.remove_node(space)
                self.inherit()
                self.model.spacegraph.update_subspaces(self)
                # TODO: Destroy space

        elif name in self.dynamic_spaces:
            # TODO: Destroy space
            self.dynamic_spaces.del_item(name)

        else:
            raise ValueError("Derived cells cannot be deleted")