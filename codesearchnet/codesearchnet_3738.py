def receive(organization=None, user=None, team=None, credential_type=None, credential=None,
            notification_template=None, inventory_script=None, inventory=None, project=None, job_template=None,
            workflow=None, all=None):
    """Export assets from Tower.

    'tower receive' exports one or more assets from a Tower instance

    For all of the possible assets types the TEXT can either be the assets name
    (or username for the case of a user) or the keyword all. Specifying all
    will export all of the assets of that type.

    """

    from tower_cli.cli.transfer.receive import Receiver
    receiver = Receiver()
    assets_to_export = {}
    for asset_type in SEND_ORDER:
        assets_to_export[asset_type] = locals()[asset_type]
    receiver.receive(all=all, asset_input=assets_to_export)