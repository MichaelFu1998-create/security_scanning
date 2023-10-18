def assert_that(val, description=''):
    """Factory method for the assertion builder with value to be tested and optional description."""
    global _soft_ctx
    if _soft_ctx:
        return AssertionBuilder(val, description, 'soft')
    return AssertionBuilder(val, description)