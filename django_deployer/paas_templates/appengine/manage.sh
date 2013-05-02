PROJECT_NAME="{{ project_name }}"
CLOUDSQL_DATABASENAME="{{ databasename }}"
CLOUDSQL_INSTANCENAME="{{ instancename }}"
APPENGINE_SDK_LOCATION={{ sdk_location }}
MANAGE_SCRIPT_LOCATION="{{ managepy }}"
APPLICATION_ID="{{ application_id }}"
PATH="$APPENGINE_SDK_LOCATION:$PATH"

export PYTHONPATH="env/lib/python2.7:$APPENGINE_SDK_LOCATION:$APPENGINE_SDK_LOCATION/lib/django-1.4"
export DJANGO_SETTINGS_MODULE="$PROJECT_NAME.settings_appengine"
export APPLICATION_ID

args=$@

manage_script () {
    env/bin/python $MANAGE_SCRIPT_LOCATION $@ --settings=$DJANGO_SETTINGS_MODULE
}


case "$1" in
  cloudcreatedb)
    echo "create database $CLOUDSQL_DATABASENAME;" | $APPENGINE_SDK_LOCATION/google_sql.py $CLOUDSQL_INSTANCENAME 
    ;;
  cloudsyncdb)
    export SETTINGS_MODE=prod && manage_script syncdb
    ;;
  clouddbshell)
    export SETTINGS_MODE=prod && manage_script dbshell
    ;;
  deploy)
    # packaging site-packages
    cp -r env/lib/python2.7/site-packages ./
    cd site-packages 
    rm -rf *.so django PIL
    cd -
    # deploy
    appcfg.py update --oauth2 .
    rm -rf site-packages
    ;;
  *)
    manage_script $args
esac
