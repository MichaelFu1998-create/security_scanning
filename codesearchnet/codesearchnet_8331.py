def invert(self):
        """ Invert the price (e.g. go from ``USD/BTS`` into ``BTS/USD``)
        """
        tmp = self["quote"]
        self["quote"] = self["base"]
        self["base"] = tmp
        if "for_sale" in self and self["for_sale"]:
            self["for_sale"] = self.amount_class(
                self["for_sale"]["amount"] * self["price"], self["base"]["symbol"]
            )
        return self