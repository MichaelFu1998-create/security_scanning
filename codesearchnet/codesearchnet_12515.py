def materialize(self, node=None, bounds=None, callback=None, out_format='TILE_STREAM', **kwargs):
        """
          Materializes images into gbdx user buckets in s3.
          Note: This method is only available to RDA based image classes. 

          Args:
            node (str): the node in the graph to materialize
            bounds (list): optional bbox for cropping what gets materialized in s3
            out_format (str): VECTOR_TILE, VECTOR, TIF, TILE_STREAM
            callback (str): a callback url like an `sns://`
          Returns:
            job_id (str): the job_id of the materialization 
        """
        kwargs.update({
          "node": node,
          "bounds": bounds,
          "callback": callback,
          "out_format": out_format
        })
        return self.rda._materialize(**kwargs)