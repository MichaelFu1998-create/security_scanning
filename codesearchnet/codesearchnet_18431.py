def write(proto_dataset_uri, input):
    """Use YAML from a file or stdin to populate the readme.

    To stream content from stdin use "-", e.g.

    echo "desc: my data" | dtool readme write <DS_URI> -
    """
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri
    )
    _validate_and_put_readme(proto_dataset, input.read())