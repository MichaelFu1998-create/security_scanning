def formatter(self, api_client, data, newval):
        """Get audio-related fields

        Try to find fields for the audio url for specified preferred quality
        level, or next-lowest available quality url otherwise.
        """
        url_map = data.get("audioUrlMap")
        audio_url = data.get("audioUrl")

        # Only an audio URL, not a quality map. This happens for most of the
        # mobile client tokens and some of the others now. In this case
        # substitute the empirically determined default values in the format
        # used by the rest of the function so downstream consumers continue to
        # work.
        if audio_url and not url_map:
            url_map = {
                BaseAPIClient.HIGH_AUDIO_QUALITY: {
                    "audioUrl": audio_url,
                    "bitrate": 64,
                    "encoding": "aacplus",
                }
            }
        elif not url_map:  # No audio url available (e.g. ad tokens)
            return None

        valid_audio_formats = [BaseAPIClient.HIGH_AUDIO_QUALITY,
                               BaseAPIClient.MED_AUDIO_QUALITY,
                               BaseAPIClient.LOW_AUDIO_QUALITY]

        # Only iterate over sublist, starting at preferred audio quality, or
        # from the beginning of the list if nothing is found. Ensures that the
        # bitrate used will always be the same or lower quality than was
        # specified to prevent audio from skipping for slow connections.
        preferred_quality = api_client.default_audio_quality
        if preferred_quality in valid_audio_formats:
            i = valid_audio_formats.index(preferred_quality)
            valid_audio_formats = valid_audio_formats[i:]

        for quality in valid_audio_formats:
            audio_url = url_map.get(quality)

            if audio_url:
                return audio_url[self.field]

        return audio_url[self.field] if audio_url else None