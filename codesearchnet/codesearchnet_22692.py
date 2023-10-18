def curl(self, url, post):
        """
        Inteface for sending web requests to the AmbientSMS API Server
        """
        try:
            req = urllib2.Request(url)
            req.add_header("Content-type", "application/xml")
            data = urllib2.urlopen(req, post.encode('utf-8')).read()
        except urllib2.URLError, v:
            raise AmbientSMSError(v)
        return dictFromXml(data)