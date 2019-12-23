# Nexinvent

* We are using a settings folder to seperate environments, therefore to run this in development mode, use:
  - ```python manage.py runserver --settings=nexinvent.settings.development```.
  - It is however reccommended to set the ```DJANGO_SETTINGS_MODULE``` envirnoment variable other you need to pass settings to every other command (like migrate)
  - You may need access keys for third party services like Amazon S3, Twilio etc. extend the development.py settings with an untracked file and put the keys there.
* This project has been configured to be deployed in ElasticBeanStalk, so the production settings should be riddled with EBS environment variable references.
  - Beanstalk container commands set up to collectstatic and migrate with --noinput
  - on the first run, a super user needs to be created manually for the django admin 
  - when you ssh into the instance using ```eb ssh```, the environment variables configured in EBS dashboard will not
   be available. use ```. /opt/python/current/env``` to load them [source: https://stackoverflow.com/questions/24562714/elastic-beanstalk-custom-ami-cant-see-environment-variables]
* additional notes for lazy googlers/ready reference:
  - ```export DJANGO_SETTINGS_MODULE=nexinvent.settings.development``` in your terminal
  - To permanently set the env variable - ```nano ~/.bash_profile``` and add the above line
  - celery worker can be started by ```celery -A tasks worker --loglevel=info```, but make sure rabbitmq has been started
  - In development : ```sudo rabbitmq-server```
  
## Doing a clean deploy

  - Set up a configured python environment in Elastic beanstalk (not docker)
  - Get a preconfigured public SSH certificate. this can be accessible from any amazon account now. Preferabbly add an entry for *.<domain>.com
  - Configure a sweet RDS instance so its environment variables are exposed
  - Add a load balancer. use a HTTPS from 443 listener configured to internal instance 80 HTTP.
  - Add Environment variables in software configuration
  - Create a new Code Pipeline from the repository, no build stage required. select the same ELB Application
  - Voila, fresh deployment should be ready