def get_wifi_packet(frame, no_rtap=False):
        """Discriminates Wi-Fi packet and creates
        packet object.
        :frame: ctypes.Structure
        :no_rtap: Bool
        :return: obj
            Wi-Fi packet
        """
        _, packet = WiHelper._strip_rtap(frame)
        frame_control = struct.unpack('BB', packet[:2])
        cat = (frame_control[0] >> 2) & 0b0011
        s_type = frame_control[0] >> 4

        if cat not in _CATEGORIES_.keys():
            logging.warning("unknown category: %d" % (cat))
            return Unknown(frame, no_rtap)

        if s_type not in _SUBTYPES_[cat].keys():
            logging.warning("unknown subtype %d in %s category" % (s_type, _CATEGORIES_[cat]))
            return Unknown(frame, no_rtap)

        if cat == 0:
            if s_type == 4:
                return ProbeReq(frame, no_rtap)
            elif s_type == 5:
                return ProbeResp(frame, no_rtap)
            elif s_type == 8:
                return Beacon(frame, no_rtap)
            else:
                return Management(frame, no_rtap)
        elif cat == 1:
            if s_type == 11:
                return RTS(frame, no_rtap)
            elif s_type == 12:
                return CTS(frame, no_rtap)
            elif s_type == 9:
                return BACK(frame, no_rtap)
            else:
                return Control(frame, no_rtap)
        elif cat == 2:
            if s_type == 8:
                return QosData(frame, no_rtap, parse_amsdu=True)
            else:
                return Data(frame, no_rtap)