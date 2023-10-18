def present_results(self, query_text, n=10):
        "Get results for the query and present them."
        self.present(self.query(query_text, n))