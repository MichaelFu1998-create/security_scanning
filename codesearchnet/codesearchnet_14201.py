def parse_tables(self, markup):
        
        """ Returns a list of tables in the markup.

        A Wikipedia table looks like:
        {| border="1"
        |-
        |Cell 1 (no modifier - not aligned)
        |-
        |align="right" |Cell 2 (right aligned)
        |-
        |}

        """

        tables = []
        m = re.findall(self.re["table"], markup)
        for chunk in m:

            table = WikipediaTable()
            table.properties = chunk.split("\n")[0].strip("{|").strip()
            self.connect_table(table, chunk, markup)
                  
            # Tables start with "{|".
            # On the same line can be properties, e.g. {| border="1"
            # The table heading starts with "|+".
            # A new row in the table starts with "|-".
            # The end of the table is marked with "|}".            
            row = None
            for chunk in chunk.split("\n"):
                chunk = chunk.strip()
                if chunk.startswith("|+"):
                    title = self.plain(chunk.strip("|+"))
                    table.title = title
                elif chunk.startswith("|-"):
                    if row: 
                        row.properties = chunk.strip("|-").strip()
                        table.append(row)
                    row = None
                elif chunk.startswith("|}"):
                    pass
                elif chunk.startswith("|") \
                  or chunk.startswith("!"):
                    row = self.parse_table_row(chunk, row)
                        
            # Append the last row.
            if row: table.append(row)
            if len(table) > 0:
                tables.append(table)
        
        return tables