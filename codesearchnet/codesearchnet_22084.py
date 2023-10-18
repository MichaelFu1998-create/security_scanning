def _hyphens_to_dashes(self):
      """Transform hyphens to various kinds of dashes"""

      problematic_hyphens = [(r'-([.,!)])', r'---\1'),
                             (r'(?<=\d)-(?=\d)', '--'),
                             (r'(?<=\s)-(?=\s)', '---')]

      for problem_case in problematic_hyphens:
          self._regex_replacement(*problem_case)