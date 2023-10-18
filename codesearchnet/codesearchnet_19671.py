def create_message(self, level, msg_text, extra_tags='', date=None, url=None):
        """
        Message instances are namedtuples of type `Message`.
        The date field is already serialized in datetime.isoformat ECMA-262 format
        """
        if not date:
            now = timezone.now()
        else:
            now = date
        r = now.isoformat()
        if now.microsecond:
            r = r[:23] + r[26:]
        if r.endswith('+00:00'):
            r = r[:-6] + 'Z'

        fingerprint = r + msg_text

        msg_id = hashlib.sha256(fingerprint.encode('ascii', 'ignore')).hexdigest()
        return Message(id=msg_id, message=msg_text, level=level, tags=extra_tags, date=r, url=url)