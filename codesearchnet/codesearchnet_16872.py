def _make_file_dict(self, f):
        """Make a dictionary with filename and base64 file data"""
        if isinstance(f, dict):
            file_obj = f['file']
            if 'filename' in f:
                file_name = f['filename']
            else:
                file_name = file_obj.name
        else:
            file_obj = f
            file_name = f.name

        b64_data = base64.b64encode(file_obj.read())
        return {
            'id': file_name,
            'data': b64_data.decode() if six.PY3 else b64_data,
        }