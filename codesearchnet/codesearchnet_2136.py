def save_model(self, directory=None, append_timestep=True):
        """
        Save TensorFlow model. If no checkpoint directory is given, the model's default saver
        directory is used. Optionally appends current timestep to prevent overwriting previous
        checkpoint files. Turn off to be able to load model from the same given path argument as
        given here.

        Args:
            directory (str): Optional checkpoint directory.
            append_timestep (bool):  Appends the current timestep to the checkpoint file if true.
                If this is set to True, the load path must include the checkpoint timestep suffix.
                For example, if stored to models/ and set to true, the exported file will be of the
                form models/model.ckpt-X where X is the last timestep saved. The load path must
                precisely match this file name. If this option is turned off, the checkpoint will
                always overwrite the file specified in path and the model can always be loaded under
                this path.

        Returns:
            Checkpoint path were the model was saved.
        """
        return self.model.save(directory=directory, append_timestep=append_timestep)