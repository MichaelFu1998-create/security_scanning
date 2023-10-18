def render_asset(self, name):
        """
        Render all includes in asset by names

        :type name: str|unicode
        :rtype: str|unicode
        """
        result = ""
        if self.has_asset(name):
            asset = self.get_asset(name)
            if asset.files:
                for f in asset.files:
                    result += f.render_include() + "\r\n"
        return result