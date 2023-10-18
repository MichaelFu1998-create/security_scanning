def _delete_key_internal(self, *args, **kwargs):
        """Remove key name from bucket set.
        """
        mimicdb.backend.srem(tpl.bucket % self.name, args[0])
        mimicdb.backend.delete(tpl.key % (self.name, args[0]))

        return super(Bucket, self)._delete_key_internal(*args, **kwargs)