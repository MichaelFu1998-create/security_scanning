def parse_args(self, ctx, args):
        """Parse arguments sent to this command.

        The code for this method is taken from MultiCommand:
        https://github.com/mitsuhiko/click/blob/master/click/core.py

        It is Copyright (c) 2014 by Armin Ronacher.
        See the license:
        https://github.com/mitsuhiko/click/blob/master/LICENSE
        """
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            click.echo(ctx.get_help())
            ctx.exit()
        return super(ActionSubcommand, self).parse_args(ctx, args)