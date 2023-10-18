def assign_prompter(self, prompter):
        """If you want to change the core prompters registry, you can
        override this method in a Question subclass.
        """
        if is_string(prompter):
            if prompter not in prompters:
                eprint("Error: '{}' is not a core prompter".format(prompter))
                sys.exit()
            self.prompter = prompters[prompter]
        else:
            self.prompter = prompter