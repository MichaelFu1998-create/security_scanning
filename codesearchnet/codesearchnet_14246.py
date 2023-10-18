def shoebot_example(**shoebot_kwargs):
    """
    Decorator to run some code in a bot instance.
    """

    def decorator(f):
        def run():
            from shoebot import ShoebotInstallError  # https://github.com/shoebot/shoebot/issues/206
            print("    Shoebot - %s:" % f.__name__.replace("_", " "))
            try:
                import shoebot
                outputfile = "/tmp/shoebot-%s.png" % f.__name__
                bot = shoebot.create_bot(outputfile=outputfile)
                f(bot)
                bot.finish()
                print('        [passed] : %s' % outputfile)
                print('')
            except ShoebotInstallError as e:
                print('        [failed]', e.args[0])
                print('')
            except Exception:
                print('        [failed] - traceback:')
                for line in traceback.format_exc().splitlines():
                    print('    %s' % line)
                print('')

        return run

    return decorator