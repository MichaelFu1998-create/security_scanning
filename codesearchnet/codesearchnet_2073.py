def translate_abstract_actions_to_keys(self, abstract):
        """
        Translates a list of tuples ([pretty mapping], [value]) to a list of tuples ([some key], [translated value])
        each single item in abstract will undergo the following translation:

        Example1:
        we want: "MoveRight": 5.0
        possible keys for the action are: ("Right", 1.0), ("Left", -1.0)
        result: "Right": 5.0 * 1.0 = 5.0

        Example2:
        we want: "MoveRight": -0.5
        possible keys for the action are: ("Left", -1.0), ("Right", 1.0)
        result: "Left": -0.5 * -1.0 = 0.5 (same as "Right": -0.5)
        """

        # Solve single tuple with name and value -> should become a list (len=1) of this tuple.
        if len(abstract) >= 2 and not isinstance(abstract[1], (list, tuple)):
            abstract = list((abstract,))

        # Now go through the list and translate each axis into an actual keyboard key (or mouse event/etc..).
        actions, axes = [], []
        for a in abstract:
            # first_key = key-name (action mapping or discretized axis mapping) OR tuple (key-name, scale) (continuous
            # axis mapping)
            first_key = self.action_space_desc[a[0]]["keys"][0]
            # action mapping
            if isinstance(first_key, (bytes, str)):
                actions.append((first_key, a[1]))
            # axis mapping
            elif isinstance(first_key, tuple):
                axes.append((first_key[0], a[1] * first_key[1]))
            else:
                raise TensorForceError("action_space_desc contains unsupported type for key {}!".format(a[0]))

        return actions, axes