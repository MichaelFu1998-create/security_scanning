def compile(pattern, flags, code, groups=0, groupindex={}, indexgroup=[None]):
    """Compiles (or rather just converts) a pattern descriptor to a SRE_Pattern
    object. Actual compilation to opcodes happens in sre_compile."""
    return SRE_Pattern(pattern, flags, code, groups, groupindex, indexgroup)