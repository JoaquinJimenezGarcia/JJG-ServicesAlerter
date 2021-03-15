import os
import yaml
import datetime
import smtplib, ssl
import subprocess

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
            # TODO: Include method to write log on InfluxDB
            
            if service['criticality'] == 1:
                service_logs = get_logs(service_logs_file)
                send_email(config, service_name, service_logs)
        
        try_start_service(service_name)

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
    
    message = """\
        JJG-ServicesAlerter

        The server %s in %s has the service %s down.
        
        %s
        """ % (hostname, company_name, service_name, service_logs)
    
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