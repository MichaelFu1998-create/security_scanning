async def update_info(self, *_):
        """Update home info async."""
        query = gql(
            """
        {
          viewer {
            name
            homes {
              subscriptions {
                status
              }
              id
            }
          }
        }
        """
        )

        res = await self._execute(query)
        if res is None:
            return
        errors = res.get("errors", [])
        if errors:
            msg = errors[0].get("message", "failed to login")
            _LOGGER.error(msg)
            raise InvalidLogin(msg)

        data = res.get("data")
        if not data:
            return
        viewer = data.get("viewer")
        if not viewer:
            return
        self._name = viewer.get("name")
        homes = viewer.get("homes", [])
        self._home_ids = []
        for _home in homes:
            home_id = _home.get("id")
            self._all_home_ids += [home_id]
            subs = _home.get("subscriptions")
            if subs:
                status = subs[0].get("status", "ended").lower()
                if not home_id or status != "running":
                    continue
            self._home_ids += [home_id]