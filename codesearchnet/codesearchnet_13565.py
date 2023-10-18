def process_unavailable_presence(self,stanza):
        """
        Process <presence type="unavailable"/> received from the room.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `MucPresence`
        """
        fr=stanza.get_from()
        if not fr.resource:
            return
        nick=fr.resource
        user=self.users.get(nick)
        if user:
            old_user=MucRoomUser(user)
            user.update_presence(stanza)
            self.handler.presence_changed(user,stanza)
            if user.new_nick:
                mc=stanza.get_muc_child()
                if isinstance(mc,MucUserX):
                    renames=[i for i in mc.get_items() if isinstance(i,MucStatus) and i.code==303]
                    if renames:
                        self.users[user.new_nick]=user
                        del self.users[nick]
                        return
        else:
            old_user=None
            user=MucRoomUser(stanza)
            self.users[user.nick]=user
            self.handler.presence_changed(user,stanza)
        if fr==self.room_jid and self.joined:
            self.joined=False
            self.handler.user_left(user,stanza)
            self.manager.forget(self)
            self.me=user
        elif old_user:
            self.handler.user_left(user,stanza)