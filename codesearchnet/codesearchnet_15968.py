def parse_tagged_params(raw_tagged_params):
        """strip tagged information elements wlan_mgt.tag
        which has generic type-length-value structure
        [type, length, value]
        type(1 byte), length(1 byte), value(varies)
        [wlan_mgt.tag.number, wlan_mgt.tag.length, payload]
        structured fields.
        :return: dict[]
            list of tagged params
        :return: int
            0 in succ, 1 for
        """
        fcs_len = 4  # wlan.fcs (4 bytes)
        idx = 0
        tagged_params = []
        while idx < len(raw_tagged_params) - fcs_len:
            tag_num, tag_len = struct.unpack('BB', raw_tagged_params[idx:idx + 2])
            idx += 2
            if len(raw_tagged_params) >= idx + tag_len:
                param = {}
                param['number'], param['length'] = tag_num, tag_len
                payload = raw_tagged_params[idx:idx + tag_len]
                if tag_num in MNGMT_TAGS:
                    param['name'] = MNGMT_TAGS[tag_num]
                    if MNGMT_TAGS[tag_num] == 'TAG_VENDOR_SPECIFIC_IE':
                        param['payload'] = Management.parse_vendor_ie(payload)
                    else:
                        param['payload'] = payload
                else:
                    param['name'] = None
                tagged_params.append(param)
                idx += tag_len
            else:
                logging.warning('out tag length header points out of boundary')
                log_msg = 'index: {p_idx}, pack_len: {p_len}'
                log_msg = log_msg.format(p_idx=idx + tag_len,
                                         p_len=len(raw_tagged_params))
                logging.warning(log_msg)
                return 1, tagged_params
        return 0, tagged_params