def get_object(cls, api_token, ip):
        """
            Class method that will return a FloatingIP object by its IP.

            Args:
                api_token: str - token
                ip: str - floating ip address
        """
        floating_ip = cls(token=api_token, ip=ip)
        floating_ip.load()
        return floating_ip