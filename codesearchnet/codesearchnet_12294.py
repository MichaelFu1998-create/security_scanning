def make_spot_fleet_cluster(
        security_groupid,
        subnet_id,
        keypair_name,
        iam_instance_profile_arn,
        spot_fleet_iam_role,
        target_capacity=20,
        spot_price=0.4,
        expires_days=7,
        allocation_strategy='lowestPrice',
        instance_types=SPOT_INSTANCE_TYPES,
        instance_weights=None,
        instance_ami='ami-04681a1dbd79675a5',
        instance_user_data=None,
        instance_ebs_optimized=True,
        wait_until_up=True,
        client=None,
        raiseonfail=False
):
    """This makes an EC2 spot-fleet cluster.

    This requires a security group ID attached to a VPC config and subnet, a
    keypair generated beforehand, and an IAM role ARN for the instance. See:

    https://docs.aws.amazon.com/cli/latest/userguide/tutorial-ec2-ubuntu.html

    Use `user_data` to launch tasks on instance launch.

    Parameters
    ----------

    security_groupid : str
        The security group ID of the AWS VPC where the instances will be
        launched.

    subnet_id : str
        The subnet ID of the AWS VPC where the instances will be
        launched.

    keypair_name : str
        The name of the keypair to be used to allow SSH access to all instances
        launched here. This corresponds to an already downloaded AWS keypair PEM
        file.

    iam_instance_profile_arn : str
        The ARN string corresponding to the AWS instance profile that describes
        the permissions the launched instances have to access other AWS
        resources. Set this up in AWS IAM.

    spot_fleet_iam_role : str
        This is the name of AWS IAM role that allows the Spot Fleet Manager to
        scale up and down instances based on demand and instances failing,
        etc. Set this up in IAM.

    target_capacity : int
        The number of instances to target in the fleet request. The fleet
        manager service will attempt to maintain this number over the lifetime
        of the Spot Fleet Request.

    spot_price : float
        The bid price in USD for the instances. This is per hour. Keep this at
        about half the hourly on-demand price of the desired instances to make
        sure your instances aren't taken away by AWS when it needs capacity.

    expires_days : int
        The number of days this request is active for. All instances launched by
        this request will live at least this long and will be terminated
        automatically after.

    allocation_strategy : {'lowestPrice', 'diversified'}
        The allocation strategy used by the fleet manager.

    instance_types : list of str
        List of the instance type to launch. See the following URL for a list of
        IDs: https://aws.amazon.com/ec2/pricing/on-demand/

    instance_weights : list of float or None
        If `instance_types` is a list of different instance types, this is the
        relative weight applied towards launching each instance type. This can
        be used to launch a mix of instances in a defined ratio among their
        types. Doing this can make the spot fleet more resilient to AWS taking
        back the instances if it runs out of capacity.

    instance_ami : str
        The Amazon Machine Image ID that describes the OS the instances will use
        after launch. The default ID is Amazon Linux 2 in the US East region.

    instance_user_data : str or None
        This is either the path to a file on disk that contains a shell-script
        or a string containing a shell-script that will be executed by root
        right after the instance is launched. Use to automatically set up
        workers and queues. If None, will not execute anything at instance
        start up.

    instance_ebs_optimized : bool
        If True, will enable EBS optimization to speed up IO. This is usually
        True for all instances made available in the last couple of years.

    wait_until_up : bool
        If True, will not return from this function until the spot fleet request
        is acknowledged by AWS.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    str or None
        This is the spot fleet request ID if successful. Otherwise, returns
        None.

    """

    fleetconfig = copy.deepcopy(SPOT_FLEET_CONFIG)
    fleetconfig['IamFleetRole'] = spot_fleet_iam_role
    fleetconfig['AllocationStrategy'] = allocation_strategy
    fleetconfig['TargetCapacity'] = target_capacity
    fleetconfig['SpotPrice'] = str(spot_price)
    fleetconfig['ValidUntil'] = (
        datetime.utcnow() + timedelta(days=expires_days)
    ).strftime(
        '%Y-%m-%dT%H:%M:%SZ'
    )

    # get the user data from a string or a file
    # we need to base64 encode it here
    if (isinstance(instance_user_data, str) and
        os.path.exists(instance_user_data)):
        with open(instance_user_data,'rb') as infd:
            udata = base64.b64encode(infd.read()).decode()

    elif isinstance(instance_user_data, str):
        udata = base64.b64encode(instance_user_data.encode()).decode()

    else:
        udata = (
            '#!/bin/bash\necho "No user data provided. '
            'Launched instance at: %s UTC"' % datetime.utcnow().isoformat()
        )
        udata = base64.b64encode(udata.encode()).decode()


    for ind, itype in enumerate(instance_types):

        thisinstance = SPOT_PERINSTANCE_CONFIG.copy()
        thisinstance['InstanceType'] = itype
        thisinstance['ImageId'] = instance_ami
        thisinstance['SubnetId'] = subnet_id
        thisinstance['KeyName'] = keypair_name
        thisinstance['IamInstanceProfile']['Arn'] = iam_instance_profile_arn
        thisinstance['SecurityGroups'][0] = {'GroupId':security_groupid}
        thisinstance['UserData'] = udata
        thisinstance['EbsOptimized'] = instance_ebs_optimized

        # get the instance weights
        if isinstance(instance_weights, list):
            thisinstance['WeightedCapacity'] = instance_weights[ind]

        fleetconfig['LaunchSpecifications'].append(thisinstance)

    #
    # launch the fleet
    #

    if not client:
        client = boto3.client('ec2')

    try:

        resp = client.request_spot_fleet(
            SpotFleetRequestConfig=fleetconfig,
        )

        if not resp:

            LOGERROR('spot fleet request failed.')
            return None

        else:

            spot_fleet_reqid = resp['SpotFleetRequestId']
            LOGINFO('spot fleet requested successfully. request ID: %s' %
                    spot_fleet_reqid)

            if not wait_until_up:
                return spot_fleet_reqid

            else:

                ntries = 10
                curr_try = 0

                while curr_try < ntries:

                    resp = client.describe_spot_fleet_requests(
                        SpotFleetRequestIds=[
                            spot_fleet_reqid
                        ]
                    )

                    curr_state = resp.get('SpotFleetRequestConfigs',[])

                    if len(curr_state) > 0:

                        curr_state = curr_state[0]['SpotFleetRequestState']

                        if curr_state == 'active':
                            LOGINFO('spot fleet with reqid: %s is now active' %
                                    spot_fleet_reqid)
                            break

                    LOGINFO(
                        'spot fleet not yet active, waiting 15 seconds. '
                        'try %s/%s' % (curr_try, ntries)
                    )
                    curr_try = curr_try + 1
                    time.sleep(15.0)

                return spot_fleet_reqid


    except ClientError as e:

        LOGEXCEPTION('could not launch spot fleet')
        if raiseonfail:
            raise

        return None

    except Exception as e:

        LOGEXCEPTION('could not launch spot fleet')
        if raiseonfail:
            raise

        return None