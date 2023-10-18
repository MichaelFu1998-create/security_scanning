def hash_id(iso_timestamp, msg):
    """Generate event id, optimized for ES."""
    return '{0}-{1}'.format(iso_timestamp,
                            hashlib.sha1(
                                msg.get('unique_id').encode('utf-8') +
                                str(msg.get('visitor_id')).
                                encode('utf-8')).
                            hexdigest())