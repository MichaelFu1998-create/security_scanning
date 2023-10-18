def refresh(self, accept=MEDIA_TYPE_TAXII_V20):
        """Update the API Root's information and list of Collections"""
        self.refresh_information(accept)
        self.refresh_collections(accept)