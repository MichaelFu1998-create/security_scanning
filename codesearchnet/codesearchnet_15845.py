def get_csv(self, cpu, device=None):
    """
    Returns the CSV file related to the given metric. The metric is determined by the cpu and device.
    The cpu is the CPU as in the interrupts file for example CPU12.
    The metric is a combination of the CPU and device. The device consists of IRQ #, the irq device ASCII name.

                                      CPU0   CPU1
    2014-10-29 00:27:42.15161    59:    29      2    IR-IO-APIC-edge    timer
                                  ^      ^      ^          ^              ^
                                  |      |      |          |              |
                                IRQ#   Value  Value   IRQ Device       Ascii Name

    This would produce a metric CPU0.timer-IRQ59 and CPU1.timer-IRQ59 so one per IRQ per CPU.

    :param cpu: The name of the cpu given as CPU#.
    :param device: The device name as given by the system. <ASCII name>-IRQ<IRQ #>
    :return: The CSV file for the metric.
    """
    cpu = naarad.utils.sanitize_string(cpu)
    if device is None:
      outcsv = os.path.join(self.resource_directory, "{0}.{1}.csv".format(self.label, cpu))
      self.csv_column_map[outcsv] = cpu
    else:
      device = naarad.utils.sanitize_string(device)
      outcsv = os.path.join(self.resource_directory, "{0}.{1}.{2}.csv".format(self.label, cpu, device))
      self.csv_column_map[outcsv] = cpu + '.' + device
    return outcsv