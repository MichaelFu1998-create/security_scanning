def convert_onnx_to_model(onnx_input_path):
    """Reimplementation of the TensorFlow-onnx official tutorial convert the onnx file to specific: model

    Parameters
    -----------
    onnx_input_path : string
    the path where you save the onnx file.

    References
    -----------
    - `onnx-tf exporting tutorial <https://github.com/onnx/tutorials/blob/master/tutorials/OnnxTensorflowExport.ipynb>`__
    """
    model = onnx.load(onnx_input_path)
    tf_rep = prepare(model)
    # Image Path
    img = np.load("./assets/image.npz")
    output = tf_rep.run(img.reshape([1, 784]))
    print("The digit is classified as ", np.argmax(output))