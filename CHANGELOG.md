# 0.3.2
* Fix - Added subject when sending email.
* Add - README.md with instructions.

# 0.3.1
* Fix - Take host name to write in Influx from config file, before it was hardcoded by error.

# 0.3.0
* Add - Compatibility to send the log to a given InfluxDB.
* Add - Support to add InfluxDB data.
* Fix - It only tries to start down services; before it tried everyone.

# 0.2.1
* Fix restarting service. In some systems "service" didn't work properly, so it was changed for "systemctl".
* Trying to start the service after collecting the logs to not send anything else in the email.

# 0.2.0
* Try to start a service when it's down.

# 0.1.0
* Send email when service from list is down with its logs if criticality is 1.