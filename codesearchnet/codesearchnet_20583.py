def spatial_map(icc, thr, mode='+'):
    """ Return the thresholded z-scored `icc`. """
    return thr_img(icc_img_to_zscore(icc), thr=thr, mode=mode).get_data()