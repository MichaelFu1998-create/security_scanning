def _handle_system_status_event(self, event: SystemStatusEvent) -> None:
        """
        DISARMED -> ARMED_AWAY -> EXIT_DELAY_START -> EXIT_DELAY_END
         (trip): -> ALARM -> OUTPUT_ON -> ALARM_RESTORE
            (disarm): -> DISARMED -> OUTPUT_OFF
         (disarm): -> DISARMED
         (disarm before EXIT_DELAY_END): -> DISARMED -> EXIT_DELAY_END

        TODO(NW): Check ALARM_RESTORE state transition to move back into ARMED_AWAY state
        """
        if event.type == SystemStatusEvent.EventType.UNSEALED:
            return self._update_zone(event.zone, True)
        elif event.type == SystemStatusEvent.EventType.SEALED:
            return self._update_zone(event.zone, False)
        elif event.type == SystemStatusEvent.EventType.ALARM:
            return self._update_arming_state(ArmingState.TRIGGERED)
        elif event.type == SystemStatusEvent.EventType.ALARM_RESTORE:
            if self.arming_state != ArmingState.DISARMED:
                return self._update_arming_state(ArmingState.ARMED)
        elif event.type == SystemStatusEvent.EventType.ENTRY_DELAY_START:
            return self._update_arming_state(ArmingState.ENTRY_DELAY)
        elif event.type == SystemStatusEvent.EventType.ENTRY_DELAY_END:
            pass
        elif event.type == SystemStatusEvent.EventType.EXIT_DELAY_START:
            return self._update_arming_state(ArmingState.EXIT_DELAY)
        elif event.type == SystemStatusEvent.EventType.EXIT_DELAY_END:
            # Exit delay finished - if we were in the process of arming update
            # state to armed
            if self.arming_state == ArmingState.EXIT_DELAY:
                return self._update_arming_state(ArmingState.ARMED)
        elif event.type in Alarm.ARM_EVENTS:
            return self._update_arming_state(ArmingState.ARMING)
        elif event.type == SystemStatusEvent.EventType.DISARMED:
            return self._update_arming_state(ArmingState.DISARMED)
        elif event.type == SystemStatusEvent.EventType.ARMING_DELAYED:
            pass