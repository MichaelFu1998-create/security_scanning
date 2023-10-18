def _x10_command(self, house_code, unit_number, state):
        """Real implementation"""

        # log = log or default_logger
        log = default_logger
        if state.startswith('xdim') or state.startswith('dim') or state.startswith('bright'):
            raise NotImplementedError('xdim/dim/bright %r' % ((house_code, unit_num, state), ))

        if unit_number is not None:
            house_and_unit = '%s%d' % (house_code, unit_number)
        else:
            raise NotImplementedError('mochad all ON/OFF %r' % ((house_code, unit_number, state), ))
            house_and_unit = house_code

        house_and_unit = to_bytes(house_and_unit)
        # TODO normalize/validate state
        state = to_bytes(state)
        mochad_cmd = self.default_type + b' ' + house_and_unit + b' ' + state + b'\n'  # byte concat works with older Python 3.4
        log.debug('mochad send: %r', mochad_cmd)
        mochad_host, mochad_port = self.device_address
        result = netcat(mochad_host, mochad_port, mochad_cmd)
        log.debug('mochad received: %r', result)