def nconflicts(self, var, val, assignment):
        "Return the number of conflicts var=val has with other variables."
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment
                    and not self.constraints(var, val, var2, assignment[var2]))
        return count_if(conflict, self.neighbors[var])