def run(self, *args, **kwargs):
        """ Deal with the incoming packets """
        while True:
            try:
                timestamp, ip_p = self._queue.popleft()

                src_ip = get_ip(ip_p, ip_p.src)
                dst_ip = get_ip(ip_p, ip_p.dst)

                src = intern('%s:%s' % (src_ip, ip_p.data.sport))
                dst = intern('%s:%s' % (dst_ip, ip_p.data.dport))
                key = intern('%s<->%s' % (src, dst))

                stream = self._streams.get(key)
                if stream is None:
                    stream = Stream(src, dst)
                    self._streams[key] = stream

                # HACK: save the timestamp
                setattr(ip_p, 'timestamp', timestamp)
                pushed = stream.push(ip_p)

                if not pushed:
                    continue

                # let listeners know about the updated stream
                for handler in self._handlers:
                    try:
                        handler(stream)
                    except Exception as ex:
                        print('handler exception: %s' % ex)
            except Exception:
                time.sleep(0.00001)