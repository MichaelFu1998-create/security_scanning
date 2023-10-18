def compose_containerized_launch_cmd(self, filepath, engine_dir, container_image):
        """Reads the json contents from filepath and uses that to compose the engine launch command.

        Notes: Add this to the ipengine launch for debug logs :
                          --log-to-file --debug
        Args:
            filepath (str): Path to the engine file
            engine_dir (str): CWD for the engines .
            container_image (str): The container to be used to launch workers
        """
        self.engine_file = os.path.expanduser(filepath)
        uid = str(uuid.uuid4())
        engine_json = None
        try:
            with open(self.engine_file, 'r') as f:
                engine_json = f.read()

        except OSError as e:
            logger.error("Could not open engine_json : ", self.engine_file)
            raise e

        return """mkdir -p {0}
cd {0}
cat <<EOF > ipengine.{uid}.json
{1}
EOF

DOCKER_ID=$(docker create --network host {2} ipengine --file=/tmp/ipengine.{uid}.json) {debug_option}
docker cp ipengine.{uid}.json $DOCKER_ID:/tmp/ipengine.{uid}.json

# Copy current dir to the working directory
DOCKER_CWD=$(docker image inspect --format='{{{{.Config.WorkingDir}}}}' {2})
docker cp -a . $DOCKER_ID:$DOCKER_CWD
docker start $DOCKER_ID

at_exit() {{
  echo "Caught SIGTERM/SIGINT signal!"
  docker stop $DOCKER_ID
}}

trap at_exit SIGTERM SIGINT
sleep infinity
""".format(engine_dir, engine_json, container_image, debug_option=self.debug_option, uid=uid)