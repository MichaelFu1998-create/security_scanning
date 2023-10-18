def parse_log_messages(self, text):
        """Will parse git log messages in the 'short' format"""
        regex = r"commit ([0-9a-f]+)\nAuthor: (.*?)\n\n(.*?)(?:\n\n|$)"
        messages = re.findall(regex, text, re.DOTALL)
        
        parsed = []
        for commit, author, message in messages:
            parsed.append((
                commit[:10],
                re.sub(r"\s*<.*?>", "", author), # Remove email address if present
                message.strip()
            ))
        return parsed