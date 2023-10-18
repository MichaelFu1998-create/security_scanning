def parse_tweets(raw_tweets, source, now=None):
    """
        Parses a list of raw tweet lines from a twtxt file
        and returns a list of :class:`Tweet` objects.

        :param list raw_tweets: list of raw tweet lines
        :param Source source: the source of the given tweets
        :param Datetime now: the current datetime

        :returns: a list of parsed tweets :class:`Tweet` objects
        :rtype: list
    """
    if now is None:
        now = datetime.now(timezone.utc)

    tweets = []
    for line in raw_tweets:
        try:
            tweet = parse_tweet(line, source, now)
        except (ValueError, OverflowError) as e:
            logger.debug("{0} - {1}".format(source.url, e))
        else:
            tweets.append(tweet)

    return tweets