# Nexinvent

* We are using a settings folder to seperate environments, therefore to run this in development mode, use:
  - ```python manage.py runserver --settings=nexinvent.settings.development```
  - Note that other commands need to be issued the same way ```python manage.py migrate --settings=mysite.settings.production```
  - You may need access keys for third party services like Amazon S3, Twilio etc. extend the development.py settings with an untracked file and put the keys there.
  - This project has been configured to be deployed in ElasticBeanStalk, so the production settings should be riddled with EBS environment variable references
  