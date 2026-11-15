coverage erase

coverage run manage.py test \
    --settings=bracketmaster.settings_test \
    --verbosity=2

coverage report -m

coverage html