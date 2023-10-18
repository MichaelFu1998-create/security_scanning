def _make_package(args):  # pragma: no cover
    """Prepare transcriptiondata from the transcription sources."""
    from lingpy.sequence.sound_classes import token2class
    from lingpy.data import Model

    columns = ['LATEX', 'FEATURES', 'SOUND', 'IMAGE', 'COUNT', 'NOTE']
    bipa = TranscriptionSystem('bipa')
    for src, rows in args.repos.iter_sources(type='td'):
        args.log.info('TranscriptionData {0} ...'.format(src['NAME']))
        uritemplate = URITemplate(src['URITEMPLATE']) if src['URITEMPLATE'] else None
        out = [['BIPA_GRAPHEME', 'CLTS_NAME', 'GENERATED', 'EXPLICIT',
                'GRAPHEME', 'URL'] + columns]
        graphemes = set()
        for row in rows:
            if row['GRAPHEME'] in graphemes:
                args.log.warn('skipping duplicate grapheme: {0}'.format(row['GRAPHEME']))
                continue
            graphemes.add(row['GRAPHEME'])
            if not row['BIPA']:
                bipa_sound = bipa[row['GRAPHEME']]
                explicit = ''
            else:
                bipa_sound = bipa[row['BIPA']]
                explicit = '+'
            generated = '+' if bipa_sound.generated else ''
            if is_valid_sound(bipa_sound, bipa):
                bipa_grapheme = bipa_sound.s
                bipa_name = bipa_sound.name
            else:
                bipa_grapheme, bipa_name = '<NA>', '<NA>'
            url = uritemplate.expand(**row) if uritemplate else row.get('URL', '')
            out.append(
                [bipa_grapheme, bipa_name, generated, explicit, row['GRAPHEME'],
                 url] + [
                    row.get(c, '') for c in columns])
        found = len([o for o in out if o[0] != '<NA>'])
        args.log.info('... {0} of {1} graphemes found ({2:.0f}%)'.format(
            found, len(out), found / len(out) * 100))
        with UnicodeWriter(
            pkg_path('transcriptiondata', '{0}.tsv'.format(src['NAME'])), delimiter='\t'
        ) as writer:
            writer.writerows(out)

    count = 0
    with UnicodeWriter(pkg_path('soundclasses', 'lingpy.tsv'), delimiter='\t') as writer:
        writer.writerow(['CLTS_NAME', 'BIPA_GRAPHEME'] + SOUNDCLASS_SYSTEMS)
        for grapheme, sound in sorted(bipa.sounds.items()):
            if not sound.alias:
                writer.writerow(
                    [sound.name, grapheme] + [token2class(
                        grapheme, Model(cls)) for cls in SOUNDCLASS_SYSTEMS])
                count += 1
    args.log.info('SoundClasses: {0} written to file.'.format(count))