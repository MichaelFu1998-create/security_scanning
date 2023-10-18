def get_role_name(region, account_id, role):
    """Shortcut to insert the `account_id` and `role` into the iam string."""
    prefix = ARN_PREFIXES.get(region, 'aws')
    return 'arn:{0}:iam::{1}:role/{2}'.format(prefix, account_id, role)