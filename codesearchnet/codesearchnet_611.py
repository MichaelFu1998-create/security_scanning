def Vgg19(rgb):
    """
    Build the VGG 19 Model

    Parameters
    -----------
    rgb : rgb image placeholder [batch, height, width, 3] values scaled [0, 1]
    """
    start_time = time.time()
    print("build model started")
    rgb_scaled = rgb * 255.0
    # Convert RGB to BGR
    red, green, blue = tf.split(rgb_scaled, 3, 3)

    if red.get_shape().as_list()[1:] != [224, 224, 1]:
        raise Exception("image size unmatch")

    if green.get_shape().as_list()[1:] != [224, 224, 1]:
        raise Exception("image size unmatch")

    if blue.get_shape().as_list()[1:] != [224, 224, 1]:
        raise Exception("image size unmatch")

    bgr = tf.concat([
        blue - VGG_MEAN[0],
        green - VGG_MEAN[1],
        red - VGG_MEAN[2],
    ], axis=3)

    if bgr.get_shape().as_list()[1:] != [224, 224, 3]:
        raise Exception("image size unmatch")
    # input layer
    net_in = InputLayer(bgr, name='input')
    # conv1
    net = Conv2dLayer(net_in, act=tf.nn.relu, shape=[3, 3, 3, 64], strides=[1, 1, 1, 1], padding='SAME', name='conv1_1')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 64, 64], strides=[1, 1, 1, 1], padding='SAME', name='conv1_2')
    net = PoolLayer(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', pool=tf.nn.max_pool, name='pool1')
    # conv2
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 64, 128], strides=[1, 1, 1, 1], padding='SAME', name='conv2_1')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 128, 128], strides=[1, 1, 1, 1], padding='SAME', name='conv2_2')
    net = PoolLayer(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', pool=tf.nn.max_pool, name='pool2')
    # conv3
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 128, 256], strides=[1, 1, 1, 1], padding='SAME', name='conv3_1')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 256, 256], strides=[1, 1, 1, 1], padding='SAME', name='conv3_2')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 256, 256], strides=[1, 1, 1, 1], padding='SAME', name='conv3_3')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 256, 256], strides=[1, 1, 1, 1], padding='SAME', name='conv3_4')
    net = PoolLayer(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', pool=tf.nn.max_pool, name='pool3')
    # conv4
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 256, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv4_1')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv4_2')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv4_3')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv4_4')
    net = PoolLayer(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', pool=tf.nn.max_pool, name='pool4')
    # conv5
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv5_1')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv5_2')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv5_3')
    net = Conv2dLayer(net, act=tf.nn.relu, shape=[3, 3, 512, 512], strides=[1, 1, 1, 1], padding='SAME', name='conv5_4')
    net = PoolLayer(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', pool=tf.nn.max_pool, name='pool5')
    # fc 6~8
    net = FlattenLayer(net, name='flatten')
    net = DenseLayer(net, n_units=4096, act=tf.nn.relu, name='fc6')
    net = DenseLayer(net, n_units=4096, act=tf.nn.relu, name='fc7')
    net = DenseLayer(net, n_units=1000, act=None, name='fc8')
    print("build model finished: %fs" % (time.time() - start_time))
    return net