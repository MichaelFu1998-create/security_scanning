def convert_model_to_onnx(frozen_graph_path, end_node_names, onnx_output_path):
    """Reimplementation of the TensorFlow-onnx official tutorial convert the proto buff to onnx file:

    Parameters
    -----------
    frozen_graph_path : string
        the path where your frozen graph file save.
    end_node_names : string
        the name of the end node in your graph you want to get in your proto buff
    onnx_output_path : string
        the path where you want to save the onnx file.

    References
    -----------
    - `onnx-tf exporting tutorial <https://github.com/onnx/tutorials/blob/master/tutorials/OnnxTensorflowExport.ipynb>`
    """
    with tf.gfile.GFile(frozen_graph_path, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        onnx_model = tensorflow_graph_to_onnx_model(graph_def, end_node_names, opset=6)
        file = open(onnx_output_path, "wb")
        file.write(onnx_model.SerializeToString())
        file.close()