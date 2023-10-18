def not_followed_by(parser):
    """Succeeds if the given parser cannot consume input"""
    @tri
    def not_followed_by_block():
        failed = object()
        result = optional(tri(parser), failed)
        if result != failed:
            fail(["not " + _fun_to_str(parser)])
    choice(not_followed_by_block)