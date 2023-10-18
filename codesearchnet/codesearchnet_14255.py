def _grow(self, generation, rule, angle, length, time=maxint, draw=True):

        """ Recurse through the system.
        
        When a segment is drawn, the LSsytem.segment() method will be called.
        You can customize this method to create your own visualizations.
        It takes an optional time parameter. 
        
        If you divide this parameter by LSsytem.duration() you get 
        a number between 0.0 and 1.0 you can use as an alpha value for example.
        
        The method also has an id parameter which is a unique number 
        between 0 and LSystem.segments.
        
        """

        if generation == 0: 
        	# We are at the bottom of the system so now we now the total time needed.
        	self._duration = 1 + maxint-time
        
        if length <= self.threshold: 
        	# Segment length has fallen below the threshold, stop recursing.
        	self._duration = 1 + maxint-time
        	return

        if rule in self.commands: 
        	# Custom command symbols:
        	# If the rule is a key in the LSsytem.commands dictionary,
        	# execute its value which is a function taking 6 parameters:
        	# lsystem, generation, rule, angle, length and time.
            self.commands[rule](self, generation, rule, angle, length, time)
        
        if draw:
            # Standard command symbols:
            # f signifies a move,
            # + and - rotate either left or right, | rotates 180 degrees,
            # [ and ] are for push() and pop(), e.g. offshoot branches,
            # < and > decrease or increases the segment length,
            # ( and ) decrease or increases the rotation angle.
	        if   rule == "f": _ctx.translate(0, -min(length, length*time))
	        elif rule == "-": _ctx.rotate(max(-angle, -angle*time))
	        elif rule == "+": _ctx.rotate(min(+angle, +angle*time))
	        elif rule == "|": _ctx.rotate(180)
	        elif rule == "[": _ctx.push()
	        elif rule == "]": _ctx.pop()

        if rule in self.rules \
        and generation > 0 \
        and time > 0:
        	# Recursion:
        	# Occurs when there is enough "life" (i.e. generation or time).
        	# Generation is decreased and segment length scaled down.
        	# Also, F symbols in the rule have a cost that depletes time.
            for cmd in self.rules[rule]:
            	# Modification command symbols:
                if   cmd == "F": time -= self.cost
                elif cmd == "!": angle = -angle
                elif cmd == "(": angle *= 1.1
                elif cmd == ")": angle *= 0.9
                elif cmd == "<": length *= 0.9
                elif cmd == ">": length *= 1.1
                self._grow(
                    generation-1,
                    cmd, 
                    angle, 
                    length*self.decrease, 
                    time,
                    draw
                )
        
        elif rule == "F" \
        or (rule in self.rules and self.rules[rule] == ""):
        	# Draw segment:
        	# If the rule is an F symbol or empty (e.g. in Penrose tiles).
        	# Segment length grows to its full size as time progresses.
            self._segments += 1
            if draw and time > 0:
            	length = min(length, length*time)
            	if self._timed:
            	    self.segment(length, generation, time, id=self._segments)
                else:
                    self.segment(length, generation, None, id=self._segments)
            	_ctx.translate(0, -length)