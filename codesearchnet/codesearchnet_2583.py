def get(self, instance_id):
    ''' get method '''
    self.content_type = 'application/json'
    self.write(json.dumps(utils.chain([
        ['ps', 'auxwwww'],
        ['grep', instance_id],
        ['grep', 'java'],
        ['awk', '\'{print $2}\'']])).strip())
    self.finish()