def _get_name_from_structure(item, default):
    """
    Given a possibly sparsely populated item dictionary, try to retrieve the item name.
    First try the default field.  If that doesn't exist, try to parse the from the ARN.
    :param item: dict containing (at the very least) item_name and/or arn
    :return: item name
    """
    if item.get(default):
        return item.get(default)

    if item.get('Arn'):
        arn = item.get('Arn')
        item_arn = ARN(arn)
        if item_arn.error:
            raise CloudAuxException('Bad ARN: {arn}'.format(arn=arn))
        return item_arn.parsed_name

    raise MissingFieldException('Cannot extract item name from input: {input}.'.format(input=item))