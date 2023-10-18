def rpcexec(self, payload):
        """ Manual execute a command on API (internally used)

            param str payload: The payload containing the request
            return: Servers answer to the query
            rtype: json
            raises RPCConnection: if no connction can be made
            raises UnauthorizedError: if the user is not authorized
            raise ValueError: if the API returns a non-JSON formated answer

            It is not recommended to use this method directly, unless
            you know what you are doing. All calls available to the API
            will be wrapped to methods directly::

                info -> grapheneapi.info()
        """
        try:
            response = requests.post(
                "http://{}:{}/rpc".format(self.host, self.port),
                data=json.dumps(payload, ensure_ascii=False).encode("utf8"),
                headers=self.headers,
                auth=(self.username, self.password),
            )
            if response.status_code == 401:
                raise UnauthorizedError
            ret = json.loads(response.text)
            if "error" in ret:
                if "detail" in ret["error"]:
                    raise RPCError(ret["error"]["detail"])
                else:
                    raise RPCError(ret["error"]["message"])
        except requests.exceptions.RequestException:
            raise RPCConnection("Error connecting to Client!")
        except UnauthorizedError:
            raise UnauthorizedError("Invalid login credentials!")
        except ValueError:
            raise ValueError("Client returned invalid format. Expected JSON!")
        except RPCError as err:
            raise err
        else:
            return ret["result"]