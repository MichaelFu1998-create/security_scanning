def delete_unused_versions(self, versions_to_keep=10):
        """
        Deletes unused versions
        """

        # get versions in use
        environments = self.ebs.describe_environments(application_name=self.app_name, include_deleted=False)
        environments = environments['DescribeEnvironmentsResponse']['DescribeEnvironmentsResult']['Environments']
        versions_in_use = []
        for env in environments:
            versions_in_use.append(env['VersionLabel'])

        # get all versions
        versions = self.ebs.describe_application_versions(application_name=self.app_name)
        versions = versions['DescribeApplicationVersionsResponse']['DescribeApplicationVersionsResult'][
            'ApplicationVersions']
        versions = sorted(versions, reverse=True, key=functools.cmp_to_key(lambda x, y: (x['DateCreated'] > y['DateCreated']) - (x['DateCreated'] < y['DateCreated'])))

        # delete versions in use
        for version in versions[versions_to_keep:]:
            if version['VersionLabel'] in versions_in_use:
                out("Not deleting " + version["VersionLabel"] + " because it is in use")
            else:
                out("Deleting unused version: " + version["VersionLabel"])
                self.ebs.delete_application_version(application_name=self.app_name,
                                                    version_label=version['VersionLabel'])
                sleep(2)