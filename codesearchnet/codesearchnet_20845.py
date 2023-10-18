def get_pub_date(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_date` record is not found.

        Returns:
            str: Date of publication (month and year usually) or `undefined` \
                 if `pub_date` is not found.
        """
        dates = self["260c  "] + self["264c"]

        def clean_date(date):
            """
            Clean the `date` strings from special characters, but leave
            sequences of numbers followed by -.

            So:
                [2015]- -> 2015
                2015- -> 2015-
            """
            out = ""
            was_digit = False
            for c in date:
                if c.isdigit() or (c == "-" and was_digit) or c == " ":
                    out += c

                was_digit = c.isdigit()

            return out

        # clean all the date strings
        dates = set([
            clean_date(date)
            for date in self["260c  "] + self["264c"]
        ])

        return _undefined_pattern(
            ", ".join(dates),
            lambda x: x.strip() == "",
            undefined
        )