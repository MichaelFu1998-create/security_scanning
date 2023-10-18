def set_value(request):
        """Set the value and returns *True* or *False*."""

        key = request.matchdict['key']
        _VALUES[key] = request.json_body
        return _VALUES.get(key)