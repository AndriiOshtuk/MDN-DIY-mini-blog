# MDN-DIY-mini-blog
DIY mini blog assignment done as final step of MDN tutorial.

## Overview

This is a simple blog built with Python and Django.

## Features
* There are models for blogger, post, comment
* All users could see list of posts and bloggers 
* All users could see individual posts with comments and dedicated blogger page
* Logged-in users can leave comments for posts
* Users can log in, log out and reset password
* Admin users can create and manage models
* Project documentation is available via the admin interface 
* All events/issues above DJANGO_LOG_LEVEL are sent both to console and Sentry

## Technologies
* Django 3.0
* Python 3.6
* Heroku
* SendGrid
* sqlite3
* admindocs
* Sentry

## Check it out
The application is available at https://mdn-diy-mini-blog.herokuapp.com  
  
Use test user credentials:
```
  $ User: testuser
  $ Password: testpassword
```

**Note:** It may take few minutes for Heroku to reload app.
