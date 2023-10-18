def write_json_response(self, response):
    """ write back json response """
    self.write(tornado.escape.json_encode(response))
    self.set_header("Content-Type", "application/json")