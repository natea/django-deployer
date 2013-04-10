Changelog
---------

0.1.6 (2013-04-10)
++++++++++++++++++

- Use a createdb.py that handles timeouts better
- Remove dj-database-url since it doesn't work with Dotcloud
- Prompt for location of manage.py (for discrepancy in project layouts in Django 1.3 vs 1.4)
- dotcloud.yml file needs DJANGO_SETTINGS_MODULE or else manage.py won't work
- dotcloud.yml file needs UTF-8 or else browsing Mezzanine gallery won't work
- Let user choose their admin password instead of hardcoding it
- Make sure STATIC_ROOT and MEDIA_ROOT are defined in settings_dotcloud.py
- If project already has a top level requirements.txt, don't do anything
- Add validators for ensuring that requirements file exists, 
- Validate the admin password and that the user chose a valid provider
- Ensure that the user doesn't leave fields blank

0.1.5 (2013-04-08)
++++++++++++++++++
 
- Need a MANIFEST.in in order to find the .txt and .rst files (@natea)
- Fixed bug with misnamed CHANGES.txt -> CHANGES.rst (@natea)
- Fixed bug with missing README.rst (@natea)

0.1.1 (2013-03-26)
++++++++++++++++++

- Added support for Google App Engine (@natea, @littleq0903)

0.1.0 (2012-09-07)
++++++++++++++++++

- Initial version for Stackato and Dotcloud (@natea, @johnthedebs)