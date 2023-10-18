def translate_file(input_path, output_path):
    '''
    Translates input JS file to python and saves the it to the output path.
    It appends some convenience code at the end so that it is easy to import JS objects.

    For example we have a file 'example.js' with:   var a = function(x) {return x}
    translate_file('example.js', 'example.py')

    Now example.py can be easily importend and used:
    >>> from example import example
    >>> example.a(30)
    30
    '''
    js = get_file_contents(input_path)

    py_code = translate_js(js)
    lib_name = os.path.basename(output_path).split('.')[0]
    head = '__all__ = [%s]\n\n# Don\'t look below, you will not understand this Python code :) I don\'t.\n\n' % repr(
        lib_name)
    tail = '\n\n# Add lib to the module scope\n%s = var.to_python()' % lib_name
    out = head + py_code + tail
    write_file_contents(output_path, out)