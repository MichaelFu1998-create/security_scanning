def detail(self, *args, **kwargs):
        prefix = kwargs.pop("prefix", default_prefix)
        # remove dublicates
        kwargs["votes"] = list(set(kwargs["votes"]))
        """ This is an example how to sort votes prior to using them in the
            Object
        """
        # # Sort votes
        # kwargs["votes"] = sorted(
        #     kwargs["votes"],
        #     key=lambda x: float(x.split(":")[1]),
        # )
        return OrderedDict(
            [
                ("memo_key", PublicKey(kwargs["memo_key"], prefix=prefix)),
                ("voting_account", ObjectId(kwargs["voting_account"], "account")),
                ("num_witness", Uint16(kwargs["num_witness"])),
                ("num_committee", Uint16(kwargs["num_committee"])),
                ("votes", Array([VoteId(o) for o in kwargs["votes"]])),
                ("extensions", Set([])),
            ]
        )