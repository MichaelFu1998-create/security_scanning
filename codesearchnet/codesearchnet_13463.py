def _make_response(self, nonce, salt, iteration_count):
        """Make a response for the first challenge from the server.

        :return: the response or a failure indicator.
        :returntype: `sasl.Response` or `sasl.Failure`
        """
        self._salted_password = self.Hi(self.Normalize(self.password), salt,
                                                            iteration_count)
        self.password = None # not needed any more
        if self.channel_binding:
            channel_binding = b"c=" + standard_b64encode(self._gs2_header +
                                                                self._cb_data)
        else:
            channel_binding = b"c=" + standard_b64encode(self._gs2_header)

        # pylint: disable=C0103
        client_final_message_without_proof = (channel_binding + b",r=" + nonce)

        client_key = self.HMAC(self._salted_password, b"Client Key")
        stored_key = self.H(client_key)
        auth_message = ( self._client_first_message_bare + b"," +
                                    self._server_first_message + b"," +
                                        client_final_message_without_proof )
        self._auth_message = auth_message
        client_signature = self.HMAC(stored_key, auth_message)
        client_proof = self.XOR(client_key, client_signature)
        proof = b"p=" + standard_b64encode(client_proof)
        client_final_message = (client_final_message_without_proof + b"," +
                                                                    proof)
        return Response(client_final_message)