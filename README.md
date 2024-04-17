Hello, welcome to Learn Together, author email: tankoman228@gmail.com

dP                                            
88                                            
88        .d8888b. .d8888b. 88d888b. 88d888b. 
88        88ooood8 88'  `88 88'  `88 88'  `88 
88        88.  ... 88.  .88 88       88    88 
88888888P `88888P' `88888P8 dP       dP    dP 
oooooooooooooooooooooooooooooooooooooooooooooo
                                              
d888888P                              dP   dP                         
   88                                 88   88                         
   88    .d8888b. .d8888b. .d8888b. d8888P 88d888b. .d8888b. 88d888b. 
   88    88'  `88 88'  `88 88ooood8   88   88'  `88 88ooood8 88'  `88 
   88    88.  .88 88.  .88 88.  ...   88   88    88 88.  ... 88       
   dP    `88888P' `8888P88 `88888P'   dP   dP    dP `88888P' dP       
ooooooooooooooooooo~~~~.88~ooooooooooooooooooooooooooooooooooooooooooo
                   d8888P      


To launch this server you need to be in same directory where main.py is. You need to start main.py after installing all the packages and mariaDB. You can launch it on windows 10 or Ubuntu, tested with python 3.8. If you have no mobile client .apk, write me there -> tankoman228@gmail.com

///Args for all commands are divided with whitespace.

1. First you need to install packages (uvicorn, fastapi, sqlalchemy, pymysql). Install MariaDB or mySQL (MariaDB is better for this app)

2. Then write connection data to config.json, don't use ROOT user to connect! Also correct "local_ip"

3. Use "recreate_db" to create database for this app

4. To start you need to create a group, use
$create_group <group name>

5. Then create some register tokens by
$create_token <id_group> <id_role> <token_string>

ID of first group from the database is usually "1"
Role is role of user, this token is used to register or to join created group, first user is better to be Owner (ID 3)
Use "roles" to get list of roles

6. After you can "start" server, after that your server can do http. If it doesn't work, check config.json

7. If you do not want to write "start" every time just add it to start_commands.txt, all commands from this file are executed before starting

8. Use register tokens to register on your server from mobile client

9. Control this system using commands you can find with "help full"