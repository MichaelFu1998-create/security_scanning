def register_credentials(self, credentials=None, user=None, user_file=None, password=None, password_file=None):
        """
        Helper method to store username and password
        """
        # lets store all kind of credential data into this dict
        if credentials is not None:
            self.credentials = credentials
        else:
            self.credentials = {}
            # set the user from CLI or file
            if user:
                self.credentials["user"] = user
            elif user_file:
                with open(user_file, "r") as of:
                    # what would the file entry look like?
                    pattern = re.compile("^user: ")
                    for l in of:
                        if re.match(pattern, l):
                            # strip away the newline
                            l = l[0:-1]
                            self.credentials["user"] = re.sub(pattern, "", l)
                # remove any surrounding quotes
                if self.credentials["user"][0:1] == '"' and \
                                    self.credentials["user"][-1:] == '"':
                    self.credentials["user"] = self.credentials["user"][1:-1]
            # set the password from CLI or file
            if password:
                self.credentials["password"] = password
            elif password_file:
                with open(password_file, "r") as of:
                    # what would the file entry look like?
                    pattern = re.compile("^password: ")
                    for l in of:
                        if re.match(pattern, l):
                            # strip away the newline
                            l = l[0:-1]
                            self.credentials["password"] = \
                                                    re.sub(pattern, "", l)
                # remove any surrounding quotes
                if self.credentials["password"][0:1] == '"' and \
                                    self.credentials["password"][-1:] == '"':
                    self.credentials["password"] = \
                                        self.credentials["password"][1:-1]

            # if both user and password is set,
            #  1. encode to base 64 for basic auth
            if "user" in self.credentials and "password" in self.credentials:
                c = self.credentials["user"] + ":" + self.credentials["password"]
                self.credentials["base64"] = b64encode(c.encode()).decode("ascii")