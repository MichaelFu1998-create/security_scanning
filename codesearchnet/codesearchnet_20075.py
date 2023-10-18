def _add_parsley_ns(cls, namespace_dict):
        """
        Extend XPath evaluation with Parsley extensions' namespace
        """

        namespace_dict.update({
            'parslepy' : cls.LOCAL_NAMESPACE,
            'parsley' : cls.LOCAL_NAMESPACE,
        })
        return namespace_dict