#! /usr/bin/python
import sys
import thread
from bluetooth import *
import binascii
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.action_dict = {'horn' : 0, 'lights' : 0, 'fault' : 0,}
        self.acceleration = 0
        self.steering = 0
        # List of available commands
        self.dict = {}
        self.dict['HORN_OFF'] = '8600'
        self.dict['HORN_ON'] = '8601'
        self.dict['LIGHTS_OFF'] = '8500'
        self.dict['LIGHTS_SOFT'] = '8501'
        self.dict['LIGHTS'] = '8502'
        self.dict['FAULT'] = ['8304',' 8404',' 8301',' 8401']
        self.dict['FAULT_OFF'] = ['8300',' 8400']
        self.dict['STEER_LEFT']=['817F','817E','817D','817C','817B','817A','8179','8178','8177','8176','8175','8174','8173','8172','8171','8170','816F','816E','816D','816C','816B','816A','8169','8168','8167','8166','8165','8164','8163','8162','8161','8160','815F','815E','815D','815C','815B','815A','8159','8158','8157','8156','8155','8154','8153','8152','8151','8150','814F','814E','814D','814C','814B','814A','8149','8148','8147','8146','8145','8144','8143','8142','8141']
        self.dict['STEER_RIGHT']=['8100','8101','8102','8103','8104','8105','8106','8107','8108','8109','810A','810B','810C','810D','810E','810F','8110','8111','8112','8113','8114','8115','8116','8117','8118','8119','811A','811B','811C','811D','811E','811F','8120','8121','8122','8123','8124','8125','8126','8127','8128','8129','812A','812B','812C','812D','812E','812F','8130','8131','8132','8133','8134','8135','8136','8137','8138','8139','813A','813B','813C','813D','813E','813F']
        self.dict['SPEED_BACK']=['827F','827E','827D','827C','827B','827A','8279','8278','8277','8276','8275','8274','8273','8272','8271','8270','826F','826E','826D','826C','826B','826A','8269','8268','8267','8266','8265','8264','8263','8262','8261','8260','825F','825E','825D','825C','825B','825A','8259','8258','8257','8256','8255','8254','8253','8252','8251','8250','824F','824E','824D','824C','824B','824A','8249','8248','8247','8246','8245','8244','8243','8242','8241']
        self.dict['SPEED_FRONT']=['8200','8201','8202','8203','8204','8205','8206','8207','8208','8209','820A','820B','820C','820D','820E','820F','8210','8211','8212','8213','8214','8215','8216','8217','8218','8219','821A','821B','821C','821D','821E','821F','8220','8221','8222','8223','8224','8225','8226','8227','8228','8229','822A','822B','822C','822D','822E','822F','8230','8231','8232','8233','8234','8235','8236','8237','8238','8239','823A','823B','823C','823D','823E','823F']
        self.dict['NO_SPEED']='8200'
        self.dict['NO_STEER'] = '8100'

        self.keycodes = {'SPACE':32, 'UP':38, 'DOWN':40, 'LEFT':37, 'RIGHT':39,
                         'W':87, 'A':65, 'S':83, 'D':68,
                         'H':72, 'L':76, 'CTRL':17, 'Q':81}

    def tryToConnect(self):
        thread.start_new_thread(self.connect,())

    def quit(self):
        try:
            self.sock.close()
        except: AttributeError
        sys.exit()

    def connect(self):
        addr = None

        print('Searching for bluetooth connections')
        uuid = '00001101-0000-1000-8000-00805F9B34FB'
        service_matches = find_service( uuid = uuid, address = addr )
        print("Connections found: "+str(service_matches))

        if len(service_matches) == 0:
            #self.ui.lineEdit.setText("Could not find device")
            return

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        # Create the client socket
        self.sock=BluetoothSocket( RFCOMM )
        self.sock.connect((host, port))
        #self.ui.lineEdit.setText("Connection established.")

    def keyPress(self, key):
        if key == self.keycodes['H']:
            if self.action_dict['horn'] == 0:
                self.action_dict['horn'] = 1
                self.sock.send(binascii.a2b_hex(self.dict['HORN_ON']))
            else:
                self.action_dict['horn'] = 0
                self.sock.send(binascii.a2b_hex(self.dict['HORN_OFF']))

        if key == self.keycodes['W']:
            self.acceleration += 2
            if self.acceleration >= 0:
                self.acceleration = min(self.acceleration, 62)
                self.sock.send(binascii.a2b_hex(self.dict['SPEED_FRONT'][self.acceleration]))
            else:
                self.sock.send(binascii.a2b_hex(self.dict['SPEED_BACK'][abs(self.acceleration)]))

        if key == self.keycodes['S']:
            self.acceleration -= 2
            if self.acceleration >= 0:
                self.sock.send(binascii.a2b_hex(self.dict['SPEED_FRONT'][self.acceleration]))
            else:
                self.acceleration = max(self.acceleration, -62)
                self.sock.send(binascii.a2b_hex(self.dict['SPEED_BACK'][abs(self.acceleration)]))

        if key == self.keycodes['A']:
            self.steering -= 4
            if self.steering >= 0:
                self.sock.send(binascii.a2b_hex(self.dict['STEER_RIGHT'][self.steering]))
            else:
                self.steering = max(self.steering, -62)
                self.sock.send(binascii.a2b_hex(self.dict['STEER_LEFT'][abs(self.steering)]))

        if key == self.keycodes['D']:
            self.steering += 4
            if self.steering >= 0:
                self.steering = min(self.steering, 62)
                self.sock.send(binascii.a2b_hex(self.dict['STEER_RIGHT'][self.steering]))
            else:
                self.sock.send(binascii.a2b_hex(self.dict['STEER_LEFT'][abs(self.steering)]))

        if key == self.keycodes['SPACE']:
            self.acceleration = 0
            self.sock.send(binascii.a2b_hex(self.dict['NO_SPEED']))
            #where does an astronaut go to drink?
            #the space bar

        if key == self.keycodes['CTRL']:
            self.steering = 0
            self.sock.send(binascii.a2b_hex(self.dict['NO_STEER']))

        if key == self.keycodes['L']:
            if self.action_dict["lights"] == 1:
                self.sock.send(binascii.a2b_hex(self.dict['LIGHTS_OFF']))
                self.action_dict["lights"] = 0
            else:
                self.action_dict["lights"] = 1
                self.sock.send(binascii.a2b_hex(self.dict['LIGHTS']))




def main(): #unused
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
