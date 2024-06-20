#!/usr/bin/env bash

SERVER_PATH={0}/

/usr/bin/screen -dmS server_screen /bin/bash -c "LD_LIBRARY_PATH=$SERVER_PATH ${SERVER_PATH}bedrock_server"
/usr/bin/screen -rD server_screen -X multiuser on
/usr/bin/screen -rD server_screen -X acladd root