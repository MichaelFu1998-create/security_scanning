def validate(self):
        """
        Check if the file still has its original contents.

        Returns True if the file is unchanged, False if it has been tampered
        with.
        """

        with open(self.filename, "rb") as f:
            text = f.read()

        start_last_line = text.rfind(b"\n", 0, -1)
        if start_last_line == -1:
            return False

        original_text = text[:start_last_line+1]
        last_line = text[start_last_line+1:]

        expected_hash = hashlib.sha1(original_text).hexdigest().encode('utf8')
        match = re.search(b"[0-9a-f]{40}", last_line)
        if not match:
            return False
        actual_hash = match.group(0)
        return actual_hash == expected_hash