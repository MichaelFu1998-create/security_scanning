def update_item(filename, item, uuid):
    """
    Update entry by UUID in the JSON file
    """
    with atomic_write(os.fsencode(str(filename))) as temp_file:
        with open(os.fsencode(str(filename))) as products_file:
            # load the JSON data into memory
            products_data = json.load(products_file)
        # apply modifications to the JSON data wrt UUID
        # TODO: handle this in a neat way
        if 'products' in products_data[-1]:
            # handle orders object
            [products_data[i]["products"][0].update(item) for (
                i, j) in enumerate(products_data) if j["uuid"] == str(uuid)]
        else:
            # handle products object
            [products_data[i].update(item) for (i, j) in enumerate(
                products_data) if j["uuid"] == str(uuid)]
        # save the modified JSON data into the temp file
        json.dump(products_data, temp_file)
        return True