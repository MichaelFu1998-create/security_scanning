def update(self, time):
        """ Update acceleration. Accounts for the importance and
        priority (order) of multiple behaviors. """
        
        # .... I feel this stuff could be done a lot better.
        total_acceleration = Vector.null()
        max_jerk = self.max_acceleration

        for behavior in self.behaviors:
            acceleration, importance = behavior.update()
            weighted_acceleration = acceleration * importance

            """ 
            if max_jerk >= weighted_acceleration.magnitude:
                max_jerk -= weighted_acceleration.magnitude
                total_acceleration += weighted_acceleration
            elif max_jerk > 0 and max_jerk < weighted_acceleration.magnitude:
                total_acceleration += weighted_acceleration.normal * max_jerk
                break
            else:
                break """
            total_acceleration += weighted_acceleration

        self.acceleration = total_acceleration

        # Update position and velocity.
        Sprite.update(self, time)

        # Update facing direction.
        if self.velocity.magnitude > 0.0:
            self.facing = self.velocity.normal