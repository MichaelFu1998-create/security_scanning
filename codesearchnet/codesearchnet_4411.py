def udp_messenger(domain_name, UDP_IP, UDP_PORT, sock_timeout, message):
    """Send UDP messages to usage tracker asynchronously

    This multiprocessing based messenger was written to overcome the limitations
    of signalling/terminating a thread that is blocked on a system call. This
    messenger is created as a separate process, and initialized with 2 queues,
    to_send to receive messages to be sent to the internet.

    Args:
          - domain_name (str) : Domain name string
          - UDP_IP (str) : IP address YYY.YYY.YYY.YYY
          - UDP_PORT (int) : UDP port to send out on
          - sock_timeout (int) : Socket timeout
          - to_send (multiprocessing.Queue) : Queue of outgoing messages to internet
    """
    try:
        if message is None:
            raise ValueError("message was none")

        encoded_message = bytes(message, "utf-8")

        if encoded_message is None:
            raise ValueError("utf-8 encoding of message failed")

        if domain_name:
            try:
                UDP_IP = socket.gethostbyname(domain_name)
            except Exception:
                # (False, "Domain lookup failed, defaulting to {0}".format(UDP_IP))
                pass

        if UDP_IP is None:
            raise Exception("UDP_IP is None")

        if UDP_PORT is None:
            raise Exception("UDP_PORT is None")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.settimeout(sock_timeout)
        sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
        sock.close()

    except socket.timeout:
        logger.debug("Failed to send usage tracking data: socket timeout")
    except OSError as e:
        logger.debug("Failed to send usage tracking data: OSError: {}".format(e))
    except Exception as e:
        logger.debug("Failed to send usage tracking data: Exception: {}".format(e))