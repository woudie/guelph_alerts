# Guelph Alerts


<img style="float: right; margin: 20px;" src="flaskr/static/Assets/Logo/guelph_alert_logo.png">

## Background

Guelph Alerts was a fun little tool that I built while learning how to use flask. It is basically a course availability notifier, where a user registers for courses, at most 5 at a time, that they are not able to take because of capacity. The user is notified the asap when space is available via email. This app is built to work for University of Guelph students and to an extent University of Guelph Humber students (i think). Since I am still a beginner developer, I implemented a few restrictions to try to ensure the application does crash. These restrictions include:

- A user can only repeatly register for 2 week periods. They cannot unregister during the 2 weeks or register for additional courses if they did not initially pick 5 courses. They have to wait for the 2 week period and there is no notification from Guelph Alerts when the 2 week period is up, so the user has to keep track themselves. 
- The user can only register for a maximum of 5 courses per registeration period.

Both of these are restriction implemented due to the fact I do not know how to build scalable web applications (yet, its on the list of things to learn). I may come back down the road and improve it.

## Installation

You need to use python2.7, yes I know it is no longer supported, but I built the application with it. I did try to run with python3 and equivalent packages and apscheduler seems to behave weirdly each time I tried (using python3.6), so you can try youeself, but it might fail.

All relevant packages are contained in requirements.txt 

To install everything correctly, follow these steps:

1. Ensure you are using python2.7
   - You can verify by running `python --version`
2. Install virtualenv using `python -m pip install virtualenv`
3. Create a virtual env using `virtualenv {env_name}`
    - replace {env_name} with whatever you want to name the virtual environment
4. Enter the virtualenv using `source {env_name}/bin/activate`, where {env_name} is the name you chose in step 3
5. Install all dependencies using `pip install -r requirements.txt`
   - Ensure you are in projects root directory

If you made it this far, congratulations, you have successfully installed all the dev dependencies for Guelph Alerts!

## Launch Guelph Alerts

In order to keep sensitive details hidden, Guelph Alerts reads password and username/email data from environment variables set locally by the user.

For the emailing service, we use yagmail to utilize a gmail account. The relevant yagmail environment variables needed are `EMAIL` for the email and `EMAIL_PASSWORD` for the email password. 

We also use MongoDB Atlas as our database provider. The relevant environment variables needed are `DB_USER` for the database user and `DB_PASSWORD` for the database password. You will also need to create a new database in MongoDB Atlas called `GuelphAlerts` in order for the uri to work. Alternatively, you can use a different DB name or different provider all together, but you will need to swap out the uri and authentication method.

Setting the environment variables over and over again after each terminal session can get annoying. To avoid that, copy and paste the small script below into a file called `env.sh` and alter the relevant information. After that, simply run `sudo ./env.sh` each time you want to set the environment variables.

Once you have the environment variables configured, simply run `gunicorn -w 4 "flaskr:create_app()" --preload` in the virtualenv and GuelphAlerts should launch running 4 workers on port 8000. If you want to verify, enter `http://localhost:8000` in your browser and the page should load.

If you have any questions or concerns regarding the application, you can email me at [tieria.dev@gmail.com](tieria.dev@gmail.com)