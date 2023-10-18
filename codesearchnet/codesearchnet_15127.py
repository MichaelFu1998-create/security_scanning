def _start(self):
        """Initialize the parsing process."""
        self._instruction_library = self._spec.new_default_instructions()
        self._as_instruction = self._instruction_library.as_instruction
        self._id_cache = {}
        self._pattern_set = None
        self._inheritance_todos = []
        self._instruction_todos = []