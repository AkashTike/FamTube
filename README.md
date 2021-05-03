# FamTube
## _Hiring Challenge By FamPay_

Famtube internally uses YouTube API's and provides a platform to view the stored information of YouTube videos.

## Features & Functionalities

- Server Calls the YouTube API's continuously in the background
  - A cronjob is setup every 15 minutes
  - Multiple Google API KEYs has been setup so if one is exhausted, the other could be used 
- GET API to fetch all the videos
  - Paginated Response 
  - [View/Call](http://127.0.0.1:8000/api/videos) API [Documentation Included]
- POST API to search videos by title or description
  - For the search,
     - Order of words does not matter
     - Special Characters and Cases won't affect the result
     - Partial word matching is allowed. For example, "Election" could be miswritten as "ection"
  - [View/Call](http://127.0.0.1:8000/api/search) API [Documentation Included] 
- Dashboard to view the stored videos and search them
  - [View dashboard](http://127.0.0.1:8000/dashboard) API [Documentation Included] 
  - Frontend Pagination Included
  - All the stored videos would be visible initially, until a search query is executed

## Tech

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Materialize CSS](https://materializecss.com/)
- [JavaScript](https://www.javascript.com/)

## Installation

Install the dependencies

```sh
pip install -r requirements.txt
```

Make Migrations & Migrate

```sh
python manage.py makemigrations
python manage.py migrate
```

Add Cronjob to store video information

```sh
python manage.py crontab add
```

## Run

Start the server

```sh
python manage.py runserver
```

Check by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```

## Improvements

- Adding more number of Google API Keys and reducing the interval of cronjob
- Search could be improved by implementing Stemming, Lemmatization, Stop word removal, LCS match etc.
