# ODP GCP Project Setup


## Overview <a name="s1"></a>

This script is used to setup a GCP project, user permissions, group permissions, service accounts, and apis required to successfully and securely deploy your project.

NOTE: This script is does not deploy any GCP services.

## Tables of Contents 

* [Overview](#s1)
* [Project Contents ](#s2)
* [Prerequisites ](#s2.1)
* [Project Setup](#s3)
* [Examples](#s4)
* [Technologies used](#s5)
* [Status and todo](#s6) 


## Project Contents <a name="s2"></a>

| Folder    |  Description    |
|---        |---              |
| gcp_project_setup.py  |   Script used to provision the GCP project, user permissions, group permissions, service accounts, and apis.   |
| project_config.ini  |  Example configuration file


## Prerequisites <a name="s2.1"></a>

* You need to have high enough privileges within the GCP organization to provision new projects.

## Project Setup  <a name="s3"></a>

### GCP Console

The easiest way to get started is to activate a cloud console by logging into GCP and clicking the `Activate Cloud Console` button.

<img src="console.PNG" width="10%">


### Clone the project

You will want to clone the project.

`git clone https://github.com/GSA/odp-gcp-project-setup.git`


### Edit the project_config.ini

You will want to customize the `project_config.ini` to meet your desired configuration.
For a complete example see the [example project_config.ini.](./project_config.ini)

Below is a list of configuration sections and the options you can set:

<strong>Note:</strong> Sections marked optional can be deleted from the `project_config.ini`

* <strong>[project]</strong>
  * `project_id`
    * Replace `<YOUR_PROJECT_ID>` with a new or existing Project ID.
  * `project_folder`
    * Replace `<YOUR_PROJECT_FOLDER>` with the existing Folder ID the project should go into
  * `billing_account`
    * Replace `<YOUR_BILL_ACCOUNT_ID>` with the Billing Account ID you wish to be associated with this project.
  * `enable_app_engine` 
    * Set to `True` or `False` to enable or disable App Engine for the Project.
  * `region`
    * Set `<YOUR_PROJECTS_REGION>` to the desired region.
* <strong>[project_labels] * Optional</strong> 
  * Any key value pairs that you add as an option under this section will generate a new label for your project.
    * `test-label = test-value` will generate a label of `test-label` with a value of `test-label`.
  * Please keep in mind the following GCP restrictions on labels and values:
    * "Only hyphens (-), underscores (_), lowercase characters, and numbers are allowed. International characters are allowed"
* <strong>[terraform_service_account]  * Optional</strong>
  * This section provides and example of creating a new or configuring an existing service account and assigning roles.  
  * `type` 
    * Set type to `service_account` to create or configure an existing service account
  * `account`
    * Replace `terraform` with the desired service account name.
  * `roles`
    * You can add or delete any roles you would like applied in this section.  Be sure to indent 2 spaces when adding new fields as white space matters.  
    * Understand roles added here will be appeneded.  Removing already applied roles is from the list will not remove them from the actual configuration.
* <strong>[project_owner_user] * Optional</strong>
  * This section provides and example of configuring an existing user account and assigning roles.
  * `type` 
    * Set type to `user` to configure an existing user account
  * `account`
    * Set the <USER@domain.com> to your desired user account.
  * `roles`
    * You can add or delete any roles you would like applied in this section.  Be sure to indent 2 spaces when adding new fields as white space matters.  
    * Understand roles added here will be appeneded.  Removing already applied roles is from the list will not remove them from the actual configuration.
* <strong>[project_owner_group] * Optional</strong>
  * This section provides and example of creating a new or configuring an existing group and assigning roles.
  * Section can be named anything you would like, and you can create as many group sections as you require. 
  * `type` 
    * Set type to `group` to configure an existing group account
  * `account`
    * Set the <group@domain.com> to your desired group account.
  * `roles`
    * You can add or delete any roles you would like applied in this section.  Be sure to indent 2 spaces when adding new fields as white space matters.  
    * Understand roles added here will be appeneded.  Removing already applied roles is from the list will not remove them from the actual configuration.


### Run the script

* Run the script with the `--config` parameter pointing to where you saved the `project_config.ini` file.
  
#### Example:

```
python gcp_project_setup.py --config project_config.ini
```

