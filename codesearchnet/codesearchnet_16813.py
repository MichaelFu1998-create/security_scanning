def post(self, pid, record, action):
        """Handle deposit action.

        After the action is executed, a
        :class:`invenio_deposit.signals.post_action` signal is sent.

        Permission required: `update_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :param action: The action to execute.
        """
        record = getattr(record, action)(pid=pid)

        db.session.commit()
        # Refresh the PID and record metadata
        db.session.refresh(pid)
        db.session.refresh(record.model)
        post_action.send(current_app._get_current_object(), action=action,
                         pid=pid, deposit=record)
        response = self.make_response(pid, record,
                                      202 if action == 'publish' else 201)
        endpoint = '.{0}_item'.format(pid.pid_type)
        location = url_for(endpoint, pid_value=pid.pid_value, _external=True)
        response.headers.extend(dict(Location=location))
        return response