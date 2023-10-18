async def _create_upstream_applications(self):
        """
        Create the upstream applications.
        """
        loop = asyncio.get_event_loop()
        for steam_name, ApplicationsCls in self.applications.items():
            application = ApplicationsCls(self.scope)
            upstream_queue = asyncio.Queue()
            self.application_streams[steam_name] = upstream_queue
            self.application_futures[steam_name] = loop.create_task(
                application(
                    upstream_queue.get,
                    partial(self.dispatch_downstream, steam_name=steam_name)
                )
            )