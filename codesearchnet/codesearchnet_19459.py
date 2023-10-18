def ReflexVacuumAgent():
    "A reflex agent for the two-state vacuum environment. [Fig. 2.8]"
    def program((location, status)):
        if status == 'Dirty': return 'Suck'
        elif location == loc_A: return 'Right'
        elif location == loc_B: return 'Left'
    return Agent(program)