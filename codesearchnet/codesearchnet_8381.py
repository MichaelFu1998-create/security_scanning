def env():
    """Verify BOARD variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("board.env: invalid SSH environment")
        return 1

    board = cij.env_to_dict(PREFIX, REQUIRED)   # Verify REQUIRED variables
    if board is None:
        cij.err("board.env: invalid BOARD environment")
        return 1

    board["CLASS"] = "_".join([board[r] for r in REQUIRED[:-1]])
    board["IDENT"] = "-".join([board["CLASS"], board["ALIAS"]])

    cij.env_export(PREFIX, EXPORTED, board)     # Export EXPORTED variables

    return 0