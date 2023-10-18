def tuple_signature_for_components(components: Sequence[Mapping[str, Any]]) -> str:
        """Equivalent to ``function_signature_for_name_and_inputs('', components)``."""
        ts = []
        for c in components:
            t: str = c['type']
            if t.startswith('tuple'):
                assert len(t) == 5 or t[5] == '['
                t = SolidityMetadata.tuple_signature_for_components(c['components']) + t[5:]
            ts.append(t)
        return f'({",".join(ts)})'