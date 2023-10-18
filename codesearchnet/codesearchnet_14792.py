def _fix_missing_tenant_id(self, context, body, key):
        """Will add the tenant_id to the context from body.

        It is assumed that the body must have a tenant_id because neutron
        core could never have gotten here otherwise.
        """
        if not body:
            raise n_exc.BadRequest(resource=key,
                                   msg="Body malformed")
        resource = body.get(key)
        if not resource:
            raise n_exc.BadRequest(resource=key,
                                   msg="Body malformed")
        if context.tenant_id is None:
            context.tenant_id = resource.get("tenant_id")
        if context.tenant_id is None:
            msg = _("Running without keystone AuthN requires "
                    "that tenant_id is specified")
            raise n_exc.BadRequest(resource=key, msg=msg)