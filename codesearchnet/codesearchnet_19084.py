def token_is_valid(self,):
        """Check the validity of the token :3600s
        """
        elapsed_time = time.time() - self.token_time
        logger.debug("ELAPSED TIME : {0}".format(elapsed_time))
        if elapsed_time > 3540: # 1 minute before it expires
            logger.debug("TOKEN HAS EXPIRED")
            return False

        logger.debug("TOKEN IS STILL VALID")
        return True