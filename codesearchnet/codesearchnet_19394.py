def index_collection(self, filenames):
        "Index a whole collection of files."
        for filename in filenames:
            self.index_document(open(filename).read(), filename)