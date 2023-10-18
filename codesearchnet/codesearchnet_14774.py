def delete_tenant_quota(context, tenant_id):
        """Delete the quota entries for a given tenant_id.

        Atfer deletion, this tenant will use default quota values in conf.
        """

        tenant_quotas = context.session.query(Quota)
        tenant_quotas = tenant_quotas.filter_by(tenant_id=tenant_id)
        tenant_quotas.delete()