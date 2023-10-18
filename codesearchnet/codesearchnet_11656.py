def inheritsFrom(self, target_name):
        ''' Return true if this target inherits from the named target (directly
            or indirectly. Also returns true if this target is the named
            target. Otherwise return false.
        '''
        for t in self.hierarchy:
            if t and t.getName() == target_name or target_name in t.description.get('inherits', {}):
                return True
        return False