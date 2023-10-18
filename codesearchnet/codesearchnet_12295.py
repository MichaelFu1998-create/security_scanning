def delete_spot_fleet_cluster(
        spot_fleet_reqid,
        client=None,
):
    """
    This deletes a spot-fleet cluster.

    Parameters
    ----------

    spot_fleet_reqid : str
        The fleet request ID returned by `make_spot_fleet_cluster`.

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

    resp = client.cancel_spot_fleet_requests(
        SpotFleetRequestIds=[spot_fleet_reqid],
        TerminateInstances=True
    )

    return resp