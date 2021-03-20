import os
import yaml
import datetime
import smtplib, ssl
import subprocess
from influxdb import InfluxDBClient

def check_services():
    with open("config.yaml", "r") as f:
        config = yaml.load(f)

    services = config['services']

    for service in services:
        service_name = service['name']
        service_logs_file = service['log_file']
        stat = os.system('systemctl is-active --quiet %s' % service_name)

        if stat != 0:
            print('Discovered service %s is stopped' % (service_name))
            write_on_influx(config, service_name)
            
            if service['criticality'] == 1:
                service_logs = get_logs(service_logs_file)
                send_email(config, service_name, service_logs)
        
            try_start_service(service_name)

def write_on_influx(config, service_name):
    influx_data = config['influxdb']
    instance_data = config['instance']

    host = influx_data['host']
    port = influx_data['port']
    user = influx_data['user']
    password = influx_data['password']
    database = influx_data['database']

    host_sending = instance_data['hostname']

    client = InfluxDBClient(host, port, user, password, database)

    json_body = [
            {
                "measurement": "services_alerter",
                "tags": {
                    "host": host_sending
                },
                "fields": {
                    "value": "Service %s is down." % service_name
                }
            }
        ]

    client.write_points(json_body)

def send_email(config, service_name, service_logs):
    email_params = config['email']
    instance_params = config['instance']

    company_name = instance_params['company_name']
    hostname = instance_params['hostname']

    port = email_params['smtp_port']
    smtp_server = email_params['smtp_server']
    sender_email = email_params['sender']
    receiver_email = email_params['receiver']
    password = email_params['password']

    print('sending email...')
    
    text = '''\
        The server %s in %s has the service %s down.
        
        %s''' % (hostname, company_name, service_name, service_logs)
    
    subject = "Problems on %s" % (company_name) 

    message = 'Subject: {}\n\n{}'.format(subject, text)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def get_logs(service_logs_file):
    try:
        logs = subprocess.check_output(['tail', '-n 50', service_logs_file])
    except:
        logs = "Log file wasn't found."
    
    return logs

def try_start_service(service_name):
    os.system('systemctl start %s' % service_name)


if __name__ == '__main__':
    check_services()