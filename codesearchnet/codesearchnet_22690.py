def getbalance(self, url='http://services.ambientmobile.co.za/credits'):
        """
        Get the number of credits remaining at AmbientSMS
        """
        postXMLList = []
        postXMLList.append("<api-key>%s</api-key>" % self.api_key)
        postXMLList.append("<password>%s</password>" % self.password)
        postXML = '<sms>%s</sms>' % "".join(postXMLList)
        result = self.curl(url, postXML)

        if result.get("credits", None):
            return result["credits"]
        else:
            raise AmbientSMSError(result["status"])