def load_package(self):
        """FInd the effect package"""
        try:
            self.package = importlib.import_module(self.name)
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Effect package '{}' not found.".format(self.name))