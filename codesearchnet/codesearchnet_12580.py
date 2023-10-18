def current_request_role(self) -> [int, str]:
        """
        Current role requested by client.
        :return:
        """
        role_val = self.headers.get('Role')
        return int(role_val) if role_val and role_val.isdigit() else role_val