def main(world_cls, referee_cls, gui_cls, gui_actor_cls, ai_actor_cls,
        theater_cls=PygletTheater, default_host=DEFAULT_HOST,
        default_port=DEFAULT_PORT, argv=None):
    """
Run a game being developed with the kxg game engine.

Usage:
    {exe_name} sandbox [<num_ais>] [-v...]
    {exe_name} client [--host HOST] [--port PORT] [-v...]
    {exe_name} server <num_guis> [<num_ais>] [--host HOST] [--port PORT] [-v...] 
    {exe_name} debug <num_guis> [<num_ais>] [--host HOST] [--port PORT] [-v...]
    {exe_name} --help

Commands:
    sandbox
        Play a single-player game with the specified number of AIs.  None of 
        the multiplayer machinery will be used.

    client
        Launch a client that will try to connect to a server on the given host 
        and port.  Once it connects and the game starts, the client will allow 
        you to play the game against any other connected clients.

    server
        Launch a server that will manage a game between the given number of 
        human and AI players.  The human players must connect using this 
        command's client mode.

    debug
        Debug a multiplayer game locally.  This command launches a server and 
        the given number of clients all in different processes, and configures 
        the logging system such that the output from each process can be easily 
        distinguished.

Arguments:
    <num_guis>
        The number of human players that will be playing the game.  Only needed 
        by commands that will launch some sort of multiplayer server.

    <num_ais>
        The number of AI players that will be playing the game.  Only needed by 
        commands that will launch single-player games or multiplayer servers.

Options:
    -x --host HOST          [default: {default_host}]
        The address of the machine running the server.  Must be accessible from 
        the machines running the clients.

    -p --port PORT          [default: {default_port}]
        The port that the server should listen on.  Don't specify a value less 
        than 1024 unless the server is running with root permissions.

    -v --verbose 
        Have the game engine log more information about what it's doing.  You 
        can specify this option several times to get more and more information.

This command is provided so that you can start writing your game with the least 
possible amount of boilerplate code.  However, the clients and servers provided 
by this command are not capable of running a production game.  Once you have 
written your game and want to give it a polished set of menus and options, 
you'll have to write new Stage subclasses encapsulating that logic and you'll 
have to call those stages yourself by interacting more directly with the 
Theater class.  The online documentation has more information on this process.
    """
    import sys, os, docopt, nonstdlib

    exe_name = os.path.basename(sys.argv[0])
    usage = main.__doc__.format(**locals()).strip()
    args = docopt.docopt(usage, argv or sys.argv[1:])
    num_guis = int(args['<num_guis>'] or 1)
    num_ais = int(args['<num_ais>'] or 0)
    host, port = args['--host'], int(args['--port'])

    logging.basicConfig(
            format='%(levelname)s: %(name)s: %(message)s',
            level=nonstdlib.verbosity(args['--verbose']),
    )

    # Use the given game objects and command line arguments to play a game!

    if args['debug']:
        print("""\
****************************** KNOWN BUG WARNING ******************************
In debug mode, every message produced by the logging system gets printed twice.
I know vaguely why this is happening, but as of yet I've not been able to fix
it.  In the mean time, don't let this confuse you!
*******************************************************************************""")
        game = MultiplayerDebugger(
                world_cls, referee_cls, gui_cls, gui_actor_cls, num_guis,
                ai_actor_cls, num_ais, theater_cls, host, port)
    else:
        game = theater_cls()
        ai_actors = [ai_actor_cls() for i in range(num_ais)]

        if args['sandbox']:
            game.gui = gui_cls()
            game.initial_stage = UniplayerGameStage(
                    world_cls(), referee_cls(), gui_actor_cls(), ai_actors)
            game.initial_stage.successor = PostgameSplashStage()

        if args['client']:
            game.gui = gui_cls()
            game.initial_stage = ClientConnectionStage(
                    world_cls(), gui_actor_cls(), host, port)

        if args['server']:
            game.initial_stage = ServerConnectionStage(
                    world_cls(), referee_cls(), num_guis, ai_actors,
                    host, port)

    game.play()