def add_objects(self, bundle, wait_for_completion=True, poll_interval=1,
                    timeout=60, accept=MEDIA_TYPE_TAXII_V20,
                    content_type=MEDIA_TYPE_STIX_V20):
        """Implement the ``Add Objects`` endpoint (section 5.4)

        Add objects to the collection.  This may be performed either
        synchronously or asynchronously.  To add asynchronously, set
        wait_for_completion to False.  If False, the latter two args are
        unused.  If the caller wishes to monitor the status of the addition,
        it may do so in its own way.  To add synchronously, set
        wait_for_completion to True, and optionally set the poll and timeout
        intervals.  After initiating the addition, the caller will block,
        and the TAXII "status" service will be polled until the timeout
        expires, or the operation completes.

        Args:
            bundle: A STIX bundle with the objects to add (string, dict, binary)
            wait_for_completion (bool): Whether to wait for the add operation
                to complete before returning
            poll_interval (int): If waiting for completion, how often to poll
                the status service (seconds)
            timeout (int): If waiting for completion, how long to poll until
                giving up (seconds).  Use <= 0 to wait forever
            accept (str): media type to include in the ``Accept:`` header.
            content_type (str): media type to include in the ``Content-Type:``
                header.

        Returns:
            If ``wait_for_completion`` is False, a Status object corresponding
            to the initial status data returned from the service, is returned.
            The status may not yet be complete at this point.

            If ``wait_for_completion`` is True, a Status object corresponding
            to the completed operation is returned if it didn't time out;
            otherwise a Status object corresponding to the most recent data
            obtained before the timeout, is returned.

        """
        self._verify_can_write()

        headers = {
            "Accept": accept,
            "Content-Type": content_type,
        }

        if isinstance(bundle, dict):
            json_text = json.dumps(bundle, ensure_ascii=False)
            data = json_text.encode("utf-8")

        elif isinstance(bundle, six.text_type):
            data = bundle.encode("utf-8")

        elif isinstance(bundle, six.binary_type):
            data = bundle

        else:
            raise TypeError("Don't know how to handle type '{}'".format(
                type(bundle).__name__))

        status_json = self._conn.post(self.objects_url, headers=headers,
                                      data=data)

        status_url = urlparse.urljoin(
            self.url,
            "../../status/{}".format(status_json["id"])
        )

        status = Status(url=status_url, conn=self._conn,
                        status_info=status_json)

        if not wait_for_completion or status.status == "complete":
            return status

        status.wait_until_final(poll_interval, timeout)

        return status