def slinky(filename, seconds_available, bucket_name, aws_key, aws_secret):
    """Simple program that creates an temp S3 link."""
    if not os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
    	print 'Need to set environment variables for AWS access and create a slinky bucket.'
    	exit()
    
    print create_temp_s3_link(filename, seconds_available, bucket_name)