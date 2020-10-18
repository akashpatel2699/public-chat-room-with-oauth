# Public Chat Room
This application has one public room that is shared by all other clients and able to see each others chatting and the chat is stored in a database for later use.
This application is build using **Python Flask**, **React**, **Flask Socketio**, **Socket.io-Client**, and **Postgresql** to store chats.

## Requirements 

All the requirements that needs to be installed has been added to the requirements.txt that includes:
* [python_dotenv](https://pypi.org/project/python-dotenv/) - useful for loading environment variables
* [flask](https://flask.palletsprojects.com/en/1.1.x/) - Python micro web-framework
* [requests](https://requests.readthedocs.io/en/master/) - Python HTTP library useful for making API Calls 
* [heroku](https://devcenter.heroku.com/categories/python-support) - Cloud based web hosting for **FREE**
* [React](https://reactjs.org/) - Front-end framework 
* [Socketio.client](https://socket.io/docs/) - enables communication between client and server
* [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/) - enables communication between server and client
* [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - simplfy use of
[SQLALCHEMY](https://www.sqlalchemy.org/) with flask
* [openweathermap](https://openweathermap.org/) - **Free** weather API 

# Set up React  
1. `clone git https://github.com/NJIT-CS490/project2-m1-amp228.git && cd project2-m1-amp228`    
2. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`  
  g) `pip install -r requirements.txt`
    
    :warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    
3. create a file called **sql.env** to store your database credential for later use and for any other API keys.
    `touch sql.env`. **NOW** follow **GETTING PSQL TO WORK WITH PYTHON** AND **SETTING UP  PSQL** AND 
**ENABLING read/write from SQLAlchemy**. After completing these steps your can move forward with **step 4** 
4. In order for !! weather bot command to work, you will have to sign up for **openweathermap** API
using [sign up](https://home.openweathermap.org/users/sign_up) and your 
[follow up email](https://openweathermap.org/appid) will have 
your API  key needed to make a call for weather information.
5. Open your **sql.env** file and insert the following  lines in it and after that you will have two entries in the 
 file. 
`DATABASE_URL=postgresql://<username>:<password>@localhost/postgres` 
`OPEN_WEATHER_API_KEY=<yourAPIKEY>`.
Username and password your created in **step 7 of setting up PSQL**.
Your API key will be in your email after signing up for API and if not you and go to their [website](https://home.openweathermap.org/users/sign_in)
and then CLick on **API Keys** and the key will be under **Key** column. Insert that for yourAPIKEY.

6. cd into the directory you cloned not already by typing `cd project2-m1-amp228`. Now we need to run   
   **webpack** in order for react code to converted into *javascript* for our index file to use.
`run npm watch`.
 7. Now webpack running, **open a new terminal** and make sure your are in that same directory, just in case
 8. type `cd project2-m1-amp228` and now run the server using **python app.py**
 9. To see your application interface, **In cloud9**, click on Preview next to the Green Run button on **Top**.
    After that click **Preview Running Application** and that will open in the same tab **BUT** if you want to
    open in a new tab then click on the arrow button in the top **right corner** of that screen.

# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo pipinstall --upgrade pip`  
3. Get psycopg2: `sudo pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    :warning: :warning: :warning: If you get an error saying "could not change directory", that's 
    okay! It worked! :warning: :warning: :warning:    
5. Make a new database: `sudo -u postgres createdb $USER`    
        :warning: :warning: :warning: If you get an error saying "could not change directory", 
        that's okay! It worked! :warning: :warning: :warning:    
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `lect11` and make a new file called `sql.env` and add `SQL_USER=` and `SQL_PASSWORD=` in it  
9. Fill in those values with the values you put in 7. b)  
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application (might have to clear your cache by doing a hard refresh)    


## Issues

##### Technical Issues
* When creating random users, I was getting curly braces show up on the screen around username as well 
as in the database. I later found out that function that generate random username was returing a list
and I was passing that as my username.

* On the client side in React, When listening for socketio event using .on function, it would make 
receive multiple event so I had to destroy the listener later that would solve the issue of multiple 
event being heard. I had to do bit of google search as well as look back at the lect11-starter 
to solve the issue.

* Creating Bot functions, I was getting an unathorized error when making an API call to fun translate 
 to translate the message. I was using one of their paid endpoints that was resulting in an error. After 
googling and reading chat messages on **Slack**, I didn't find my answer but fortunately try different 
endpoint work and I was getting response back from the API call.

* On front-end, When in the Message component that takes a prop as Message object that contains the username,
  message, and time when it was created, I was using javascript method map to loop over the list of objects.
It was throwing an error called "object are not valid as a React Child". I tried myseld to find an solution by 
going back and forward in the components files and I think I was restructuring  the object message in the Message 
component wrong and after an hour I was able to resolved by just accepting the prop as an object instead of restructuring.

* I spent lot of time styling the application as I had to plug and play to see the effect of it as I would run into
  problem most of the times. It would do complete opposite than I wanted on most occasion. I had to visit 
  [w3school](https://www.w3schools.com/html/html_css.asp) many time to fix my styling and I still thought I could 
  have done better if I had use their css library that makes styling much easier.

## Improvements
* If I had more time then I would have implemented an API for random jokes so when client types 
 !! jokes, the server will make an api call to fetch a random joke and send it to all clients 
 and also store it in the database for persistence. 
* I wanted to use external css library such w3school to make my application responsive as well
 as look appealing to the client. I started using that library but it would have required me to change 
 most of my scripts files to add classNames and then plug and play after getting classNames setup. 
* I wanted to use enum for my bot commands as it looks clean and better to use it to avoid making 
 spelling mistake after seeing lect12 where profesor shows us an example of how using enum make 
life easier. I thought of using it but lack of time forced to use simple const on the top and use
and in some cases leave what I had (mess) as it is. 

FAQ
---

Q: After typing **psql**, I am asked for password and I tried all password which didn't work?

A: Login in with the user you created in stept **7** and then change your $USER(what your local user is)
 password after loging in. 
 `psql -d postgres -U <the user you created>`. Now that you logged in type:
 `ALTER USER "yourLocalUser" WITH PASSWORD <new password for ec2-user>`;
 

---

Q: What is the use of Procfile?

A: A Procfile is used to deploy application on **heroku** and that tells heroku how to run your application.

---

Q: What is the use of  requirements.txt?

A: A requirements.txt file has all the python library installed and/or needed to run your application so you want to run 
`pip install -r requirements` to make sure you have all that it takes to run smooth.

---