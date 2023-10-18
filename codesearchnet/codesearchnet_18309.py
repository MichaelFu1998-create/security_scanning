def stream(self, report):
        """Stream reports to application logs"""
        with self.ClientSession() as session:
            lines = []
            for job in report['traces']:
                key = '%s:%s' % (self.name, job)
                for minute in report['traces'][job]:
                    for k, v in report['traces'][job][minute].items():
                        lines.append('# TYPE %s_%s gauge' % (key, k))
                        lines.append('%s_%s %0.2f' % (key, k, v))

            # Empty is required at the end of the payload
            lines.append("")
            data = "\n".join(lines)
            logger.info(data)
            yield from session.post(self.url, data=bytes(data.encode('utf-8')))