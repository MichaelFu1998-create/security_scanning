def old_lambdef(self, lambda_loc, args_opt, colon_loc, body):
        """(2.6, 2.7) old_lambdef: 'lambda' [varargslist] ':' old_test"""
        if args_opt is None:
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))