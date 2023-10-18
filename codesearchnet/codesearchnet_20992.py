def generate(request):
    """ Create a new DataItem. """
    models.DataItem.create(
        content=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    )
    return muffin.HTTPFound('/')