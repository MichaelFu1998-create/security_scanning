def decode_payload(self, payload):
        """This function can extract multiple messages from one HTTP payload.
        Some times, the XHR/JSONP/.. transports can pack more than one message
        on a single packet.  They are encoding following the WebSocket
        semantics, which need to be reproduced here to unwrap the messages.

        The semantics are:

          \ufffd + [length as a string] + \ufffd + [payload as a unicode string]

        This function returns a list of messages, even though there is only
        one.

        Inspired by socket.io/lib/transports/http.js
        """
        payload = payload.decode('utf-8')
        if payload[0] == u"\ufffd":
            ret = []
            while len(payload) != 0:
                len_end = payload.find(u"\ufffd", 1)
                length = int(payload[1:len_end])
                msg_start = len_end + 1
                msg_end = length + msg_start
                message = payload[msg_start:msg_end]
                ret.append(message)
                payload = payload[msg_end:]
            return ret
        return [payload]