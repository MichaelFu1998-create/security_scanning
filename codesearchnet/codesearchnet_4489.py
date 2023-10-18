def create_session(self):
        """Create a session.

        First we look in self.key_file for a path to a json file with the
        credentials. The key file should have 'AWSAccessKeyId' and 'AWSSecretKey'.

        Next we look at self.profile for a profile name and try
        to use the Session call to automatically pick up the keys for the profile from
        the user default keys file ~/.aws/config.

        Finally, boto3 will look for the keys in environment variables:
        AWS_ACCESS_KEY_ID: The access key for your AWS account.
        AWS_SECRET_ACCESS_KEY: The secret key for your AWS account.
        AWS_SESSION_TOKEN: The session key for your AWS account.
        This is only needed when you are using temporary credentials.
        The AWS_SECURITY_TOKEN environment variable can also be used,
        but is only supported for backwards compatibility purposes.
        AWS_SESSION_TOKEN is supported by multiple AWS SDKs besides python.
        """

        session = None

        if self.key_file is not None:
            credfile = os.path.expandvars(os.path.expanduser(self.key_file))

            try:
                with open(credfile, 'r') as f:
                    creds = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(
                    "EC2Provider '{}': json decode error in credential file {}".format(self.label, credfile)
                )
                raise e

            except Exception as e:
                logger.debug(
                    "EC2Provider '{0}' caught exception while reading credential file: {1}".format(
                        self.label, credfile
                    )
                )
                raise e

            logger.debug("EC2Provider '{}': Using credential file to create session".format(self.label))
            session = boto3.session.Session(region_name=self.region, **creds)
        elif self.profile is not None:
            logger.debug("EC2Provider '{}': Using profile name to create session".format(self.label))
            session = boto3.session.Session(
                profile_name=self.profile, region_name=self.region
            )
        else:
            logger.debug("EC2Provider '{}': Using environment variables to create session".format(self.label))
            session = boto3.session.Session(region_name=self.region)

        return session