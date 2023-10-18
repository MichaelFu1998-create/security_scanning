def path_from_keywords(keywords,into='path'):
    '''
    turns keyword pairs into path or filename 
    
    if `into=='path'`, then keywords are separted by underscores, else keywords are used to create a directory hierarchy
    '''
    subdirs = []
    def prepare_string(s):
        s = str(s)
        s = re.sub('[][{},*"'+f"'{os.sep}]",'_',s)#replace characters that make bash life difficult by underscore 
        if into=='file':
            s = s.replace('_', ' ')#Remove underscore because they will be used as separator
        if ' ' in s:
            s = s.title()
            s = s.replace(' ','')
        return s
    if isinstance(keywords,set):
        keywords_list = sorted(keywords)
        for property in keywords_list:
            subdirs.append(prepare_string(property))
    else:
        keywords_list = sorted(keywords.items())
        for property,value in keywords_list:  # @reservedassignment
            if Bool.valid(value):
                subdirs.append(('' if value else ('not_' if into=='path' else 'not'))+prepare_string(property))
            #elif String.valid(value):
            #    subdirs.append(prepare_string(value))
            elif (Float|Integer).valid(value):
                subdirs.append('{}{}'.format(prepare_string(property),prepare_string(value)))
            else:
                subdirs.append('{}{}{}'.format(prepare_string(property),'_' if into == 'path' else '',prepare_string(value)))
    if into == 'path':
        out = os.path.join(*subdirs)
    else:
        out = '_'.join(subdirs)
    return out