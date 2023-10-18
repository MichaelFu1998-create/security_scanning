def example1():
    """ Example 1: Applying transformation one-by-one is very SLOW ! """
    st = time.time()
    for _ in range(100):  # Try 100 times and compute the averaged speed
        xx = tl.prepro.rotation(image, rg=-20, is_random=False)
        xx = tl.prepro.flip_axis(xx, axis=1, is_random=False)
        xx = tl.prepro.shear2(xx, shear=(0., -0.2), is_random=False)
        xx = tl.prepro.zoom(xx, zoom_range=1 / 0.8)
        xx = tl.prepro.shift(xx, wrg=-0.1, hrg=0, is_random=False)
    print("apply transforms one-by-one took %fs for each image" % ((time.time() - st) / 100))
    tl.vis.save_image(xx, '_result_slow.png')