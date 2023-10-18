def get_response_page(self):
        """Return a tuple (content-type, response page)."""
        # If it has pre- or post-condition: return as XML response
        if self.err_condition:
            return ("application/xml", compat.to_bytes(self.err_condition.as_string()))

        # Else return as HTML
        status = get_http_status_string(self)
        html = []
        html.append(
            "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01//EN' "
            "'http://www.w3.org/TR/html4/strict.dtd'>"
        )
        html.append("<html><head>")
        html.append(
            "  <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>"
        )
        html.append("  <title>{}</title>".format(status))
        html.append("</head><body>")
        html.append("  <h1>{}</h1>".format(status))
        html.append("  <p>{}</p>".format(compat.html_escape(self.get_user_info())))
        html.append("<hr/>")
        html.append(
            "<a href='https://github.com/mar10/wsgidav/'>WsgiDAV/{}</a> - {}".format(
                __version__, compat.html_escape(str(datetime.datetime.now()), "utf-8")
            )
        )
        html.append("</body></html>")
        html = "\n".join(html)
        return ("text/html", compat.to_bytes(html))