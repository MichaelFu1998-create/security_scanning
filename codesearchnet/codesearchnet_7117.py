async def set_active(self):
        """Set this client as active.

        While a client is active, no other clients will raise notifications.
        Call this method whenever there is an indication the user is
        interacting with this client. This method may be called very
        frequently, and it will only make a request when necessary.
        """
        is_active = (self._active_client_state ==
                     hangouts_pb2.ACTIVE_CLIENT_STATE_IS_ACTIVE)
        timed_out = (time.time() - self._last_active_secs >
                     SETACTIVECLIENT_LIMIT_SECS)
        if not is_active or timed_out:
            # Update these immediately so if the function is called again
            # before the API request finishes, we don't start extra requests.
            self._active_client_state = (
                hangouts_pb2.ACTIVE_CLIENT_STATE_IS_ACTIVE
            )
            self._last_active_secs = time.time()

            # The first time this is called, we need to retrieve the user's
            # email address.
            if self._email is None:
                try:
                    get_self_info_request = hangouts_pb2.GetSelfInfoRequest(
                        request_header=self.get_request_header(),
                    )
                    get_self_info_response = await self.get_self_info(
                        get_self_info_request
                    )
                except exceptions.NetworkError as e:
                    logger.warning('Failed to find email address: {}'
                                   .format(e))
                    return
                self._email = (
                    get_self_info_response.self_entity.properties.email[0]
                )

            # If the client_id hasn't been received yet, we can't set the
            # active client.
            if self._client_id is None:
                logger.info(
                    'Cannot set active client until client_id is received'
                )
                return

            try:
                set_active_request = hangouts_pb2.SetActiveClientRequest(
                    request_header=self.get_request_header(),
                    is_active=True,
                    full_jid="{}/{}".format(self._email, self._client_id),
                    timeout_secs=ACTIVE_TIMEOUT_SECS,
                )
                await self.set_active_client(set_active_request)
            except exceptions.NetworkError as e:
                logger.warning('Failed to set active client: {}'.format(e))
            else:
                logger.info('Set active client for {} seconds'
                            .format(ACTIVE_TIMEOUT_SECS))