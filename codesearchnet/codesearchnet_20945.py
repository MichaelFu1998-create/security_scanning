def styles(self):
        """Get a dictionary of CSL styles."""
        styles = get_all_styles()
        whitelist = self.app.config.get('CSL_STYLES_WHITELIST')
        if whitelist:
            return {k: v for k, v in styles.items() if k in whitelist}
        return styles