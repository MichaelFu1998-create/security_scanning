def deref(self, ctx):
        """
        Returns the value this reference is pointing to. This method uses 'ctx' to resolve the reference and return
        the value this reference references.
        If the call was already made, it returns a cached result.
        It also makes sure there's no cyclic reference, and if so raises CyclicReferenceError.
        """
        if self in ctx.call_nodes:
            raise CyclicReferenceError(ctx, self)

        if self in ctx.cached_results:
            return ctx.cached_results[self]

        try:
            ctx.call_nodes.add(self)
            ctx.call_stack.append(self)

            result = self.evaluate(ctx)
            ctx.cached_results[self] = result
            return result
        except:
            if ctx.exception_call_stack is None:
                ctx.exception_call_stack = list(ctx.call_stack)
            raise
        finally:
            ctx.call_stack.pop()
            ctx.call_nodes.remove(self)