def get_item(filename, uuid):
    """
    Read entry from JSON file
    """
    with open(os.fsencode(str(filename)), "r") as f:
        data = json.load(f)
        results = [i for i in data if i["uuid"] == str(uuid)]
        if results:
            return results
        return None