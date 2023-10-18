def serve(self, port=62000):
        """ Start LanguageBoard web application

        Parameters
        ----------
        port: int
            port to serve web application
        """

        from http.server import HTTPServer, CGIHTTPRequestHandler
        os.chdir(self.log_folder)

        httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
        print("Starting LanguageBoard on port: " + str(httpd.server_port))
        webbrowser.open('http://0.0.0.0:{}'.format(port))
        httpd.serve_forever()