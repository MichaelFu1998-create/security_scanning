def process_available_presence(self,stanza):
        """
        Process <presence/> received from the room.

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
            user.nick=nick
        else:
            old_user=None
            user=MucRoomUser(stanza)
            self.users[user.nick]=user
        self.handler.presence_changed(user,stanza)
        if fr==self.room_jid and not self.joined:
            self.joined=True
            self.me=user
            mc=stanza.get_muc_child()
            if isinstance(mc,MucUserX):
                status = [i for i in mc.get_items() if isinstance(i,MucStatus) and i.code==201]
                if status:
                    self.configured = False
                    self.handler.room_created(stanza)
            if self.configured is None:
                self.configured = True
        if not old_user or old_user.role=="none":
            self.handler.user_joined(user,stanza)
        else:
            if old_user.nick!=user.nick:
                self.handler.nick_changed(user,old_user.nick,stanza)
                if old_user.room_jid==self.room_jid:
                    self.room_jid=fr
            if old_user.role!=user.role:
                self.handler.role_changed(user,old_user.role,user.role,stanza)
            if old_user.affiliation!=user.affiliation:
                self.handler.affiliation_changed(user,old_user.affiliation,user.affiliation,stanza)