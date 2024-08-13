""" Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests, json, os
from dotenv import load_dotenv
import csv

load_dotenv()
base=os.environ["base"]
requests.packages.urllib3.disable_warnings()



with open('overview.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["Tenant", "Application EPGs", "Contracts Relations"]
    writer.writerow(field)

def get_token():
    user=os.environ["user"]
    password=os.environ["password"]
    url = f"{base}/aaaLogin.json"
    payload = {
            "aaaUser": {
                "attributes": {
                    "name": user,
                    "pwd": password
                }
            }
        }
    headers = {'Content-Type': 'text/plain'}
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    
    if response.status_code == 200:
        token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
        return token


def get_tenants():
    token = get_token()
    url= f'{base}/class/fvTenant.json'
    headers = {
                "Cookie": f"APIC-Cookie={token}",
            }
    
    tanents = requests.get(url, headers=headers, verify=False).json()
    tanents_list=[]
    

    for tanent in tanents["imdata"]:
        tanents_dictionary={}
        tanents_dictionary["dn"]=tanent["fvTenant"]["attributes"]["dn"]
        tanents_dictionary["name"]=tanent["fvTenant"]["attributes"]["name"]
        tanents_list.append(tanents_dictionary)
    APs_list=[]
    for tanent in tanents_list:
        f_name=tanent["name"]+".csv"
        with open(f_name, 'w', newline='') as file:
                writer = csv.writer(file)
                
        tn=tanent["dn"]
        url= f"{base}/mo/{tn}.json?rsp-subtree=full&rsp-prop-include=config-only"
        response=requests.get(url, headers=headers, verify=False).json()
   



        for r in response["imdata"]:
            epg_count=0
            for rr in r["fvTenant"]["children"]:
                contrct_count=0
                if "fvAp" in rr:
                    
                    ap=rr["fvAp"]["attributes"]["name"]
                    # print(ap)
                    url=f"{base}/node/mo/{tn}/ap-{ap}.json?query-target=subtree&target-subtree-class=fvAEPg"
                    # print(url)
                    EPGs=requests.get(url, headers=headers, verify=False).json()
                   
                    with open(f_name, 'a', newline='') as file:
                        writer = csv.writer(file)
                        
                        ap_name=ap
                       
                        field1 = ["EPG Name","Contract Name", "Provided/Consumed","State"]
                        writer.writerow(field1)
                       
            
                    for epg in EPGs["imdata"]:
                        ep=epg["fvAEPg"]["attributes"]["dn"]
                        
                        epg_count+=1

                        with open(f_name, 'a', newline='') as file:
                            writer = csv.writer(file)
                            
                            epg_name=epg["fvAEPg"]["attributes"]["name"]
                            


                        
                        url=f"{base}/node/mo/{ep}.json?query-target=subtree&target-subtree-class=fvRsProv"
                        contratcs_provided=requests.get(url, headers=headers, verify=False).json()

                        
                        for contract in contratcs_provided["imdata"]:
                            if len(contract) != 0:
                                cont=contract["fvRsProv"]["attributes"]["dn"]
                                contrct_count+=1
                                with open(f_name, 'a', newline='') as file:
                                    writer = csv.writer(file)
                                    field=[epg_name,str(cont.split("rsprov-",1)[1]),"Provided" ,contract["fvRsProv"]["attributes"]["state"]]
                                    writer.writerow(field)

                    
                        url=f"{base}/node/mo/{ep}.json?query-target=subtree&target-subtree-class=fvRsCons"
                        contratcs_consumed=requests.get(url, headers=headers, verify=False).json()

                        if contratcs_consumed["totalCount"] =="0":
                            with open(f_name, 'a', newline='') as file:
                                        writer = csv.writer(file)
                                        field=[epg_name]
                                        writer.writerow(field)
                                        
                        else:
                        
                            for contract in contratcs_consumed["imdata"]:
                                        cont=contract["fvRsCons"]["attributes"]["dn"]
                                        contrct_count+=1

                                        with open(f_name, 'a', newline='') as file:
                                            writer = csv.writer(file)
                                            field1=[epg_name,str(cont.split("rscons-",1)[1]),"Consumed" ,contract["fvRsCons"]["attributes"]["state"]]
                                            writer.writerow(field1)
                                                     
            file_row=[]
            with open('overview.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                file_row.append(tanent["name"])
                file_row.append(str(epg_count))
                file_row.append(str(contrct_count))
                writer.writerow(file_row)

            

if __name__ == "__main__":
    get_tenants()