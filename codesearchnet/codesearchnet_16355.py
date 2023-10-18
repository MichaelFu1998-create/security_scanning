def notify(self, message):
        """
            TODO: Add code to lpush to redis stack
                    rpop when stack hits size 'X'
        """
        data = dict(
                payload=self.payload,
                attempt=self.attempt,
                success=self.success,
                response_message=self.response_content,
                hash_value=self.hash_value,
                response_status=self.response.status_code,
                notification=message,
                created=timezone.now()
            )
        value = json.dumps(data, cls=StandardJSONEncoder)
        key = make_key(self.event, self.owner.username, self.identifier)
        redis.lpush(key, value)