def embed_data(request):
    """
    Create a temporary directory with input data for the test.
    The directory contents is copied from a directory with the same name as the module located in the same directory of
    the test module.
    """
    result = _EmbedDataFixture(request)
    result.delete_data_dir()
    result.create_data_dir()
    yield result
    result.delete_data_dir()