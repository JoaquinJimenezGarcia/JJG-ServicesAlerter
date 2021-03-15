# 0.2.1
* Fix restarting service. In some systems "service" didn't work properly, so it was changed for "systemctl".
* Trying to start the service after collecting the logs to not send anything else in the email.

# 0.2.0
* Try to start a service when it's down.

# 0.1.0
* Send email when service from list is down with its logs if criticality is 1.