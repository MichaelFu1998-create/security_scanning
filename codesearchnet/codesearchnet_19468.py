def percept(self, agent):
        "By default, agent perceives things within a default radius."
        return [self.thing_percept(thing, agent)
                for thing in self.things_near(agent.location)]