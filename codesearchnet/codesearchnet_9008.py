def main():
    """The Outstation has been started from the command line. Execute ad-hoc tests if desired."""
    app = OutstationApplication()
    _log.debug('Initialization complete. In command loop.')
    # Ad-hoc tests can be inserted here if desired. See outstation_cmd.py for examples.
    app.shutdown()
    _log.debug('Exiting.')
    exit()