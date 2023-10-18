def delete_ec2_nodes(
        instance_id_list,
        client=None
):
    """This deletes EC2 nodes and terminates the instances.

    Parameters
    ----------

    instance_id_list : list of str
        A list of EC2 instance IDs to terminate.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    Returns
    -------

    Nothing.

    """

    if not client:
        client = boto3.client('ec2')

    resp = client.terminate_instances(
        InstanceIds=instance_id_list
    )

    return resp