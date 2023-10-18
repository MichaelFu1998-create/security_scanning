def metadata(proto_dataset_uri, relpath_in_dataset, key, value):
    """Add metadata to a file in the proto dataset."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH)
    proto_dataset.add_item_metadata(
        handle=relpath_in_dataset,
        key=key,
        value=value)