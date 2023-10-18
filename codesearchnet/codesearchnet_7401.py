def dump(self, itemkey, filename=None, path=None):
        """
        Dump a file attachment to disk, with optional filename and path
        """
        if not filename:
            filename = self.item(itemkey)["data"]["filename"]
        if path:
            pth = os.path.join(path, filename)
        else:
            pth = filename
        file = self.file(itemkey)
        if self.snapshot:
            self.snapshot = False
            pth = pth + ".zip"
        with open(pth, "wb") as f:
            f.write(file)