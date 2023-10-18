def handle_add_fun(self, function_name):
        """Add a function to the function list, in order."""
        function_name = function_name.strip()
        try:
            function = get_function(function_name)
        except Exception, exc:
            self.wfile.write(js_error(exc) + NEWLINE)
            return
        # This tests to see if the function has been decorated with the view
        # server synchronisation decorator (``decorate_view``).
        if not getattr(function, 'view_decorated', None):
            self.functions[function_name] = (self.function_counter, function)
        # The decorator gets called with the logger function.
        else:
            self.functions[function_name] = (self.function_counter,
                function(self.log))
        self.function_counter += 1
        return True