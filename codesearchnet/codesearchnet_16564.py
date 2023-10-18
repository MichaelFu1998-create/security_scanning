async def rt_subscribe(self, loop, async_callback):
        """Connect to Tibber and subscribe to Tibber rt subscription."""
        if self._subscription_id is not None:
            _LOGGER.error("Already subscribed.")
            return
        await self._tibber_control.rt_connect(loop)
        document = gql(
            """
            subscription{
              liveMeasurement(homeId:"%s"){
                timestamp
                power
                powerProduction
                accumulatedProduction
                accumulatedConsumption
                accumulatedCost
                currency
                minPower
                averagePower
                maxPower
                voltagePhase1
                voltagePhase2
                voltagePhase3
                currentPhase1
                currentPhase2
                currentPhase3
                lastMeterConsumption
                lastMeterProduction
            }
           }
        """
            % self.home_id
        )
        sub_query = print_ast(document)

        self._subscription_id = await self._tibber_control.sub_manager.subscribe(
            sub_query, async_callback
        )