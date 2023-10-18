def set_project(self, project):
        """Set the base project for routing."""
        def visit(x):
            # Try to set_project, then recurse through any values()
            set_project = getattr(x, 'set_project', None)
            if set_project:
                set_project(project)
            values = getattr(x, 'values', lambda: ())
            for v in values():
                visit(v)

        visit(self.routing)