def set_pkg_verif_code(self, doc, code):
        """Sets the package verification code, if not already set.
        code - A string.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises Value error if doesn't match verifcode form
        """
        self.assert_package_exists()
        if not self.package_verif_set:
            self.package_verif_set = True
            match = self.VERIF_CODE_REGEX.match(code)
            if match:
                doc.package.verif_code = match.group(self.VERIF_CODE_CODE_GRP)
                if match.group(self.VERIF_CODE_EXC_FILES_GRP) is not None:
                    doc.package.verif_exc_files = match.group(self.VERIF_CODE_EXC_FILES_GRP).split(',')
                return True
            else:
                raise SPDXValueError('Package::VerificationCode')
        else:
            raise CardinalityError('Package::VerificationCode')