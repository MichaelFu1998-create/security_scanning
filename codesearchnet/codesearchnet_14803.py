def remove_floating_ip(self, floating_ip):
        """Register a floating ip with Unicorn

        :param floating_ip: The quark.db.models.IPAddress to remove
        :return: None
        """
        url = "%s/%s" % (CONF.QUARK.floating_ip_base_url,
                         floating_ip.address_readable)
        timeout = CONF.QUARK.unicorn_api_timeout_seconds

        try:
            LOG.info("Calling unicorn to remove floating ip: %s" % url)
            r = requests.delete(url, timeout=timeout)
        except Exception as e:
            LOG.error("Unhandled Exception caught when trying to un-register "
                      "floating ip %s with the unicorn API.  Error: %s"
                      % (floating_ip.id, e.message))
            raise ex.RemoveFloatingIpFailure(id=floating_ip.id)

        if r.status_code == 404:
            LOG.warn("The floating IP %s does not exist in the unicorn system."
                     % floating_ip.address_readable)
        elif r.status_code != 204:
            msg = "Unexpected status from unicorn API: Status Code %s, " \
                  "Message: %s" % (r.status_code, r.json())
            LOG.error("remove_floating_ip: %s" % msg)
            raise ex.RemoveFloatingIpFailure(id=floating_ip.id)