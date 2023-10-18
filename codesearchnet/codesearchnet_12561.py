def order(self, image_catalog_ids, batch_size=100, callback=None):
        '''Orders images from GBDX.

           Args:
               image_catalog_ids (str or list): A single catalog id or a list of 
                                                catalog ids.
               batch_size (int): The image_catalog_ids will be split into 
                                 batches of batch_size. The ordering API max 
                                 batch size is 100, if batch_size is greater 
                                 than 100 it will be truncated.
               callback (str): A url to call when ordering is completed.

           Returns:
               order_ids (str or list): If one batch, returns a string. If more
                                        than one batch, returns a list of order ids, 
                                        one for each batch.
        '''
        def _order_single_batch(url_, ids, results_list):
            data = json.dumps(ids) if callback is None else json.dumps({"acquisitionIds": ids, "callback": callback})
            r = self.gbdx_connection.post(url_, data=data)
            r.raise_for_status()
            order_id = r.json().get("order_id")
            if order_id:
                results_list.append(order_id)

        self.logger.debug('Place order')
        url = ('%s/order' if callback is None else '%s/ordercb') % self.base_url

        batch_size = min(100, batch_size)
        
        if not isinstance(image_catalog_ids, list):
            image_catalog_ids = [image_catalog_ids]

        sanitized_ids = list(set((id for id in (_id.strip() for _id in image_catalog_ids) if id)))

        res = []
        # Use itertool batch recipe
        acq_ids_by_batch = zip(*([iter(sanitized_ids)] * batch_size))
        for ids_batch in acq_ids_by_batch:
            _order_single_batch(url, ids_batch, res)

        # Order reminder
        remain_count = len(sanitized_ids) % batch_size
        if remain_count > 0:
            _order_single_batch(url, sanitized_ids[-remain_count:], res)

        if len(res) == 1:
            return res[0]
        elif len(res)>1:
            return res