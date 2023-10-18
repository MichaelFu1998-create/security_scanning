def _adjust_delay(self, slot, response):
        """Define delay adjustment policy"""
        if response.status in self.retry_http_codes:
            new_delay = max(slot.delay, 1) * 4
            new_delay = max(new_delay, self.mindelay)
            new_delay = min(new_delay, self.maxdelay)
            slot.delay = new_delay
            self.stats.inc_value('delay_count')
        elif response.status == 200:
            new_delay = max(slot.delay / 2, self.mindelay)
            if new_delay < 0.01:
                new_delay = 0
            slot.delay = new_delay