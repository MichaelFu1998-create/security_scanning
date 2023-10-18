def roi_pooling(input, rois, pool_height, pool_width):
    """
      returns a tensorflow operation for computing the Region of Interest Pooling
    
      @arg input: feature maps on which to perform the pooling operation
      @arg rois: list of regions of interest in the format (feature map index, upper left, bottom right)
      @arg pool_width: size of the pooling sections
    """
    # TODO(maciek): ops scope
    out = roi_pooling_module.roi_pooling(input, rois, pool_height=pool_height, pool_width=pool_width)
    output, argmax_output = out[0], out[1]
    return output