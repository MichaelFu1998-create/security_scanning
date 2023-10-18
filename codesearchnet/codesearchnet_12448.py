def train_subprocess(self, *args, **kwargs):
        """
        Trains in a subprocess which provides a timeout guarantees everything shuts down properly

        Args:
            See <train>
        Returns:
            bool: True for success, False if timed out
        """
        ret = call([
            sys.executable, '-m', 'padatious', 'train', self.cache_dir,
            '-d', json.dumps(self.serialized_args),
            '-a', json.dumps(args),
            '-k', json.dumps(kwargs),
        ])
        if ret == 2:
            raise TypeError('Invalid train arguments: {} {}'.format(args, kwargs))
        data = self.serialized_args
        self.clear()
        self.apply_training_args(data)
        self.padaos.compile()
        if ret == 0:
            self.must_train = False
            return True
        elif ret == 10:  # timeout
            return False
        else:
            raise ValueError('Training failed and returned code: {}'.format(ret))