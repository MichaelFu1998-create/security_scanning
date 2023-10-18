def phrase_to_filename(self, phrase):
        """Convert phrase to normilized file name."""
        # remove non-word characters
        name = re.sub(r"[^\w\s\.]", '', phrase.strip().lower())
        # replace whitespace with underscores
        name = re.sub(r"\s+", '_', name)

        return name + '.png'