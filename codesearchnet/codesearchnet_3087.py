def console(self):
        """starts to interact (starts interactive console) Something like code.InteractiveConsole"""
        while True:
            if six.PY2:
                code = raw_input('>>> ')
            else:
                code = input('>>>')
            try:
                print(self.eval(code))
            except KeyboardInterrupt:
                break
            except Exception as e:
                import traceback
                if DEBUG:
                    sys.stderr.write(traceback.format_exc())
                else:
                    sys.stderr.write('EXCEPTION: ' + str(e) + '\n')
                time.sleep(0.01)