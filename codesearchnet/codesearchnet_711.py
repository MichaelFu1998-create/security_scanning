def freeze_graph(graph_path, checkpoint_path, output_path, end_node_names, is_binary_graph):
    """Reimplementation of the TensorFlow official freeze_graph function to freeze the graph and checkpoint together:

    Parameters
    -----------
    graph_path : string
        the path where your graph file save.
    checkpoint_output_path : string
        the path where your checkpoint save.
    output_path : string
        the path where you want to save the output proto buff
    end_node_names : string
        the name of the end node in your graph you want to get in your proto buff
    is_binary_graph : boolean
        declare your file whether is a binary graph

    References
    ----------
    - `onnx-tf exporting tutorial <https://github.com/onnx/tutorials/blob/master/tutorials/OnnxTensorflowExport.ipynb>`__
    - `tensorflow freeze_graph <https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/tools/freeze_graph.py>`
    """
    _freeze_graph(
        input_graph=graph_path, input_saver='', input_binary=is_binary_graph, input_checkpoint=checkpoint_path,
        output_graph=output_path, output_node_names=end_node_names, restore_op_name='save/restore_all',
        filename_tensor_name='save/Const:0', clear_devices=True, initializer_nodes=None
    )