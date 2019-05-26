# Nexinvent

* We are using a settings folder to seperate environments, therefore to run this in development mode, use:
  - ```python manage.py runserver --settings=nexinvent.settings.development```.
  - It is however reccomended to set the ```DJANGO_SETTINGS_MODULE``` envirnoment variable other you need to pass settings to every other command (like migrate)
  - You may need access keys for third party services like Amazon S3, Twilio etc. extend the development.py settings with an untracked file and put the keys there.
* This project has been configured to be deployed in ElasticBeanStalk, so the production settings should be riddled with EBS environment variable references.
  - Beanstalk container commands set up to collectstatic and migrate with --noinput
  - on the first run, a super user needs to be created manually for the django admin 
  - when you ssh into the instance using ```eb ssh```, the environment variables configured in EBS dashboard will not
   be available. use ```. /opt/python/current/env``` to load them [source: https://stackoverflow.com/questions/24562714/elastic-beanstalk-custom-ami-cant-see-environment-variables]