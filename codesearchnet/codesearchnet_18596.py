def main(path):
    '''scan path directory and any subdirectories for valid captain scripts'''
    basepath = os.path.abspath(os.path.expanduser(str(path)))

    echo.h2("Available scripts in {}".format(basepath))
    echo.br()
    for root_dir, dirs, files in os.walk(basepath, topdown=True):
        for f in fnmatch.filter(files, '*.py'):
            try:
                filepath = os.path.join(root_dir, f)

                # super edge case, this makes sure the python script won't start
                # an interactive console session which would cause the session
                # to start and not allow the for loop to complete
                with open(filepath, encoding="UTF-8") as fp:
                    body = fp.read()
                    is_console = "InteractiveConsole" in body
                    is_console = is_console or "code" in body
                    is_console = is_console and "interact(" in body
                    if is_console:
                        continue

                s = captain.Script(filepath)
                if s.can_run_from_cli():
                    rel_filepath = s.call_path(basepath)
                    p = s.parser

                    echo.h3(rel_filepath)

                    desc = p.description
                    if desc:
                        echo.indent(desc, indent=(" " * 4))

                    subcommands = s.subcommands
                    if subcommands:
                        echo.br()
                        echo.indent("Subcommands:", indent=(" " * 4))
                        for sc in subcommands.keys():
                            echo.indent(sc, indent=(" " * 6))

                    echo.br()

            except captain.ParseError:
                pass

            except Exception as e:
                #echo.exception(e)
                #echo.err("Failed to parse {} because {}", f, e.message)
                echo.err("Failed to parse {}", f)
                echo.verbose(e.message)
                echo.br()