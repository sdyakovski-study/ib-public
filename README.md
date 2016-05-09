Implementation of the IB Online Rater in Django with possibly AngularJS.
requirements.txt lists the external libraries installed with pip in this virtualenv.

Added to settings the BASE_DIR, BASE_PATH, PROJECT_DIR values settings using advises from the cookbook.
Copied all from rater from python-projects/limits/project/rater
Copied the models.py from rater. run makemigrations in ib-public/project over its rater app
It created 001_initial.py migration with all tables.
SInce there were 3 migrations on rater at limits/project/rater, and both projects pointed to the same db and tables.
I copied the 001_initial from ib-public into limits/rater removing the 002 and 003. Deleted them from db from table django_migrations.


 
