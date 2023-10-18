def prepare(self):
        """
        This uploads the protocol functions nessecary to do binary
        chunked transfer
        """
        log.info('Preparing esp for transfer.')

        for func in LUA_FUNCTIONS:
            detected = self.__exchange('print({0})'.format(func))
            if detected.find('function:') == -1:
                break
        else:
            log.info('Preparation already done. Not adding functions again.')
            return True
        functions = RECV_LUA + '\n' + SEND_LUA
        data = functions.format(baud=self._port.baudrate)
        ##change any \r\n to just \n and split on that
        lines = data.replace('\r', '').split('\n')

        #remove some unneccesary spaces to conserve some bytes
        for line in lines:
            line = line.strip().replace(', ', ',').replace(' = ', '=')

            if len(line) == 0:
                continue

            resp = self.__exchange(line)
            #do some basic test of the result
            if ('unexpected' in resp) or ('stdin' in resp) or len(resp) > len(functions)+10:
                log.error('error when preparing "%s"', resp)
                return False
        return True