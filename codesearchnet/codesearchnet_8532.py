def train_model(best_processed_path, weight_path='../weight/model_weight.h5', verbose=2):
    """
    Given path to processed BEST dataset,
    train CNN model for words beginning alongside with
    character label encoder and character type label encoder

    Input
    =====
    best_processed_path: str, path to processed BEST dataset
    weight_path: str, path to weight path file
    verbose: int, verbost option for training Keras model

    Output
    ======
    model: keras model, keras model for tokenize prediction
    """

    x_train_char, x_train_type, y_train = prepare_feature(best_processed_path, option='train')
    x_test_char, x_test_type, y_test = prepare_feature(best_processed_path, option='test')

    validation_set = False
    if os.path.isdir(os.path.join(best_processed_path, 'val')):
        validation_set = True
        x_val_char, x_val_type, y_val = prepare_feature(best_processed_path, option='val')

    if not os.path.isdir(os.path.dirname(weight_path)):
        os.makedirs(os.path.dirname(weight_path)) # make directory if weight does not exist

    callbacks_list = [
        ReduceLROnPlateau(),
        ModelCheckpoint(
            weight_path,
            save_best_only=True,
            save_weights_only=True,
            monitor='val_loss',
            mode='min',
            verbose=1
        )
    ]

    # train model
    model = get_convo_nn2()
    train_params = [(10, 256), (3, 512), (3, 2048), (3, 4096), (3, 8192)]
    for (epochs, batch_size) in train_params:
        print("train with {} epochs and {} batch size".format(epochs, batch_size))
        if validation_set:
            model.fit([x_train_char, x_train_type], y_train,
                      epochs=epochs, batch_size=batch_size,
                      verbose=verbose,
                      callbacks=callbacks_list,
                      validation_data=([x_val_char, x_val_type], y_val))
        else:
            model.fit([x_train_char, x_train_type], y_train,
                      epochs=epochs, batch_size=batch_size,
                      verbose=verbose,
                      callbacks=callbacks_list)
    return model