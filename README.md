# Redraw
COS 333 Project.  Revamped Roomdraw website.

To run Django backend, cd into "Redraw":
 1) npm start in frontend folder
 2) ./manage.py runserver

In order to run the production server,
 1) npm run build in the frontend folder
 2) ./manage.py collectstatic --settings=Redraw.production_settings
 3) ./manage.py runserver --settings=Redraw.production_settings
