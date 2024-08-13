# GVE DevNet ACI EPGs Contracts Export
This prototype utilizes the ACI REST API to get all EPGs and contract relations configured in APIC. The Python script generates the following:

An overview csv file which provides a summary of how many application EPGs and contracts relations are there in each tenant. Then there’s a csv file for each tenant that shows the application profiles, EPGs and contracts(type and state). An empty tenant file indicates a tenant with no application profiles and EPGs. 
 
## Contacts
* Roaa Alkhalaf

## Solution Components
* APIC
* ACI
* ACI REST APIs
* Python

## Installation/Configuration
The following commands are executed in the terminal.

1. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 
Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html). 

2. Access the created virtual environment folder

        $ cd your_venv

3. Clone this repository

        $ git clone https://wwwin-github.cisco.com/gve/gve_devnet_aci_epgs_contracts_export.git


4. Access the folder `gve_devnet_aci_epgs_contracts_export`

        $ cd gve_devnet_aci_epgs_contracts_export

5. Install the dependencies:

        $ pip3 install -r requirements.txt

6. In `.env`, fill out the ACI credentials:

```
base=<https://IP-address/api>
user=<Username>
password=<Password>

```
## Usage
1. To generate the CSV files, type the following command in your terminal:

        $ python3 main.py



#



# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.