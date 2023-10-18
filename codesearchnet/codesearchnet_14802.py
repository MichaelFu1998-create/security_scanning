def register_floating_ip(self, floating_ip, port_fixed_ips):
        """Register a floating ip with Unicorn

        :param floating_ip: The quark.db.models.IPAddress to register
        :param port_fixed_ips: A dictionary containing the port and fixed ips
        to associate the floating IP with.  Has the structure of:
        {"<id of port>": {"port": <quark.db.models.Port>,
         "fixed_ip": "<fixed ip address>"}}
        :return: None
        """
        url = CONF.QUARK.floating_ip_base_url
        timeout = CONF.QUARK.unicorn_api_timeout_seconds
        req = self._build_request_body(floating_ip, port_fixed_ips)

        try:
            LOG.info("Calling unicorn to register floating ip: %s %s"
                     % (url, req))
            r = requests.post(url, data=json.dumps(req), timeout=timeout)
        except Exception as e:
            LOG.error("Unhandled Exception caught when trying to register "
                      "floating ip %s with the unicorn API.  Error: %s"
                      % (floating_ip.id, e.message))
            raise ex.RegisterFloatingIpFailure(id=floating_ip.id)

        if r.status_code != 200 and r.status_code != 201:
            msg = "Unexpected status from unicorn API: Status Code %s, " \
                  "Message: %s" % (r.status_code, r.json())
            LOG.error("register_floating_ip: %s" % msg)
            raise ex.RegisterFloatingIpFailure(id=floating_ip.id)