def _validateDirectives(self, directiveList, checkFileName):

        if len(directiveList) == 0:
            raise ParsingException("'{file}' does not contain any CHECK directives".format(file=checkFileName))

        from . import Directives
        """
            We should enforce for every CHECK-NOT and CHECK-NOT-L directive that the next directive (if it exists) is
            a CHECK or CHECK-L directive
        """
        last = len(directiveList) -1
        supportedDirectives = [ Directives.Check, Directives.CheckLiteral ]
        for (index,directive) in enumerate(directiveList):
            if isA(directive, [Directives.CheckNot, Directives.CheckNotLiteral]):
                if index < last:
                    after = directiveList[index +1]
                    if not isA(after, supportedDirectives):
                        requiredTypes = " or ".join( [ "CHECK{suffix}".format(suffix=d.directiveToken()) for d in supportedDirectives])
                        raise ParsingException("{directive} must have a {requiredTypes} directive after it instead of a {bad}".format(
                                                  directive=directive,
                                                  requiredTypes=requiredTypes,
                                                  check=Directives.Check.directiveToken(),
                                                  bad=after)
                                              )