def get(self, pid):
    ''' get method '''
    body = utils.str_cmd(['jmap', '-histo', pid], None, None)
    self.content_type = 'application/json'
    self.write(json.dumps(body))
    self.finish()