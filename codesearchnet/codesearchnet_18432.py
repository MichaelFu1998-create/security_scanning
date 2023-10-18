def item(proto_dataset_uri, input_file, relpath_in_dataset):
    """Add a file to the proto dataset."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        proto_dataset_uri,
        config_path=CONFIG_PATH)
    if relpath_in_dataset == "":
        relpath_in_dataset = os.path.basename(input_file)
    proto_dataset.put_item(input_file, relpath_in_dataset)