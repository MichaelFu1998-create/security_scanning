def strftime(self, fmt="%d:%H:%M:%S"):
        """Primitive string formatter.

        The only directives understood are the following:
          ============   ==========================
          Directive      meaning
          ============   ==========================
          %d             day as integer
          %H             hour  [00-23]
          %h             hours including days
          %M             minute as integer [00-59]
          %S             second as integer [00-59]
          ============   ==========================
        """
        substitutions = {
            "%d": str(self.days),
            "%H": "{0:02d}".format(self.dhours),
            "%h": str(24*self.days + self.dhours),
            "%M": "{0:02d}".format(self.dminutes),
            "%S": "{0:02d}".format(self.dseconds),
            }
        s = fmt
        for search, replacement in substitutions.items():
            s = s.replace(search, replacement)
        return s