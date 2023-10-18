def setup(
            self,
            configuration="ModbusSerialClient(method='rtu',port='/dev/cu.usbmodem14101',baudrate=9600)"
    ):
        """Start a Modbus server.

        The following classes are available with their respective named
        parameters:
        
        ModbusTcpClient
            host: The host to connect to (default 127.0.0.1)
            port: The modbus port to connect to (default 502)
            source_address: The source address tuple to bind to (default ('', 0))
            timeout: The timeout to use for this socket (default Defaults.Timeout)

        ModbusUdpClient
            host: The host to connect to (default 127.0.0.1)
            port: The modbus port to connect to (default 502)
            timeout: The timeout to use for this socket (default None)

        ModbusSerialClient
            method: The method to use for connection (asii, rtu, binary)
            port: The serial port to attach to
            stopbits: The number of stop bits to use (default 1)
            bytesize: The bytesize of the serial messages (default 8 bits)
            parity: Which kind of parity to use (default None)
            baudrate: The baud rate to use for the serial device
            timeout: The timeout between serial requests (default 3s)

        When configuring the ports, the following convention should be
        respected:
        
        portname: C1:13 -> Coil on device 1, address 13

        The letters can be:

        C = Coil
        I = Input
        R = Register
        H = Holding

        @arg configuration a string that instantiates one of those classes.

        @throw RuntimeError can't connect to Arduino
        """
        from pymodbus3.client.sync import ModbusSerialClient, ModbusUdpClient, ModbusTcpClient
        self._client = eval(configuration)
        self._client.connect()