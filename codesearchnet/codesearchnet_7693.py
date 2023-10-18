def make_formatter(format_name):
    """Returns a callable that outputs the data. Defaults to print."""

    if "json" in format_name:
        from json import dumps
        import datetime
        def jsonhandler(obj): obj.isoformat() if isinstance(obj, (datetime.datetime, datetime.date)) else obj
        if format_name == "prettyjson":
            def jsondumps(data): return dumps(data, default=jsonhandler, indent=2, separators=(',', ': '))
        else:
            def jsondumps(data): return dumps(data, default=jsonhandler)

        def jsonify(data):
            if isinstance(data, dict):
                print(jsondumps(data))
            elif isinstance(data, list):
                print(jsondumps([device._asdict() for device in data]))
            else:
                print(dumps({'result': data}))
        return jsonify
    else:
        def printer(data):
            if isinstance(data, dict):
                print(data)
            else:
                for row in data:
                    print(row)
        return printer