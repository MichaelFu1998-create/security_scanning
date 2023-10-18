def make_hash(self, task):
        """Create a hash of the task inputs.

        This uses a serialization library borrowed from ipyparallel.
        If this fails here, then all ipp calls are also likely to fail due to failure
        at serialization.

        Args:
            - task (dict) : Task dictionary from dfk.tasks

        Returns:
            - hash (str) : A unique hash string
        """
        # Function name TODO: Add fn body later
        t = [serialize_object(task['func_name'])[0],
             serialize_object(task['fn_hash'])[0],
             serialize_object(task['args'])[0],
             serialize_object(task['kwargs'])[0],
             serialize_object(task['env'])[0]]
        x = b''.join(t)
        hashedsum = hashlib.md5(x).hexdigest()
        return hashedsum