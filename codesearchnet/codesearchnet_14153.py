def batch(vars, oldvars, ns):
        """
        Context manager to only update listeners
        at the end, in the meantime it doesn't
        matter what intermediate state the vars
        are in (they can be added and removed)

        >>> with VarListener.batch()
        ...     pass
        """
        snapshot_vars = dict(vars)

        with VarListener.disabled():
            yield

        added_vars = set(oldvars.keys()) - set(snapshot_vars.keys())
        deleted_vars = set(snapshot_vars.keys()) - set(oldvars.keys())
        existing_vars = set(vars.keys()) - added_vars - deleted_vars
        for name in existing_vars:
            old_var = snapshot_vars[name]
            new_var = vars[name]
            if old_var.type != new_var.type or old_var.min != new_var.min or old_var.max != new_var.max:
                deleted_vars.add(name)
                added_vars.add(name)
                if old_var.type == new_var.type:
                    new_var.value = old_var.value

        for listener in VarListener.listeners:
            for name in deleted_vars:
                listener.var_deleted(snapshot_vars[name])
                if ns.get(name) is snapshot_vars[name].value:
                    del ns[name]
            for name in added_vars:
                listener.var_added(vars[name])