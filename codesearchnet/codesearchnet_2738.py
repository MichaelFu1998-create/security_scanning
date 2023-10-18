def call_editor(file_path):
  '''
  call editor
  '''
  EDITOR = os.environ.get('EDITOR', 'vim')
  with open(file_path, 'r+') as tf:
    call([EDITOR, tf.name])