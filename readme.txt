PROJECT SETUP:
--------------

1) create a .env file and env_variables.yaml in the project folder.
2) use os.urandom(12).hex() on the python console to generate secret keys
3) save keys in the files in the following formats:

.env
FLASK_KEY=XXXX

env_variables.yaml
env_variables:
  FLASK_KEY: "XXXX"


GOOGLE APP ENGINE:
------------------
1) Create a new project and create an app inside it (optional - can do this below)
2) In pycharm terminal 'gcloud init' then create a new configuration
3) 'gcloud app deploy'