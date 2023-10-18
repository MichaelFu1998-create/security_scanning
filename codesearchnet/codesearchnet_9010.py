def configure_database(db_config):
        """
            Configure the Outstation's database of input point definitions.

            Configure two Analog points (group/variation 30.1) at indexes 1 and 2.
            Configure two Binary points (group/variation 1.2) at indexes 1 and 2.
        """
        db_config.analog[1].clazz = opendnp3.PointClass.Class2
        db_config.analog[1].svariation = opendnp3.StaticAnalogVariation.Group30Var1
        db_config.analog[1].evariation = opendnp3.EventAnalogVariation.Group32Var7
        db_config.analog[2].clazz = opendnp3.PointClass.Class2
        db_config.analog[2].svariation = opendnp3.StaticAnalogVariation.Group30Var1
        db_config.analog[2].evariation = opendnp3.EventAnalogVariation.Group32Var7
        db_config.binary[1].clazz = opendnp3.PointClass.Class2
        db_config.binary[1].svariation = opendnp3.StaticBinaryVariation.Group1Var2
        db_config.binary[1].evariation = opendnp3.EventBinaryVariation.Group2Var2
        db_config.binary[2].clazz = opendnp3.PointClass.Class2
        db_config.binary[2].svariation = opendnp3.StaticBinaryVariation.Group1Var2
        db_config.binary[2].evariation = opendnp3.EventBinaryVariation.Group2Var2