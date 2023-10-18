def dispatch(self, message, source = None):
        """Sends decoded OSC data to an appropriate calback"""
        msgtype = ""
        try:
            if type(message[0]) == str:
                # got a single message
                address = message[0]
                self.callbacks[address](message)
            elif type(message[0]) == list:
                for msg in message:
                    self.dispatch(msg)
        except KeyError, key:
            print 'address %s not found, %s: %s' % (address, key, message)
            pprint.pprint(message)
        except IndexError, e:
            print '%s: %s' % (e, message)
            pass
        except None, e:
            print "Exception in", address, "callback :", e

        return