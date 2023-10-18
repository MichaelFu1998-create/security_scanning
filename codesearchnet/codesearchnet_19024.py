def _rc_rename(self, src, dst):
        """
        Rename key ``src`` to ``dst``
        """
        if src == dst:
            return self.rename(src + "{" + src + "}", src)
        if not self.exists(src):
            return self.rename(src + "{" + src + "}", src)

        self.delete(dst)
        ktype = self.type(src)
        kttl = self.ttl(src)

        if ktype == b('none'):
            return False

        if ktype == b('string'):
            self.set(dst, self.get(src))
        elif ktype == b('hash'):
            self.hmset(dst, self.hgetall(src))
        elif ktype == b('list'):
            for k in self.lrange(src, 0, -1):
                self.rpush(dst, k)
        elif ktype == b('set'):
            for k in self.smembers(src):
                self.sadd(dst, k)
        elif ktype == b('zset'):
            for k, v in self.zrange(src, 0, -1, withscores=True):
                self.zadd(dst, v, k)

        # Handle keys with an expire time set
        kttl = -1 if kttl is None or kttl < 0 else int(kttl)
        if kttl != -1:
            self.expire(dst, kttl)

        return self.delete(src)