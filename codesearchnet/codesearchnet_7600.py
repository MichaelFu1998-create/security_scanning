def add_markdown_cell(self, text):
        """Add a markdown cell to the notebook

        Parameters
        ----------
        code : str
            Cell content
        """
        markdown_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [rst2md(text)]
        }
        self.work_notebook["cells"].append(markdown_cell)