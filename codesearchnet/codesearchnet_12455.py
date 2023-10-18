def wrap_name(name):
        """Wraps SkillName:entity into SkillName:{entity}"""
        if ':' in name:
            parts = name.split(':')
            intent_name, ent_name = parts[0], parts[1:]
            return intent_name + ':{' + ':'.join(ent_name) + '}'
        else:
            return '{' + name + '}'