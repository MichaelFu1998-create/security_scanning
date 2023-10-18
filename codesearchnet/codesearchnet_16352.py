def deliveries(self):
        """ Get delivery log from Redis"""
        key = make_key(
            event=self.object.event,
            owner_name=self.object.owner.username,
            identifier=self.object.identifier
        )
        return redis.lrange(key, 0, 20)