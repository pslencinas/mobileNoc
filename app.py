from os import path
from glob import glob
import sys
import yaml
from ciscoconfparse import CiscoConfParse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Vlan
import logging
from netmiko import ConnectHandler
from device import Device
from menu import menu


logger = logging.getLogger(__name__)
           

def run():
    
    dev = Device('10.20.255.250', 'MY_USER', 'MY_PASSWORD')
    dev.backup()

    while True:
        option = menu()

        if option == 1:
            vlan_id = input('vlan ID: ')
            while not vlan_id.isnumeric() and (int(vlan_id) > 1 and int(vlan_id) < 4094):
                print('Please, enter a right vlan id!')
                vlan_id = input('vlan ID: ')
                
            vlan_name = input('Name: ')
            vlan_description = input('Description: ')

            data = {
                'vlan_id': vlan_id,
                'vlan_name': vlan_name,
                'vlan_description': vlan_description
            }
            dev.create_vlan_db(data)
            dev.create_vlan_device(data)
            dev.backup()

        if option == 2:
            vlan_id = input('vlan ID: ')
            while not vlan_id.isnumeric() and (int(vlan_id) > 1 and int(vlan_id) < 4094):
                print('Please, enter a right vlan id!')
                vlan_id = input('vlan ID: ')
                
            vlan_name = input('Name: ')
            vlan_description = input('Description: ')

            data = {
                'vlan_id': vlan_id,
                'vlan_name': vlan_name,
                'vlan_description': vlan_description
            }
            dev.update_vlan_db(data)
            dev.create_vlan_device(data)
            dev.backup()
            
        if option == 3:
            vlan_id = input('vlan ID: ')
            while not vlan_id.isnumeric() and (int(vlan_id) > 1 and int(vlan_id) < 4094):
                print('Please, enter a right vlan id!')
                vlan_id = input('vlan ID: ')
                
            data = {
                'vlan_id': vlan_id
            }
            
            dev.delete_vlan_db(data)
            dev.delete_vlan_device(data)
            dev.backup()

        if option == 4:
          
            dev.backup()
            dev.find_vlans_device()
            print(dev.vlans_device)

        if option == 5:

            dev.backup()
            # sync between device and DB
            dev.find_vlans_device()
            for item in dev.vlans_device:
                vlan = dev.find_vlan_db(item.get('id'))
                if vlan:
                    # have vlan, check same name
                    if vlan.name != item.get('name'):
                        data = {
                            'vlan_id': item.get('id'),
                            'vlan_name': item.get('name')
                        }
                        dev.update_vlan_db(data)

                else:
                    # vlan not found in db, updating
                    data = {
                        'vlan_id': item.get('id'),
                        'vlan_name': item.get('name'),
                        'vlan_description': item.get('name')
                    }
                    dev.create_vlan_db(data)


            # sync between db and device
            vlans = dev.find_vlans_db()
            if vlans:
                for item in vlans:
                    found = False
                    for vlan_device in dev.vlans_device:
                        if item.id == vlan_device.get('id'):
                            found = True
                            break
                    
                    if not found:
                        #create vlan in device
                        data = {
                            'vlan_id': item.id,
                            'vlan_name': item.name,
                            'vlan_description': item.description
                        }
                        dev.create_vlan_device(data)



        
        if option == 9:
          
            break
                    



run()
