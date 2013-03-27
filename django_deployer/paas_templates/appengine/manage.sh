PROJECT_NAME="{{ project_name }}"
CLOUDSQL_DATABASENAME="{{ databasename }}"
CLOUDSQL_INSTANCENAME="{{ instancename }}"
APPENGINE_SDK_LOCATION="{{ sdk_location }}"
APPLICATION_ID="{{ application_id }}"

args=$@

manage_script () {
    env/bin/python $PROJECT_NAME/manage.py $@ --settings=$PROJECT_NAME.settings_appengine
}

export PYTHONPATH="env/lib/python2.7:$APPENGINE_SDK_LOCATION:$APPENGINE_SDK_LOCATION/lib/django-1.4"
export DJANGO_SETTINGS_MODULE="$PROJECT_NAME.settings_appengine"
export APPLICATION_ID

if [ $1 == "cloudcreatedb" ] ; then
    echo "create database $CLOUDSQL_DATABASENAME;" | $APPENGINE_SDK_LOCATION/google_sql.py $CLOUDSQL_INSTANCENAME 
elif [ $1 == "cloudsyncdb" ] ; then
    export SETTINGS_MODE=prod && manage_script syncdb
else
    manage_script $args
fi

