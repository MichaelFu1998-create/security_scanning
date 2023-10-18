def get_poll_func():
    """Get the best available socket poll function
    
    :return: poller function
    """
    if hasattr(select, 'epoll'):
        poll_func = epoll_poller
    elif hasattr(select, 'poll'):
        poll_func = asyncore.poll2
    else:
        poll_func = asyncore.poll
    return poll_func