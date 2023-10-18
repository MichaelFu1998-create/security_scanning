def _write_stop_to_stop_network_edges(net, file_name, data=True, fmt=None):
    """
    Write out a network

    Parameters
    ----------
    net: networkx.DiGraph
    base_name: str
        path to the filename (without extension)
    data: bool, optional
        whether or not to write out any edge data present
    fmt: str, optional
        If "csv" write out the network in csv format.
    """
    if fmt is None:
        fmt = "edg"

    if fmt == "edg":
        if data:
            networkx.write_edgelist(net, file_name, data=True)
        else:
            networkx.write_edgelist(net, file_name)
    elif fmt == "csv":
        with open(file_name, 'w') as f:
            # writing out the header
            edge_iter = net.edges_iter(data=True)
            _, _, edg_data = next(edge_iter)
            edg_data_keys = list(sorted(edg_data.keys()))
            header = ";".join(["from_stop_I", "to_stop_I"] + edg_data_keys)
            f.write(header)
            for from_node_I, to_node_I, data in net.edges_iter(data=True):
                f.write("\n")
                values = [str(from_node_I), str(to_node_I)]
                data_values = []
                for key in edg_data_keys:
                    if key == "route_I_counts":
                        route_I_counts_string = str(data[key]).replace(" ", "")[1:-1]
                        data_values.append(route_I_counts_string)
                    else:
                        data_values.append(str(data[key]))
                all_values = values + data_values
                f.write(";".join(all_values))