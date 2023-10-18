def example2():
    """ Example 2: Applying all transforms in one is very FAST ! """
    st = time.time()
    for _ in range(100):  # Repeat 100 times and compute the averaged speed
        transform_matrix = create_transformation_matrix()
        result = tl.prepro.affine_transform_cv2(image, transform_matrix)  # Transform the image using a single operation
    print("apply all transforms once took %fs for each image" % ((time.time() - st) / 100))  # usually 50x faster
    tl.vis.save_image(result, '_result_fast.png')