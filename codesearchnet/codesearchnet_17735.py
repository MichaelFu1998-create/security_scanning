def _x10_command(self, house_code, unit_number, state):
        """Real implementation"""

        # log = log or default_logger
        log = default_logger

        # FIXME move these functions?
        def scale_255_to_8(x):
            """Scale x from 0..255 to 0..7
            0 is considered OFF
            8 is considered fully on
            """
            factor = x / 255.0
            return 8 - int(abs(round(8 * factor)))

        def scale_31_to_8(x):
            """Scale x from 0..31 to 0..7
            0 is considered OFF
            8 is considered fully on
            """
            factor = x / 31.0
            return 8 - int(abs(round(8 * factor)))

        serial_port_name = self.device_address
        house_code = normalize_housecode(house_code)
        if unit_number is not None:
            unit_number = normalize_unitnumber(unit_number)
        else:
            # command is intended for the entire house code, not a single unit number
            if firecracker:
                log.error('using python-x10-firecracker-interface NO support for all ON/OFF')
        # TODO normalize/validate state, sort of implemented below

        if firecracker:
            log.debug('firecracker send: %r', (serial_port_name, house_code, unit_number, state))
            firecracker.send_command(serial_port_name, house_code, unit_number, state)
        else:
            if unit_number is not None:
                if state.startswith('xdim') or state.startswith('dim') or state.startswith('bright'):
                    dim_count = int(state.split()[-1])
                    if state.startswith('xdim'):
                        dim_count = scale_255_to_8(dim_count)
                    else:
                        # assumed dim or bright
                        dim_count = scale_31_to_8(dim_count)
                    dim_str = ', %s dim' % (house_code, )
                    dim_list = []
                    for _ in range(dim_count):
                        dim_list.append(dim_str)
                    dim_str = ''.join(dim_list)
                    if dim_count == 0:
                        # No dim
                        x10_command_str = '%s%s %s' % (house_code, unit_number, 'on')
                    else:
                        # If lamp is already dimmed, need to turn it off and then back on
                        x10_command_str = '%s%s %s, %s%s %s%s' % (house_code, unit_number, 'off', house_code, unit_number, 'on', dim_str)
                else:
                    x10_command_str = '%s%s %s' % (house_code, unit_number, state)
            else:
                # Assume a command for house not a specific unit
                state = x10_mapping[state]

                x10_command_str = '%s %s' % (house_code, state)
            log.debug('x10_command_str send: %r', x10_command_str)
            x10.sendCommands(serial_port_name, x10_command_str)