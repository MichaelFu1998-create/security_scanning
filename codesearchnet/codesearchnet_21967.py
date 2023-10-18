def resourcePath(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        from os import path
        import sys
        
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = path.dirname(path.abspath(__file__))
        return path.join(base_path, relative_path)