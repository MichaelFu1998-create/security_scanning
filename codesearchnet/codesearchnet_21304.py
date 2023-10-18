def pipe_worker(pipename, filename, object_type, query, format_string, unique=False):
    """
        Starts the loop to provide the data from jackal.
    """
    print_notification("[{}] Starting pipe".format(pipename))
    object_type = object_type()
    try:
        while True:
            uniq = set()
            # Remove the previous file if it exists
            if os.path.exists(filename):
                os.remove(filename)

            # Create the named pipe
            os.mkfifo(filename)
            # This function will block until a process opens it
            with open(filename, 'w') as pipe:
                print_success("[{}] Providing data".format(pipename))
                # Search the database
                objects = object_type.search(**query)
                for obj in objects:
                    data = fmt.format(format_string, **obj.to_dict())
                    if unique:
                        if not data in uniq:
                            uniq.add(data)
                            pipe.write(data + '\n')
                    else:
                        pipe.write(data + '\n')
            os.unlink(filename)
    except KeyboardInterrupt:
        print_notification("[{}] Shutting down named pipe".format(pipename))
    except Exception as e:
        print_error("[{}] Error: {}, stopping named pipe".format(e, pipename))
    finally:
        os.remove(filename)