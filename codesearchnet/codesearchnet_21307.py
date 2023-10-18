def main():
    """
        Loads the config and handles the workers.
    """
    config = Config()
    pipes_dir = config.get('pipes', 'directory')
    pipes_config = config.get('pipes', 'config_file')
    pipes_config_path = os.path.join(config.config_dir, pipes_config)
    if not os.path.exists(pipes_config_path):
        print_error("Please configure the named pipes first")
        return

    workers = create_pipe_workers(pipes_config_path, pipes_dir)
    if workers:
        for worker in workers:
            worker.start()

        try:
            for worker in workers:
                worker.join()
        except KeyboardInterrupt:
            print_notification("Shutting down")
            for worker in workers:
                worker.terminate()
                worker.join()