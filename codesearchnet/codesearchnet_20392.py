def package_changes(self, name, current_version, new_version):
        """
          List of changes for package name from current_version to new_version, in descending order.
          If current version is higher than new version (downgrade), then a minus sign will be prefixed to each change.
        """
        if pkg_resources.parse_version(current_version) > pkg_resources.parse_version(new_version):
            downgrade_sign = '- '
            (current_version, new_version) = (new_version, current_version)
        else:
            downgrade_sign = None

        changes = self._package_changes(name, current_version, new_version)

        if changes and downgrade_sign:
            changes = [downgrade_sign + c for c in changes]

        return changes