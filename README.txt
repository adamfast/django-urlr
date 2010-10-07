This project makes it trivially easy to get/create shortened URLs via bit.ly for Django objects.

Requirements:
    bit.ly Python API http://github.com/bitly/bitly-api-python

Configuration:
    Set BITLY_API_USER and BITLY_API_KEY in settings.
    Optionally set BITLY_CUSTOM_DOMAIN if you have a custom URL through their pro service.
    Add 'urlr' to INSTALLED_APPS so the model will be created.

    Use manage.py migrate to create the necessary tables (or, if not using South a syncdb will accomplish this as well)
