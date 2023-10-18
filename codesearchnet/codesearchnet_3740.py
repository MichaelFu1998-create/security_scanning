def empty(organization=None, user=None, team=None, credential_type=None, credential=None, notification_template=None,
          inventory_script=None, inventory=None, project=None, job_template=None, workflow=None,
          all=None, no_color=False):
    """Empties assets from Tower.

    'tower empty' removes all assets from Tower

    """

    # Create an import/export object
    from tower_cli.cli.transfer.cleaner import Cleaner
    destroyer = Cleaner(no_color)
    assets_to_export = {}
    for asset_type in SEND_ORDER:
        assets_to_export[asset_type] = locals()[asset_type]
    destroyer.go_ham(all=all, asset_input=assets_to_export)