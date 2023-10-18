def createNetwork(dataSource):
  """Create the Network instance.

  The network has a sensor region reading data from `dataSource` and passing
  the encoded representation to an Identity Region.

  :param dataSource: a RecordStream instance to get data from
  :returns: a Network instance ready to run
  """
  network = Network()

  # Our input is sensor data from the gym file. The RecordSensor region
  # allows us to specify a file record stream as the input source via the
  # dataSource attribute.
  network.addRegion("sensor", "py.RecordSensor",
                    json.dumps({"verbosity": _VERBOSITY}))
  sensor = network.regions["sensor"].getSelf()
  # The RecordSensor needs to know how to encode the input values
  sensor.encoder = createEncoder()
  # Specify the dataSource as a file record stream instance
  sensor.dataSource = dataSource

  # CUSTOM REGION
  # Add path to custom region to PYTHONPATH
  # NOTE: Before using a custom region, please modify your PYTHONPATH
  # export PYTHONPATH="<path to custom region module>:$PYTHONPATH"
  # In this demo, we have modified it using sys.path.append since we need it to
  # have an effect on this program.
  sys.path.append(os.path.dirname(os.path.abspath(__file__)))
  
  from custom_region.identity_region import IdentityRegion

  # Add custom region class to the network
  Network.registerRegion(IdentityRegion)

  # Create a custom region
  network.addRegion("identityRegion", "py.IdentityRegion",
                    json.dumps({
                      "dataWidth": sensor.encoder.getWidth(),
                    }))

  # Link the Identity region to the sensor output
  network.link("sensor", "identityRegion", "UniformLink", "")

  network.initialize()

  return network