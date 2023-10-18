def example3():
    """ Example 3: Using TF dataset API to load and process image for training """
    n_data = 100
    imgs_file_list = ['tiger.jpeg'] * n_data
    train_targets = [np.ones(1)] * n_data

    def generator():
        if len(imgs_file_list) != len(train_targets):
            raise RuntimeError('len(imgs_file_list) != len(train_targets)')
        for _input, _target in zip(imgs_file_list, train_targets):
            yield _input, _target

    def _data_aug_fn(image):
        transform_matrix = create_transformation_matrix()
        result = tl.prepro.affine_transform_cv2(image, transform_matrix)  # Transform the image using a single operation
        return result

    def _map_fn(image_path, target):
        image = tf.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)  # Get RGB with 0~1
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        image = tf.py_func(_data_aug_fn, [image], [tf.float32])
        # image = tf.reshape(image, (h, w, 3))
        target = tf.reshape(target, ())
        return image, target

    n_epoch = 10
    batch_size = 5
    dataset = tf.data.Dataset().from_generator(generator, output_types=(tf.string, tf.int64))
    dataset = dataset.shuffle(buffer_size=4096)  # shuffle before loading images
    dataset = dataset.repeat(n_epoch)
    dataset = dataset.map(_map_fn, num_parallel_calls=multiprocessing.cpu_count())
    dataset = dataset.batch(batch_size)  # TODO: consider using tf.contrib.map_and_batch
    dataset = dataset.prefetch(1)  # prefetch 1 batch
    iterator = dataset.make_one_shot_iterator()
    one_element = iterator.get_next()
    sess = tf.Session()
    # feed `one_element` into a network, for demo, we simply get the data as follows
    n_step = round(n_epoch * n_data / batch_size)
    st = time.time()
    for _ in range(n_step):
        _images, _targets = sess.run(one_element)
    print("dataset APIs took %fs for each image" % ((time.time() - st) / batch_size / n_step))