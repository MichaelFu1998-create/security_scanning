def block_to_fork(block_number):
    """ Convert block number to fork name.

        :param block_number: block number
        :type block_number: int
        :return: fork name
        :rtype: str

        Example use::

            >>> block_to_fork(0)
            ...
            "frontier"
            >>> block_to_fork(4370000)
            ...
            "byzantium"
            >>> block_to_fork(4370001)
            ...
            "byzantium"
    """
    forks_by_block = {
        0: "frontier",
        1150000: "homestead",
        # 1920000 Dao 
        2463000: "tangerine_whistle",
        2675000: "spurious_dragon",
        4370000: "byzantium",
        #7280000: "constantinople", # Same Block as petersburg, commented to avoid conflicts
        7280000: "petersburg",
        9999999: "serenity"  # to be replaced after Serenity launch
    }
    fork_names = list(forks_by_block.values())
    fork_blocks = list(forks_by_block.keys())
    return fork_names[bisect(fork_blocks, block_number) - 1]