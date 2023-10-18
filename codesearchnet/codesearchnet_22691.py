def sendmsg(self,
                message,
                recipient_mobiles=[],
                url='http://services.ambientmobile.co.za/sms',
                concatenate_message=True,
                message_id=str(time()).replace(".", ""),
                reply_path=None,
                allow_duplicates=True,
                allow_invalid_numbers=True,
                ):

        """
        Send a mesage via the AmbientSMS API server
        """
        if not recipient_mobiles or not(isinstance(recipient_mobiles, list) \
                or isinstance(recipient_mobiles, tuple)):
            raise AmbientSMSError("Missing recipients")

        if not message or not len(message):
            raise AmbientSMSError("Missing message")

        postXMLList = []
        postXMLList.append("<api-key>%s</api-key>" % self.api_key)
        postXMLList.append("<password>%s</password>" % self.password)
        postXMLList.append("<recipients>%s</recipients>" % \
                "".join(["<mobile>%s</mobile>" % \
                m for m in recipient_mobiles]))
        postXMLList.append("<msg>%s</msg>" % message)
        postXMLList.append("<concat>%s</concat>" % \
                (1 if concatenate_message else 0))
        postXMLList.append("<message_id>%s</message_id>" % message_id)
        postXMLList.append("<allow_duplicates>%s</allow_duplicates>" % \
                (1 if allow_duplicates else 0))
        postXMLList.append(
            "<allow_invalid_numbers>%s</allow_invalid_numbers>" % \
                    (1 if allow_invalid_numbers else 0)
        )
        if reply_path:
            postXMLList.append("<reply_path>%s</reply_path>" % reply_path)

        postXML = '<sms>%s</sms>' % "".join(postXMLList)
        result = self.curl(url, postXML)

        status = result.get("status", None)
        if status and int(status) in [0, 1, 2]:
            return result
        else:
            raise AmbientSMSError(int(status))