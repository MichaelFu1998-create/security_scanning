def update (self):
        """ Calculate what the desired change in velocity is. 
        delta_velocity = acceleration * delta_time
        Time will be dealt with by the sprite. """
        delta_velocity = Vector.null()
        target_position = self.target.get_position()
        sprite_position = self.sprite.get_position()

        desired_direction = target_position - sprite_position

        if 0.0 == self.los or desired_direction.magnitude <= self.los:
            try:
                desired_normal = desired_direction.normal
            except NullVectorError:
                desired_normal = Vector.null()
            desired_velocity = desired_normal * self.sprite.get_max_speed()
            delta_velocity = desired_velocity - self.sprite.get_velocity()

        self.last_delta_velocity = delta_velocity
        return delta_velocity, self.power