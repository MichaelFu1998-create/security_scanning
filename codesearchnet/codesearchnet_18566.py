def get_dict(self):
        '''
        Convert Paginator instance to dict

        :return: Paging data
        :rtype: dict
        '''

        return dict(
            current_page=self.current_page,
            total_page_count=self.total_page_count,
            items=self.items,
            total_item_count=self.total_item_count,
            page_size=self.page_size
        )