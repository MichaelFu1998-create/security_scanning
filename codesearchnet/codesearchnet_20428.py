def _expand_targets(self, targets, base_dir=None):
        """ Expand targets by looking for '-r' in targets. """
        all_targets = []

        for target in targets:
            target_dirs = [p for p in [base_dir, os.path.dirname(target)] if p]
            target_dir = target_dirs and os.path.join(*target_dirs) or ''
            target = os.path.basename(target)
            target_path = os.path.join(target_dir, target)

            if os.path.exists(target_path):
                all_targets.append(target_path)

                with open(target_path) as fp:
                    for line in fp:
                        if line.startswith('-r '):
                            _, new_target = line.split(' ', 1)
                            all_targets.extend(self._expand_targets([new_target.strip()], base_dir=target_dir))

        return all_targets