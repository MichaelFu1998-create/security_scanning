def scale_in(self, blocks=0, machines=0, strategy=None):
        ''' Scale in resources
        '''
        count = 0
        instances = self.client.servers.list()
        for instance in instances[0:machines]:
            print("Deleting : ", instance)
            instance.delete()
            count += 1

        return count