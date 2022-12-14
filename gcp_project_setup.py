#!/usr/bin/python
import sys, optparse, subprocess, configparser
def exit_clean():
  print "\nCaptured ctrl+c"
  sys.exit(0)

def parse_input():
  usage = "usage: %prog --config <config file>"
  parser = optparse.OptionParser(usage)
  parser.add_option("--config", dest="config_file", type="string", help="Input file: --config")
  options, arguments = parser.parse_args()

  if not options.config_file:
    parser.error('Error: --config option is require')
  return options

def parse_config(config_file):
  #Setup the config parser
  config = configparser.ConfigParser(allow_no_value=True)
  config._interpolation = configparser.ExtendedInterpolation()
  config.sections()
  #Open and read config file
  try:
    f = open(config_file)
    f.close()
  except IOError as e:
    print "There was an error loading the configuration file."
    print e[1]
    sys.exit(1)
  try:
    config.read(config_file)
  except Exception as e:
    print "There was an error reading the config file."
    print e[1]
    sys.exit(1)
  return config

def run_subcommand(cmd):
  proc = subprocess.Popen( cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  proc.wait()
  (stdout, stderr) = proc.communicate()  
  return stdout, stderr, proc.returncode

def create_project(config):
  project_id = config["project"]["project_id"]  
  project_folder = config["project"]["project_folder"]
  billing_account = config["project"]["billing_account"]

  #Convert dictionary to list of key value pairs as tuples
  label_list = config["project_labels"].items()
  #Create a new list where the tuples are coverted to string seperated by = 
  new_list = ['='.join(tups) for tups in label_list] 
  #Create a new where each label is separated by a comma
  labels = ','.join(new_list)

  print "Creating Project: "
  cmd = ['gcloud', 'projects', 'create', project_id , '--folder', project_folder, '--labels', labels  ]
  stdout, stderr, returncode = run_subcommand(cmd)
  if returncode:
    if "already in use by another project" not in stderr:
      print stderr.splitlines()[0]
      sys.exit(returncode)
    else:
      print "Project already exists with ID: " + project_id
      print "Continuing to configuration using existing project with ID: " + project_id
  else:
    print stdout
    print stderr 

  print "Linking Project to billing account: "
  cmd = ['gcloud', 'beta', 'billing','projects', 'link' , project_id , '--billing-account', billing_account ]
  stdout, stderr, returncode = run_subcommand(cmd) 
  print stdout
  print stderr     

def enable_api(config):
  project_id = config["project"]["project_id"]  
  print "Enabling APIs: "
  for api in config["apis"]:
    print "  Enabling API: " + api
    cmd = ['gcloud', 'services', 'enable', api , '--project', project_id ]
    stdout, stderr, returncode = run_subcommand(cmd)  
    if returncode:
      print stderr.splitlines()[0]
      sys.exit(returncode)
    else:
      print stdout
      print stderr 


def enable_app_engine(config):
  project_id = config["project"]["project_id"]
  enable = config["project"]["enable_app_engine"]
  region = config["project"]["region"]
  #If we are enabling app engine run the gcloud command to do just that
  if enable:
    print "Enabling App Engine"
    cmd = ['gcloud', 'app', 'create', '--region', region , '--project', project_id ]
    stdout, stderr, returncode = run_subcommand(cmd)   
    if returncode:
        if 'already contains an App Engine application' not in stderr:
          print stderr.splitlines()
          sys.exit(returncode)
        else:
          print "  App Engine already enabled for project: " + project_id
    else:
      print stderr.splitlines()[0]  



def create_service_account( account, roles, project_id ):
  result = ''
  #Split the account into 2 "names" [0] = account and [2] = fqdn
  names = account.split('@')
  service_fqdn = project_id + ".iam.gserviceaccount.com"
  #If the fqdn portion of the account name is a standard service account then try to create it.
  if names[1] == service_fqdn:
    display_name = account + " service account"
    cmd = ['gcloud', 'iam', 'service-accounts', 'create', names[0], '--display-name', display_name, '--project', project_id]
    stdout, stderr, returncode = run_subcommand(cmd) 
    if returncode:
      if "already exists within project" not in stderr:
        print stderr.splitlines()[0]
        sys.exit(returncode)
      else:
        print "  User already exists.  Continuing to assign roles..."
    else:
        print stderr.splitlines()[0]
  else:
    print "  " + account + " is not a standard service account ending in @" + project_id + ".iam.gserviceaccount.com. " +  "We will not attempt to create it."

def add_roles(account,roles,project_id,account_type):
  member = account_type + ":" + account
  for role in roles:
    cmd = [ 'gcloud', 'projects', 'add-iam-policy-binding', project_id, '--member', member, '--role', role ]
    stdout, stderr, returncode = run_subcommand(cmd) 
    if returncode:
      print stderr
    else:
      print "    Role: " + role + " applied to: " + account

def setup_service_accounts(config):
  #Configure the option key "type" value to search for. 
  option_type = "service_account"
  #Loop through all sections of the config...
  for section in config:
    #If the section has an option named "type" then continue to perform tasks based on type
    if config.has_option(section, "type"):
      if config[section]["type"] == option_type:
        roles = config[section]["roles"].split()
        account = config[section]["account"]
        project_id = config["project"]["project_id"]
        print "Adding Service Account: " + account
        create_service_account( account, roles, project_id )
        add_roles(account,roles,project_id,"serviceAccount")

def setup_users(config):
  #Configure the option key "type" value to search for. 
  option_type = "user"
  #Loop through all sections of the config...
  for section in config:
    #If the section has an option named "type" then continue to perform tasks based on type
    if config.has_option(section, "type"):
      if config[section]["type"] == option_type:
        roles = config[section]["roles"].split()
        account = config[section]["account"]
        project_id = config["project"]["project_id"]        
        print "Configuring user: " + account
        add_roles(account,roles,project_id,"user")

def setup_groups(config):
  #Configure the option key "type" value to search for. 
  option_type = "group"
  #Loop through all sections of the config...
  for section in config:
    #If the section has an option named "type" then continue to perform tasks based on type
    if config.has_option(section, "type"):
      if config[section]["type"] == option_type:
        roles = config[section]["roles"].split()
        account = config[section]["account"]
        project_id = config["project"]["project_id"]        
        print "Configuring group: " + account
        add_roles(account,roles,project_id,"group")

def main():
  options = parse_input()

  #Parse and store the configuration
  config = parse_config(options.config_file)
  #Create project
  create_project(config)  
  #Enable the APIs
  enable_api(config)
  #Enable App Engine
  enable_app_engine(config)
  #Create and assign roles to the service accounts
  setup_service_accounts(config)
  #Assign roles to the user accounts
  setup_users(config)  
  #Assign roles to the group accounts
  setup_groups(config)    

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
    my_parser = exit_clean()