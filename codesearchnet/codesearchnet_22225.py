def repack(self):
        """Removes any blank ranks in the order."""
        items = self.grouped_filter().order_by('rank').select_for_update()
        for count, item in enumerate(items):
            item.rank = count + 1
            item.save(rerank=False)