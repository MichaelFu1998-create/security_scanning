def actionsiter(self):
        """Iterator."""
        for msg in self.queue.consume():
            try:
                for preproc in self.preprocessors:
                    msg = preproc(msg)
                    if msg is None:
                        break
                if msg is None:
                    continue
                suffix = arrow.get(msg.get('timestamp')).strftime(self.suffix)
                ts = parser.parse(msg.get('timestamp'))
                # Truncate timestamp to keep only seconds. This is to improve
                # elasticsearch performances.
                ts = ts.replace(microsecond=0)
                msg['timestamp'] = ts.isoformat()
                # apply timestamp windowing in order to group events too close
                # in time
                if self.double_click_window > 0:
                    timestamp = mktime(utc.localize(ts).utctimetuple())
                    ts = ts.fromtimestamp(
                        timestamp // self.double_click_window *
                        self.double_click_window
                    )
                yield dict(
                    _id=hash_id(ts.isoformat(), msg),
                    _op_type='index',
                    _index='{0}-{1}'.format(self.index, suffix),
                    _type=self.doctype,
                    _source=msg,
                )
            except Exception:
                current_app.logger.exception(u'Error while processing event')