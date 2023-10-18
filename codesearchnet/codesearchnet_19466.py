def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError, e:
            print e
            print "  in Environment delete_thing"
            print "  Thing to be removed: %s at %s" % (thing, thing.location)
            print "  from list: %s" % [(thing, thing.location)
                                       for thing in self.things]
        if thing in self.agents:
            self.agents.remove(thing)