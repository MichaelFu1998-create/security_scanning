def _execute(self, query, commit=False, working_columns=None):
        """ 
        Execute a query with provided parameters 

        Parameters
        :query:     SQL string with parameter placeholders
        :commit:    If True, the query will commit
        :returns:   List of rows
        """

        log.debug("RawlBase._execute()")

        result = []

        if working_columns is None:
            working_columns = self.columns

        with RawlConnection(self.dsn) as conn:

            query_id = random.randrange(9999)

            curs = conn.cursor()

            try:
                log.debug("Executing(%s): %s" % (query_id, query.as_string(curs)))
            except:
                log.exception("LOGGING EXCEPTION LOL")

            curs.execute(query)

            log.debug("Executed")

            if commit == True:
                log.debug("COMMIT(%s)" % query_id)
                conn.commit()
            
            log.debug("curs.rowcount: %s" % curs.rowcount)
            
            if curs.rowcount > 0:
                #result = curs.fetchall()
                # Process the results into a dict and stuff it in a RawlResult
                # object.  Then append that object to result
                result_rows = curs.fetchall()
                for row in result_rows:
                    
                    i = 0
                    row_dict = {}
                    for col in working_columns:
                        try:
                            #log.debug("row_dict[%s] = row[%s] which is %s" % (col, i, row[i]))
                            # For aliased columns, we need to get rid of the dot
                            col = col.replace('.', '_')
                            row_dict[col] = row[i]
                        except IndexError: pass
                        i += 1
                    
                    log.debug("Appending dict to result: %s" % row_dict)
                    
                    rr = RawlResult(working_columns, row_dict)
                    result.append(rr)
            
            curs.close()

        return result