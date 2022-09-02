# cogs-challenge
Simple mobile backend api for quiz application


To run project you can proceed in two ways:
  * You can set up to run locally. Copy file ```.env.local``` to 
    ```.env``` and set connection parameters for database. 
    You could work on system python, but it's recommended to create 
    virtual environment and activate it. After that install dependencies with
    ```pip insall -r requirements.txt``` and run migration with
    ```python manage.py migrate```. And lastly, run 
    ```python manage.py runserver 0.0.0.0:8000``` (or choose other
    port to your liking). That's it, api should be up and running.
  * Other option is to run it through docker. Make sure you have 
    docker and docker-compose installed and enabled on your system. Start with copying
    ```.env.docker``` to ```.env```. You can modify these variables, but it 
    should work out of the box. Just run ```docker-compose up``` or 
    ```docker-compose up -d``` (if you want to run it detached from terminal),
    and that should be it, api should be up and running at configured port.
    (Default start, if left unchanged, uses port 8000)


# What's done in this project
  * Created models for users and endpoints for user registration, login, create and refresh tokens  
    ``baseurl/v1/users/register/`` - Create new user   
    ``baseurl/v1/users/login/`` - Login using username and password, get jwt access token to use in header
                                  and refresh_token to use when access_token expires  
    ``baseurl/v1/users/login/refresh/``  - Refresh access token
    ``baseurl/v1/users/me/`` - Get basic data for logged user
  
  * Models and endpoints for quizzes, questions and answers  
    Only basic authorization is used, user has to be logged in, but any user can create quiz, but only user who created it can update it  
    ``baseurl/v1/quizzes/administration/`` - List all existing quizzes (GET) and create new (POST)   
    ``baseurl/v1/quizzes/administration/{quiz_id}/`` - Get existing quiz with questions (GET) and update it (PUT/PATCH)   
    ``baseurl/v1/quizzes/administration/{quiz_id}/add_qustion/`` - Add new question with answers (POST)   
    ``baseurl/v1/quizzes/administration/{quiz_id}/remove_question/{qustion_id}`` - Delete question (DELETE)  
    ``baseurl/v1/quizzes/administration/{quiz_id}/finalize/`` - Finalize quiz creation (PUT/PATCH), can't be undone, and only after quiz is final, it can be taken   
  
  * Models and endpoints for quiz attempts, progress and history  
    ``baseurl/v1/quizzes/`` - List all existing quizzes (GET) that are final and can be taken
    ``baseurl/v1/quizzes/attempt/{quiz_id}/`` - Start or continue one quiz (GET), if there is attempt in progress returns saved answers, if not, it starts new attempt  
    ``baseurl/v1/quizzes/submit/{quiz_id}/`` - Submit and finish quiz attempt, get score (PUT/PATCH), must have attempt in progress
    ``baseurl/v1/quizzes/save-progress/{quiz_id}/`` - Submit and save current answers to be continued later (PUT/PATCH), will not be scored, must have attempt in progress   
  
  * All endpoints should be at least covered with happy path testing, preferably even error handling
  
  
# Tasks for improvement:
  
  * More in depth user and quiz administration, and updates
  * Create roles and permission system to use (who can create and administrate quizzes, questions, etc)
  * Add some kind of categories to quizzes, to allow for filtering and even maybe access control
  * Add filters and searches to all list endpoints, ordering, pagination
  * Add some randomness to answer display order
