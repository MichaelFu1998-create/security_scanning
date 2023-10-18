def get_vault(vault_obj, flags=FLAGS.ALL, **conn):
    """
    Orchestrates calls to build a Glacier Vault in the following format:

    {
        "VaultARN": ...,
        "VaultName": ...,
        "CreationDate" ...,
        "LastInventoryDate" ...,
        "NumberOfArchives" ...,
        "SizeInBytes" ...,
        "Policy" ...,
        "Tags" ...
    }
    Args:
        vault_obj: name, ARN, or dict of Glacier Vault
        flags: Flags describing which sections should be included in the return value. Default ALL

    Returns:
        dictionary describing the requested Vault
    """
    if isinstance(vault_obj, string_types):
        vault_arn = ARN(vault_obj)
        if vault_arn.error:
            vault_obj = {'VaultName': vault_obj}
        else:
            vault_obj = {'VaultName': vault_arn.parsed_name}

    return registry.build_out(flags, vault_obj, **conn)