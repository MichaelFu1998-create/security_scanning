def full_analysis(self):
        """Execute the count and verify_words methods."""
        self.count()
        self.verify_words()
        self.verify_user()

        if self.review_requested == 'yes':
            self.label_suspicious('Review requested')