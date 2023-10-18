def write(self, text, hashline=b"# {}"):
        u"""
        Write `text` to the file.

        Writes the text to the file, with a final line checksumming the
        contents.  The entire file must be written with one `.write()` call.

        The last line is written with the `hashline` format string, which can
        be changed to accommodate different file syntaxes.

        Both arguments are UTF8 byte strings.

        Arguments:
            text (UTF8 byte string): the contents of the file to write.

            hashline (UTF8 byte string): the format of the last line to append
                to the file, with "{}" replaced with the hash.

        """
        if not text.endswith(b"\n"):
            text += b"\n"

        actual_hash = hashlib.sha1(text).hexdigest()

        with open(self.filename, "wb") as f:
            f.write(text)
            f.write(hashline.decode("utf8").format(actual_hash).encode("utf8"))
            f.write(b"\n")