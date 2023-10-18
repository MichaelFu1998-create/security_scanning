def memberness(context):
    '''The likelihood that the context is a "member".'''
    if context:
        texts = context.xpath('.//*[local-name()="explicitMember"]/text()').extract()
        text = str(texts).lower()

        if len(texts) > 1:
            return 2
        elif 'country' in text:
            return 2
        elif 'member' not in text:
            return 0
        elif 'successor' in text:
            # 'SuccessorMember' is a rare case that shouldn't be treated as member
            return 1
        elif 'parent' in text:
            return 2
    return 3