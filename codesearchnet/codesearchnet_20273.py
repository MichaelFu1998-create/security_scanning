def save(self):
        """Saves this invoice to Holvi, returns the created/updated invoice"""
        if not self.items:
            raise HolviError("No items")
        if not self.subject:
            raise HolviError("No subject")
        send_json = self.to_holvi_dict()
        if self.code:
            url = str(self.api.base_url + '{code}/').format(code=self.code)
            if not self.code:
                send_patch = {k: v for (k, v) in send_json.items() if k in self._patch_valid_keys}
                send_patch["items"] = []
                for item in self.items:
                    send_patch["items"].append(item.to_holvi_dict(True))
                stat = self.api.connection.make_patch(url, send_patch)
            else:
                stat = self.api.connection.make_put(url, send_json)
            return Invoice(self.api, stat)
        else:
            url = str(self.api.base_url)
            stat = self.api.connection.make_post(url, send_json)
            return Invoice(self.api, stat)