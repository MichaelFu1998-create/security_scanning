def is_self(addr):
  '''
  check if this host is this addr
  '''
  ips = []
  for i in netifaces.interfaces():
    entry = netifaces.ifaddresses(i)
    if netifaces.AF_INET in entry:
      for ipv4 in entry[netifaces.AF_INET]:
        if "addr" in ipv4:
          ips.append(ipv4["addr"])
  return addr in ips or addr == get_self_hostname()