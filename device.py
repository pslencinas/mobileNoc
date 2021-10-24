from os import path
from glob import glob
import os
from ciscoconfparse import CiscoConfParse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Vlan
import logging
from netmiko import ConnectHandler

logger = logging.getLogger(__name__)

filepath = os.path.dirname(__file__)
targetdir_backup = './backup/'
if not os.path.exists(targetdir_backup):
    os.makedirs(targetdir_backup)

class Device(object):

    vlans_device = []


    def __init__(self, ip, username, password):
        engine = create_engine('sqlite:///my_db.db?check_same_thread=False')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.db_session = DBSession()

        
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password
        }

        self.device_session = ConnectHandler(**device)
        logger.debug(" Connected ")
        

    def backup(self):
        fullPath = targetdir_backup+ '/config.txt'

        config_data = ''
        config_data += self.device_session.send_command('show runn')
        with open( fullPath, 'w' ) as config_out:  
            config_out.write( config_data )

    
    def create_vlan_db(self, data):

        new_vlan = Vlan(
                    vlan_id = data.get('vlan_id'),
                    name=data.get('vlan_name'),
                    description = data.get('vlan_description')
                ) 

        self.db_session.add(new_vlan)
        self.db_session.commit()

        logger.debug(" Vlan created on DB: {}".format(data))


    def update_vlan_db(self, data):

        vlan = self.db_session.query(Vlan).filter_by(vlan_id = data.get('vlan_id')).first()
        vlan.name = data.get('vlan_name')
        vlan.description = data.get('vlan_description')
        self.db_session.commit()
        
        logger.debug(" Vlan updated on DB: {}".format(data))

    def delete_vlan_db(self, data):

        vlan = self.db_session.query(Vlan).filter_by(vlan_id = data.get('vlan_id')).first()
        self.db_session.delete(vlan)
        self.db_session.commit()

        logger.debug(" Vlan removed on DB: {}".format(data))

    def find_vlan_db(self, vlan_id):

        vlan = self.db_session.query(Vlan).filter_by(vlan_id = vlan_id).first()
        return vlan

    def find_vlans_db(self):

        vlans = self.db_session.query(Vlan).all()
        return vlans


    def create_vlan_device(self, data):

        config_commands = ['vlan ' + data.get('vlan_id'), 'name ' + data.get('vlan_name')]
        output = self.device_session.send_config_set(config_commands)
        
        logger.debug(" Vlan created on device: {}".format(data))       


    def delete_vlan_device(self, data):

        config_commands = ['no vlan ' + data.get('vlan_id')]
        output = self.device_session.send_config_set(config_commands)

        logger.debug(" Vlan deleted on device: {}".format(data))       


 

    def find_vlan_device(sef, vlan_id):
        fullPath = targetdir_backup+ '/config.txt'
        parse = CiscoConfParse(fullPath)
        vlan = parse.find_objects(r'^vlan\s+'+str(vlan_id))
        if vlan:
            return True
        else:
            return False

 

    def find_vlans_device(self):
        
        self.vlans_device = []
        fullPath = targetdir_backup+ '/config.txt'
        parse = CiscoConfParse(fullPath)
        users = parse.find_objects(r'^vlan\s+')
        for user in users:
            #print(user.text)
            for child in user.children:
                #print(child.text)
                self.vlans_device.append({
                        'id': (user.text).split()[1],
                        'name': (child.text).split()[1]
                })

        logger.debug(" Find Vlans : {}".format(self.vlans_device))       
        
           