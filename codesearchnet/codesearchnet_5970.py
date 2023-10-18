def get_image(image_id, flags=FLAGS.ALL, **conn):
    """
    Orchestrates all the calls required to fully build out an EC2 Image (AMI, AKI, ARI)

    {
        "Architecture": "x86_64", 
        "Arn": "arn:aws:ec2:us-east-1::image/ami-11111111", 
        "BlockDeviceMappings": [], 
        "CreationDate": "2013-07-11T16:04:06.000Z", 
        "Description": "...", 
        "Hypervisor": "xen", 
        "ImageId": "ami-11111111", 
        "ImageLocation": "111111111111/...", 
        "ImageType": "machine", 
        "KernelId": "aki-88888888", 
        "LaunchPermissions": [], 
        "Name": "...", 
        "OwnerId": "111111111111", 
        "ProductCodes": [], 
        "Public": false, 
        "RamdiskId": {}, 
        "RootDeviceName": "/dev/sda1", 
        "RootDeviceType": "ebs", 
        "SriovNetSupport": "simple",
        "State": "available", 
        "Tags": [], 
        "VirtualizationType": "hvm", 
        "_version": 1
    }

    :param image_id: str ami id
    :param flags: By default, set to ALL fields
    :param conn: dict containing enough information to make a connection to the desired account.
    Must at least have 'assume_role' key.
    :return: dict containing a fully built out image.
    """
    image = dict(ImageId=image_id)
    conn['region'] = conn.get('region', 'us-east-1')
    return registry.build_out(flags, image, **conn)