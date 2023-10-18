def send(source=None, prevent=None, exclude=None, secret_management='default', no_color=False):
    """Import assets into Tower.

    'tower send' imports one or more assets into a Tower instance

    The import can take either JSON or YAML.
    Data can be sent on stdin (i.e. from tower-cli receive pipe) and/or from files
    or directories passed as parameters.

    If a directory is specified only files that end in .json, .yaml or .yml will be
    imported. Other files will be ignored.
    """

    from tower_cli.cli.transfer.send import Sender
    sender = Sender(no_color)
    sender.send(source, prevent, exclude, secret_management)