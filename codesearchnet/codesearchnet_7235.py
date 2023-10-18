def _on_return(self, text):
        """Called when the user presses return on the send message widget."""
        # Ignore if the user hasn't typed a message.
        if not text:
            return
        elif text.startswith('/image') and len(text.split(' ')) == 2:
            # Temporary UI for testing image uploads
            filename = text.split(' ')[1]
            image_file = open(filename, 'rb')
            text = ''
        else:
            image_file = None
        text = replace_emoticons(text)
        segments = hangups.ChatMessageSegment.from_str(text)
        self._coroutine_queue.put(
            self._handle_send_message(
                self._conversation.send_message(
                    segments, image_file=image_file
                )
            )
        )