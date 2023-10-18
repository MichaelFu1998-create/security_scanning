def set_item(filename, item):
    """
    Save entry to JSON file
    """
    with atomic_write(os.fsencode(str(filename))) as temp_file:
        with open(os.fsencode(str(filename))) as products_file:
            # load the JSON data into memory
            products_data = json.load(products_file)
        # check if UUID already exists
        uuid_list = [i for i in filter(
            lambda z: z["uuid"] == str(item["uuid"]), products_data)]
        if len(uuid_list) == 0:
            # add the new item to the JSON file
            products_data.append(item)
            # save the new JSON to the temp file
            json.dump(products_data, temp_file)
            return True
        return None