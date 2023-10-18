def register_disco_cache_fetchers(cache_suite,stream):
    """Register Service Discovery cache fetchers into given
    cache suite and using the stream provided.

    :Parameters:
        - `cache_suite`: the cache suite where the fetchers are to be
          registered.
        - `stream`: the stream to be used by the fetchers.
    :Types:
        - `cache_suite`: `cache.CacheSuite`
        - `stream`: `pyxmpp.stream.Stream`
    """
    tmp=stream
    class DiscoInfoCacheFetcher(DiscoCacheFetcherBase):
        """Cache fetcher for DiscoInfo."""
        stream=tmp
        disco_class=DiscoInfo
    class DiscoItemsCacheFetcher(DiscoCacheFetcherBase):
        """Cache fetcher for DiscoItems."""
        stream=tmp
        disco_class=DiscoItems
    cache_suite.register_fetcher(DiscoInfo,DiscoInfoCacheFetcher)
    cache_suite.register_fetcher(DiscoItems,DiscoItemsCacheFetcher)