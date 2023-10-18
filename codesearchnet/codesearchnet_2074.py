def discretize_action_space_desc(self):
        """
        Creates a list of discrete action(-combinations) in case we want to learn with a discrete set of actions,
        but only have action-combinations (maybe even continuous) available from the env.
        E.g. the UE4 game has the following action/axis-mappings:

        ```javascript
        {
        'Fire':
            {'type': 'action', 'keys': ('SpaceBar',)},
        'MoveRight':
            {'type': 'axis', 'keys': (('Right', 1.0), ('Left', -1.0), ('A', -1.0), ('D', 1.0))},
        }
        ```

        -> this method will discretize them into the following 6 discrete actions:

        ```javascript
        [
        [(Right, 0.0),(SpaceBar, False)],
        [(Right, 0.0),(SpaceBar, True)]
        [(Right, -1.0),(SpaceBar, False)],
        [(Right, -1.0),(SpaceBar, True)],
        [(Right, 1.0),(SpaceBar, False)],
        [(Right, 1.0),(SpaceBar, True)],
        ]
        ```

        """
        # Put all unique_keys lists in one list and itertools.product that list.
        unique_list = []
        for nice, record in self.action_space_desc.items():
            list_for_record = []
            if record["type"] == "axis":
                # The main key for this record (always the first one)
                head_key = record["keys"][0][0]
                # The reference value (divide by this one to get the others)
                head_value = record["keys"][0][1]
                # The zero key (idle action; axis scale=0.0)
                list_for_record.append((head_key, 0.0))
                set_ = set()
                for key_and_scale in self.action_space_desc[nice]["keys"]:
                    # Build unique lists of mappings (each axis value should only be represented once).
                    if key_and_scale[1] not in set_:
                        list_for_record.append((head_key, key_and_scale[1] / head_value))
                        set_.add(key_and_scale[1])
            else:
                # Action-mapping
                list_for_record = [(record["keys"][0], False), (record["keys"][0], True)]
            unique_list.append(list_for_record)

        def so(in_):
            # in_ is List[Tuple[str,any]] -> sort by concat'd sequence of str(any's)
            st = ""
            for i in in_:
                st += str(i[1])
            return st

        # Then sort and get the entire list of all possible sorted meaningful key-combinations.
        combinations = list(itertools.product(*unique_list))
        combinations = list(map(lambda x: sorted(list(x), key=lambda y: y[0]), combinations))
        combinations = sorted(combinations, key=so)
        # Store that list as discretized_actions.
        self.discretized_actions = combinations