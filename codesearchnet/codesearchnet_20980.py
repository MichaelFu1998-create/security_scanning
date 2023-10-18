def tokens_referenced(self):
        """
        Return a list of all the tokens that are referenced (i.e. contained in) 
        this message.  Tokens that haven't been assigned an id yet are searched 
        recursively for tokens.  So this method may return fewer results after 
        the message is sent.  This information is used by the game engine to 
        catch mistakes like forgetting to add a token to the world or keeping a 
        stale reference to a token after its been removed.
        """
        tokens = set()

        # Use the pickle machinery to find all the tokens contained at any 
        # level of this message.  When an object is being pickled, the Pickler 
        # calls its persistent_id() method for each object it encounters.  We  
        # hijack this method to add every Token we encounter to a list.

        # This definitely feels like a hacky abuse of the pickle machinery, but 
        # that notwithstanding this should be quite robust and quite fast.

        def persistent_id(obj):
            from .tokens import Token

            if isinstance(obj, Token):
                tokens.add(obj)

                # Recursively descend into tokens that haven't been assigned an 
                # id yet, but not into tokens that have.

                return obj.id

        from pickle import Pickler
        from io import BytesIO

        # Use BytesIO to basically ignore the serialized data stream, since we 
        # only care about visiting all the objects that would be pickled.

        pickler = Pickler(BytesIO())
        pickler.persistent_id = persistent_id
        pickler.dump(self)

        return tokens