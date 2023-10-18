def make_ec2_nodes(
        security_groupid,
        subnet_id,
        keypair_name,
        iam_instance_profile_arn,
        launch_instances=1,
        ami='ami-04681a1dbd79675a5',
        instance='t3.micro',
        ebs_optimized=True,
        user_data=None,
        wait_until_up=True,
        client=None,
        raiseonfail=False,
):
    """This makes new EC2 worker nodes.

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

    launch_instances : int
        The number of instances to launch in this request.

    ami : str
        The Amazon Machine Image ID that describes the OS the instances will use
        after launch. The default ID is Amazon Linux 2 in the US East region.

    instance : str
        The instance type to launch. See the following URL for a list of IDs:
        https://aws.amazon.com/ec2/pricing/on-demand/

    ebs_optimized : bool
        If True, will enable EBS optimization to speed up IO. This is usually
        True for all instances made available in the last couple of years.

    user_data : str or None
        This is either the path to a file on disk that contains a shell-script
        or a string containing a shell-script that will be executed by root
        right after the instance is launched. Use to automatically set up
        workers and queues. If None, will not execute anything at instance
        start up.

    wait_until_up : bool
        If True, will not return from this function until all launched instances
        are verified as running by AWS.

    client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its operations. Alternatively, pass in an existing `boto3.Client`
        instance to re-use it here.

    raiseonfail : bool
        If True, will re-raise whatever Exception caused the operation to fail
        and break out immediately.

    Returns
    -------

    dict
        Returns launched instance info as a dict, keyed by instance ID.

    """

    if not client:
        client = boto3.client('ec2')

    # get the user data from a string or a file
    # note: boto3 will base64 encode this itself
    if isinstance(user_data, str) and os.path.exists(user_data):
        with open(user_data,'r') as infd:
            udata = infd.read()

    elif isinstance(user_data, str):
        udata = user_data

    else:
        udata = (
            '#!/bin/bash\necho "No user data provided. '
            'Launched instance at: %s UTC"' % datetime.utcnow().isoformat()
        )


    # fire the request
    try:
        resp = client.run_instances(
            ImageId=ami,
            InstanceType=instance,
            SecurityGroupIds=[
                security_groupid,
            ],
            SubnetId=subnet_id,
            UserData=udata,
            IamInstanceProfile={'Arn':iam_instance_profile_arn},
            InstanceInitiatedShutdownBehavior='terminate',
            KeyName=keypair_name,
            MaxCount=launch_instances,
            MinCount=launch_instances,
            EbsOptimized=ebs_optimized,
        )

        if not resp:
            LOGERROR('could not launch requested instance')
            return None

        else:

            instance_dict = {}

            instance_list = resp.get('Instances',[])

            if len(instance_list) > 0:

                for instance in instance_list:

                    LOGINFO('launched instance ID: %s of type: %s at: %s. '
                            'current state: %s'
                            % (instance['InstanceId'],
                               instance['InstanceType'],
                               instance['LaunchTime'].isoformat(),
                               instance['State']['Name']))

                    instance_dict[instance['InstanceId']] = {
                        'type':instance['InstanceType'],
                        'launched':instance['LaunchTime'],
                        'state':instance['State']['Name'],
                        'info':instance
                    }

            # if we're waiting until we're up, then do so
            if wait_until_up:

                ready_instances = []

                LOGINFO('waiting until launched instances are up...')

                ntries = 5
                curr_try = 0

                while ( (curr_try < ntries) or
                        ( len(ready_instances) <
                          len(list(instance_dict.keys()))) ):

                    resp = client.describe_instances(
                        InstanceIds=list(instance_dict.keys()),
                    )

                    if len(resp['Reservations']) > 0:
                        for resv in resp['Reservations']:
                            if len(resv['Instances']) > 0:
                                for instance in resv['Instances']:
                                    if instance['State']['Name'] == 'running':

                                        ready_instances.append(
                                            instance['InstanceId']
                                        )

                                        instance_dict[
                                            instance['InstanceId']
                                        ]['state'] = 'running'

                                        instance_dict[
                                            instance['InstanceId']
                                        ]['ip'] = instance['PublicIpAddress']

                                        instance_dict[
                                            instance['InstanceId']
                                        ]['info'] = instance

                    # sleep for a bit so we don't hit the API too often
                    curr_try = curr_try + 1
                    time.sleep(5.0)

                if len(ready_instances) == len(list(instance_dict.keys())):
                    LOGINFO('all instances now up.')
                else:
                    LOGWARNING(
                        'reached maximum number of tries for instance status, '
                        'not all instances may be up.'
                    )


            return instance_dict

    except ClientError as e:

        LOGEXCEPTION('could not launch requested instance')
        if raiseonfail:
            raise

        return None

    except Exception as e:

        LOGEXCEPTION('could not launch requested instance')
        if raiseonfail:
            raise

        return None