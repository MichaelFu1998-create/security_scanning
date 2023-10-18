def preview(self, input_filepath):
        '''Play a preview of the output with the current set of effects

        Parameters
        ----------
        input_filepath : str
            Path to input audio file.

        '''
        args = ["play", "--no-show-progress"]
        args.extend(self.globals)
        args.extend(self.input_format)
        args.append(input_filepath)
        args.extend(self.effects)

        play(args)