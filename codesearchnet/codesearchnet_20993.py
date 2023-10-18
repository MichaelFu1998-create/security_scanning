def require_active_token(object):
    """
    Raise an ApiUsageError if the given object is not a token that is currently 
    participating in the game.  To be participating in the game, the given 
    token must have an id number and be associated with the world.
    """
    require_token(object)
    token = object

    if not token.has_id:
        raise ApiUsageError("""\
                token {token} should have an id, but doesn't.

                This error usually means that a token was added to the world 
                without being assigned an id number.  To correct this, make 
                sure that you're using a message (i.e. CreateToken) to create 
                all of your tokens.""")

    if not token.has_world:
        raise ApiUsageError("""\
                token {token} (id={token.id}) not in world.

                You can get this error if you try to remove the same token from 
                the world twice.  This might happen is you don't get rid of 
                every reference to a token after it's removed the first time, 
                then later on you try to remove the stale reference.""")