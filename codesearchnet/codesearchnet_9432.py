def parse_tweet(raw_tweet, source, now=None):
    """
        Parses a single raw tweet line from a twtxt file
        and returns a :class:`Tweet` object.

        :param str raw_tweet: a single raw tweet line
        :param Source source: the source of the given tweet
        :param Datetime now: the current datetime

        :returns: the parsed tweet
        :rtype: Tweet
    """
    if now is None:
        now = datetime.now(timezone.utc)

    raw_created_at, text = raw_tweet.split("\t", 1)
    created_at = parse_iso8601(raw_created_at)

    if created_at > now:
        raise ValueError("Tweet is from the future")

    return Tweet(click.unstyle(text.strip()), created_at, source)