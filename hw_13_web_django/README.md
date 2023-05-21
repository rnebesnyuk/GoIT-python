The Quotes website is a simple django project website.

You need the /quotes_app/.env file with environment variables to work with the app. Please create the file with the following variables and insert your values:

SECRET_KEY=

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=


To start the app:

cd quotes_app
py manage.py runserver


The app will allow you to:

* register, login and logout the certain username
* add new Tag (only for logged in User)
* add new Author (only for logged in User)
* add new Quote with an author and multi tag selection possibility (only for logged in User)
* browse all quotes added to the website
* check the author details
* search all quotes by certain Tag by clicking on the Tag name
* see the top 10 Tags cloud on the home and quotes_by_tag pages; the feature is refreshed each time when you refresh those pages
* navigate through the pages (next, previous, first, last, +/- 2 pages from the current one) on the home and quotes_by_tag pages
* according to the homework requirements, the initial json files with authors and quotes can be migrated to MongoDB; from MongoDB to Postgres database (scripts in the utils folder). Working database for the project is Postgres DB.


Notes:
- list of authors ordered by fullname
- slug for the author created automatically upon author creation
- list of tags ordered by name
- list of quotes is sorted by date created desc
- you need to be logged in to see the Add Tag/Add Author/Add Quote links; for logged out user visible only Home link
- upon successful author adding - user is redirected to the author description page
- upon successful quote adding - user is redirected to the home page where the new quote added should be on top
- upon successful user creating - user is redirected to the home page