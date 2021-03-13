import os
import yaml
import datetime
import smtplib, ssl

def check_services():
    with open("config.yaml", "r") as f:
        config = yaml.load(f)

    services = config['services']

    for service in services:
        service_name = service['name']
        stat = os.system('systemctl is-active --quiet %s' % service_name)

        if stat != 0:
            print('Discovered service %s is stopped' % (service_name))
            # TODO: Include method to write log on InfluxDB
            
            if service['criticality'] == 1:
                send_email(config, service_name)

def send_email(config, service_name):
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

        The server %s in %s has the service %s down.""" % (hostname, company_name, service_name)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
    check_services()