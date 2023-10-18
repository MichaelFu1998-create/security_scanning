def describeStats(stats, stream, title=None, details=True, totals=True, gettext=None):
  '''
  Renders an ASCII-table of the synchronization statistics `stats`,
  example output:

  .. code-block::

    +----------------------------------------------------------------------------------+
    |                                      TITLE                                       |
    +----------+------+-------------------------+--------------------------+-----------+
    |          |      |          Local          |          Remote          | Conflicts |
    |   Source | Mode |  Add  | Mod | Del | Err |   Add  | Mod | Del | Err | Col | Mrg |
    +----------+------+-------+-----+-----+-----+--------+-----+-----+-----+-----+-----+
    | contacts |  <=  |   -   |  -  |  -  |  -  | 10,387 |  -  |  -  |  -  |  -  |  -  |
    |     note |  SS  | 1,308 |  -  |   2 |  -  |    -   |  -  |  -  |  -  |  -  |  -  |
    +----------+------+-------+-----+-----+-----+--------+-----+-----+-----+-----+-----+
    |                  1,310 local changes and 10,387 remote changes.                  |
    +----------------------------------------------------------------------------------+

  :Parameters:

  stats : dict

    The synchronization stats returned by a call to Adapter.sync().

  stream : file-like-object

    An output file-like object that has at least a `write()` method,
    e.g. ``sys.stdout`` can be used.

  title : str, optional, default: null

    A title placed at the top of the table -- if omitted (the default),
    then no title is rendered.

  details : bool, optional, default: true

    If truthy, a per-datastore listing of changes will be displayed
    (as in the above example).

  totals : bool, optional, default: true

    If truthy, a summary of all changes will be displayed (as in the
    above example).

  gettext : callable, optional, @DEPRECATED(0.2.0), default: null

    A `gettext.gettext` compatible callable used for translating
    localized content (such as number formatting, etc.).

    NOTE: this parameter is deprecated, and will be replaced with
    a generalized i18n solution.
  '''

  from . import state
  modeStringLut = dict((
    (constants.SYNCTYPE_TWO_WAY,             '<>'),
    (constants.SYNCTYPE_SLOW_SYNC,           'SS'),
    (constants.SYNCTYPE_ONE_WAY_FROM_CLIENT, '->'),
    (constants.SYNCTYPE_REFRESH_FROM_CLIENT, '=>'),
    (constants.SYNCTYPE_ONE_WAY_FROM_SERVER, '<-'),
    (constants.SYNCTYPE_REFRESH_FROM_SERVER, '<='),
    ))

  if gettext is not None:
    _ = gettext
  else:
    _ = lambda s: s

  # todo: this does not handle the case where the title is wider than the table.

  wSrc  = len(_('Source'))
  wMode = len(_('Mode'))
  wCon  = len(_('Conflicts'))
  wCol  = len(_('Col'))
  wMrg  = len(_('Mrg'))
  wHereAdd = wPeerAdd = len(_('Add'))
  wHereMod = wPeerMod = len(_('Mod'))
  wHereDel = wPeerDel = len(_('Del'))
  wHereErr = wPeerErr = len(_('Err'))

  totLoc = 0
  totRem = 0
  totErr = 0
  totCol = 0
  totMrg = 0

  for key in stats.keys():
    wSrc  = max(wSrc, len(key))
    wMode = max(wMode, len(modeStringLut.get(stats[key].mode)))
    wCol  = max(wCol, len(num2str(stats[key].conflicts)))
    wMrg  = max(wMrg, len(num2str(stats[key].merged)))
    wHereAdd = max(wHereAdd, len(num2str(stats[key].hereAdd)))
    wPeerAdd = max(wPeerAdd, len(num2str(stats[key].peerAdd)))
    wHereMod = max(wHereMod, len(num2str(stats[key].hereMod)))
    wPeerMod = max(wPeerMod, len(num2str(stats[key].peerMod)))
    wHereDel = max(wHereDel, len(num2str(stats[key].hereDel)))
    wPeerDel = max(wPeerDel, len(num2str(stats[key].peerDel)))
    wHereErr = max(wHereErr, len(num2str(stats[key].hereErr)))
    wPeerErr = max(wPeerErr, len(num2str(stats[key].peerErr)))
    totLoc += stats[key].hereAdd + stats[key].hereMod + stats[key].hereDel
    totRem += stats[key].peerAdd + stats[key].peerMod + stats[key].peerDel
    totErr += stats[key].hereErr + stats[key].peerErr
    totCol += stats[key].conflicts
    totMrg += stats[key].merged

  # TODO: i'm 100% sure there is a python library that can do this for me...

  if wCon > wCol + 3 + wMrg:
    diff = wCon - ( wCol + 3 + wMrg )
    wCol += diff / 2
    wMrg = wCon - 3 - wCol
  else:
    wCon = wCol + 3 + wMrg

  if details:
    tWid = ( wSrc + 3 + wMode + 3
             + wHereAdd + wHereMod + wHereDel + wHereErr + 9 + 3
             + wPeerAdd + wPeerMod + wPeerDel + wPeerErr + 9 + 3
             + wCon )
  else:
    if title is None:
      tWid = 0
    else:
      tWid = len(title)

  if totals:
    # TODO: oh dear. from an i18n POV, this is *horrible*!...
    sumlist = []
    for val, singular, plural in [
      (totLoc, _('local change'), _('local changes')),
      (totRem, _('remote change'), _('remote changes')),
      (totErr, _('error'), _('errors')),
      ]:
      if val == 1:
        sumlist.append(num2str(val) + ' ' + singular)
      elif val > 1:
        sumlist.append(num2str(val) + ' ' + plural)
    if len(sumlist) <= 0:
      sumlist = _('No changes')
    elif len(sumlist) == 1:
      sumlist = sumlist[0]
    else:
      sumlist = ', '.join(sumlist[:-1]) + ' ' + _('and') + ' ' + sumlist[-1]
    if totMrg > 0 or totCol > 0:
      sumlist += ': '
      if totMrg == 1:
        sumlist += num2str(totMrg) + ' ' + _('merge')
      elif totMrg > 1:
        sumlist += num2str(totMrg) + ' ' + _('merges')
      if totMrg > 0 and totCol > 0:
        sumlist += ' ' + _('and') + ' '
      if totCol == 1:
        sumlist += num2str(totCol) + ' ' + _('conflict')
      elif totCol > 1:
        sumlist += num2str(totCol) + ' ' + _('conflicts')
    sumlist += '.'
    if len(sumlist) > tWid:
      wSrc += len(sumlist) - tWid
      tWid = len(sumlist)

  if title is not None:
    stream.write('+-' + '-' * tWid + '-+\n')
    stream.write('| {0: ^{w}}'.format(title, w=tWid))
    stream.write(' |\n')

  hline = '+-' \
          + '-' * wSrc \
          + '-+-' \
          + '-' * wMode \
          + '-+-' \
          + '-' * ( wHereAdd + wHereMod + wHereDel + wHereErr + 9 ) \
          + '-+-' \
          + '-' * ( wPeerAdd + wPeerMod + wPeerDel + wPeerErr + 9 )  \
          + '-+-' \
          + '-' * wCon \
          + '-+\n'

  if details:

    stream.write(hline)

    stream.write('| ' + ' ' * wSrc)
    stream.write(' | ' + ' ' * wMode)
    stream.write(' | {0: ^{w}}'.format(_('Local'), w=( wHereAdd + wHereMod + wHereDel + wHereErr + 9 )))
    stream.write(' | {0: ^{w}}'.format(_('Remote'), w=( wPeerAdd + wPeerMod + wPeerDel + wPeerErr + 9 )))
    stream.write(' | {0: ^{w}}'.format(_('Conflicts'), w=wCon))
    stream.write(' |\n')

    stream.write('| {0: >{w}}'.format(_('Source'), w=wSrc))
    stream.write(' | {0: >{w}}'.format(_('Mode'), w=wMode))
    stream.write(' | {0: ^{w}}'.format(_('Add'), w=wHereAdd))
    stream.write(' | {0: ^{w}}'.format(_('Mod'), w=wHereMod))
    stream.write(' | {0: ^{w}}'.format(_('Del'), w=wHereDel))
    stream.write(' | {0: ^{w}}'.format(_('Err'), w=wHereErr))
    stream.write(' | {0: ^{w}}'.format(_('Add'), w=wPeerAdd))
    stream.write(' | {0: ^{w}}'.format(_('Mod'), w=wPeerMod))
    stream.write(' | {0: ^{w}}'.format(_('Del'), w=wPeerDel))
    stream.write(' | {0: ^{w}}'.format(_('Err'), w=wPeerErr))
    stream.write(' | {0: ^{w}}'.format(_('Col'), w=wCol))
    stream.write(' | {0: ^{w}}'.format(_('Mrg'), w=wMrg))
    stream.write(' |\n')

    hsline = '+-' + '-' * wSrc \
             + '-+-' + '-' * wMode \
             + '-+-' + '-' * wHereAdd \
             + '-+-' + '-' * wHereMod \
             + '-+-' + '-' * wHereDel \
             + '-+-' + '-' * wHereErr \
             + '-+-' + '-' * wPeerAdd \
             + '-+-' + '-' * wPeerMod \
             + '-+-' + '-' * wPeerDel \
             + '-+-' + '-' * wPeerErr \
             + '-+-' + '-' * wCol \
             + '-+-' + '-' * wMrg \
             + '-+\n'

    stream.write(hsline)

    def numcol(val, wid):
      if val == 0:
        return ' | {0: ^{w}}'.format('-', w=wid)
      return ' | {0: >{w}}'.format(num2str(val), w=wid)

    for key in sorted(stats.keys(), key=lambda k: str(k).lower()):
      stream.write('| {0: >{w}}'.format(key, w=wSrc))
      stream.write(' | {0: ^{w}}'.format(modeStringLut.get(stats[key].mode), w=wMode))
      stream.write(numcol(stats[key].hereAdd, wHereAdd))
      stream.write(numcol(stats[key].hereMod, wHereMod))
      stream.write(numcol(stats[key].hereDel, wHereDel))
      stream.write(numcol(stats[key].hereErr, wHereErr))
      stream.write(numcol(stats[key].peerAdd, wPeerAdd))
      stream.write(numcol(stats[key].peerMod, wPeerMod))
      stream.write(numcol(stats[key].peerDel, wPeerDel))
      stream.write(numcol(stats[key].peerErr, wPeerErr))
      stream.write(numcol(stats[key].conflicts, wCol))
      stream.write(numcol(stats[key].merged, wMrg))
      stream.write(' |\n')

    stream.write(hsline)

  if totals:
    if title is None and not details:
      stream.write('+-' + '-' * tWid + '-+\n')
    stream.write('| {0: ^{w}}'.format(sumlist, w=tWid))
    stream.write(' |\n')
    stream.write('+-' + '-' * tWid + '-+\n')

  return