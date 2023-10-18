def dump(self, stream, state, mevm, conc_tx=None):
        """
        Concretize and write a human readable version of the transaction into the stream. Used during testcase
        generation.

        :param stream: Output stream to write to. Typically a file.
        :param manticore.ethereum.State state: state that the tx exists in
        :param manticore.ethereum.ManticoreEVM mevm: manticore instance
        :return:
        """
        from ..ethereum import ABI  # circular imports
        from ..ethereum.manticore import flagged

        is_something_symbolic = False

        if conc_tx is None:
            conc_tx = self.concretize(state)

        # The result if any RETURN or REVERT
        stream.write("Type: %s (%d)\n" % (self.sort, self.depth))

        caller_solution = conc_tx.caller

        caller_name = mevm.account_name(caller_solution)
        stream.write("From: %s(0x%x) %s\n" % (caller_name, caller_solution, flagged(issymbolic(self.caller))))

        address_solution = conc_tx.address
        address_name = mevm.account_name(address_solution)

        stream.write("To: %s(0x%x) %s\n" % (address_name, address_solution, flagged(issymbolic(self.address))))
        stream.write("Value: %d %s\n" % (conc_tx.value, flagged(issymbolic(self.value))))
        stream.write("Gas used: %d %s\n" % (conc_tx.gas, flagged(issymbolic(self.gas))))

        tx_data = conc_tx.data

        stream.write("Data: 0x{} {}\n".format(binascii.hexlify(tx_data).decode(), flagged(issymbolic(self.data))))

        if self.return_data is not None:
            return_data = conc_tx.return_data

            stream.write("Return_data: 0x{} {}\n".format(binascii.hexlify(return_data).decode(), flagged(issymbolic(self.return_data))))

        metadata = mevm.get_metadata(self.address)
        if self.sort == 'CREATE':
            if metadata is not None:

                conc_args_data = conc_tx.data[len(metadata._init_bytecode):]
                arguments = ABI.deserialize(metadata.get_constructor_arguments(), conc_args_data)

                # TODO confirm: arguments should all be concrete?

                is_argument_symbolic = any(map(issymbolic, arguments))  # is this redundant since arguments are all concrete?
                stream.write('Function call:\n')
                stream.write("Constructor(")
                stream.write(','.join(map(repr, map(state.solve_one, arguments))))  # is this redundant since arguments are all concrete?
                stream.write(') -> %s %s\n' % (self.result, flagged(is_argument_symbolic)))

        if self.sort == 'CALL':
            if metadata is not None:
                calldata = conc_tx.data
                is_calldata_symbolic = issymbolic(self.data)

                function_id = calldata[:4]  # hope there is enough data
                signature = metadata.get_func_signature(function_id)
                function_name = metadata.get_func_name(function_id)
                if signature:
                    _, arguments = ABI.deserialize(signature, calldata)
                else:
                    arguments = (calldata,)

                return_data = None
                if self.result == 'RETURN':
                    ret_types = metadata.get_func_return_types(function_id)
                    return_data = conc_tx.return_data
                    return_values = ABI.deserialize(ret_types, return_data)  # function return

                is_return_symbolic = issymbolic(self.return_data)

                stream.write('\n')
                stream.write("Function call:\n")
                stream.write("%s(" % function_name)
                stream.write(','.join(map(repr, arguments)))
                stream.write(') -> %s %s\n' % (self.result, flagged(is_calldata_symbolic)))

                if return_data is not None:
                    if len(return_values) == 1:
                        return_values = return_values[0]

                    stream.write('return: %r %s\n' % (return_values, flagged(is_return_symbolic)))
                is_something_symbolic = is_calldata_symbolic or is_return_symbolic

        stream.write('\n\n')
        return is_something_symbolic