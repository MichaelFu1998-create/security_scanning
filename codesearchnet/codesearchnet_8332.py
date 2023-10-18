def json(self):
        """
        return {
            "base": self["base"].json(),
            "quote": self["quote"].json()
        }
        """
        quote = self["quote"]
        base = self["base"]
        frac = Fraction(int(quote) / int(base)).limit_denominator(
            10 ** base["asset"]["precision"]
        )
        return {
            "base": {"amount": int(frac.denominator), "asset_id": base["asset"]["id"]},
            "quote": {"amount": int(frac.numerator), "asset_id": quote["asset"]["id"]},
        }