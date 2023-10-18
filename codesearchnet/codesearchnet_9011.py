def GetApplicationIIN(self):
        """Return the application-controlled IIN field."""
        application_iin = opendnp3.ApplicationIIN()
        application_iin.configCorrupt = False
        application_iin.deviceTrouble = False
        application_iin.localControl = False
        application_iin.needTime = False
        # Just for testing purposes, convert it to an IINField and display the contents of the two bytes.
        iin_field = application_iin.ToIIN()
        _log.debug('OutstationApplication.GetApplicationIIN: IINField LSB={}, MSB={}'.format(iin_field.LSB,
                                                                                             iin_field.MSB))
        return application_iin