# Environment
* Python 3.x
* Docker Desktop

# Build project
1. Pull this repository to local
2. Open command line tool, and navigate to project root folder.
3. Run "docker-compose pull app" to get docker image from docker hub.
4. Run "docker-compose up" to initial a container and start service.
5. Keep the service running to do the following tests.

# Automated Test
1. Run "docker exec -it change_password_app_1 /bin/bash" to login container, "change_password_app_1" is the container name.
2. Run "pytest tests/test_app.py -v" in the container to see api test result.
3. Run "pytest tests/test_func.py -v" in the container to see function unit test result.
4. Run "exit" to leave container.

# Manual Test by Simple Script
1. Run "docker exec -it change_password_app_1 /bin/bash" to login container, "change_password_app_1" is the container name.
2. Run "python change_password.py %old_password% %new_password%", please replace variables with your passwords.
3. Example: "python change_password.py my_old_password 1qaz@WSX3edc#RFV5tgb", and you should see success result.
4. Please escape special characters if needed when you run this script on command line tool.
