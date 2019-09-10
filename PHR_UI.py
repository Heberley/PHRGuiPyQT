# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial.tools.list_ports as port_list
import serial
from time import *

#Variable global con la lista de puertos
ports = list(port_list.comports())


class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(300, 300)
        self.setWindowTitle("Cuadro de diálogo")
        self.etiqueta = QLabel(self)

class MainWindowPHR(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("phr.ui", self)
        _translate = QtCore.QCoreApplication.translate


        self.dialogo = Dialogo()

        #Definiendo el Boton SET
        self.SetButton.clicked.connect(self.SetRoutine)
        #Definiendo el Boton Resume
        self.ResumeButton.clicked.connect(self.ResumeRoutine)
        #Definiendo metodos de los slider
        self.ZSlider.valueChanged.connect(self.getValueZ)
        self.YSlider.valueChanged.connect(self.getValueY)
        self.TiltSlider.valueChanged.connect(self.getValueTilt)
        self.PowerDial.valueChanged.connect(self.getValueDial)
        #Setting the initial value for the sliderZ
        global Zvalue
        Zvalue=self.ZSlider.value()
        self.labelZvalue.setText(str(('%.2f'%(Zvalue*(100.0/1023))))+" %")
        #Setting the initial value for the silderY
        global Yvalue
        Yvalue=self.YSlider.value()
        self.labelYvalue.setText(str(('%.2f'%(Yvalue*(100.0/1023))))+" %")
        #Setting the initial value for the TiltSilder
        global Tiltvalue
        Tiltvalue=self.TiltSlider.value()
        self.labelTiltvalue.setText(str(('%.2f'%(Tiltvalue*(100.0/1023))))+" %")
        #Setting the initial value for the PowerDial
        global PowerValue
        PowerValue=self.PowerDial.value()
        self.labelPower.setText(str(('%.2f'%(PowerValue*(100.0/1023))))+" %")
        
        
        i=0
        for p in ports:
            self.comboBoxPuertos.setItemText(i, _translate("MainWindow", p.device))
            i=1+1      

    def SetRoutine(self):
        
        try:
            self.sendData(str(Zvalue)+"z"+'\r')
            self.sendData(str(Yvalue)+"y"+'\r')
            self.sendData(str(Tiltvalue)+"t"+'\r')
            self.sendData(str(PowerValue)+"l"+'\r')
        except  Exception as e:
                print(e)

        
        
        #port = self.serial.Serial(ports[item].device, baudrate=9600, timeout=0.1)

    def getValueZ(self):
        Zvalue=self.ZSlider.value()
        self.labelZvalue.setText(str(('%.2f'%(Zvalue*(100.0/1023))))+" %")
        if self.checkBoxAxis.isChecked():
            try:
                self.sendData(str(Zvalue)+"z"+'\r')
            except  Exception as e:
                print(e)

    def getValueY(self):
        Yvalue=self.YSlider.value()
        self.labelYvalue.setText(str(('%.2f'%(Yvalue*(100.0/1023))))+" %")
        if self.checkBoxAxis.isChecked():
            try:
                self.sendData(str(Yvalue)+"y"+'\r')
            except  Exception as e:
                print(e)
    
    def getValueTilt(self):
        Tiltvalue=self.TiltSlider.value()
        self.labelTiltvalue.setText(str(('%.2f'%(Tiltvalue*(100.0/1023))))+" %")
        if self.checkBoxAxis.isChecked():
            try:
                self.sendData(str(Tiltvalue)+"t"+'\r')
            except  Exception as e:
                print(e)
   
    def getValueDial(self):
        
        PowerValue=self.PowerDial.value()
        self.labelPower.setText(str(('%.2f'%(PowerValue*(100.0/1023))))+" %")
        
        if self.checkBoxLaser.isChecked():
            try:
                self.sendData(str(PowerValue)+"l"+'\r')
            except  Exception as e:
                print(e)

    def ResumeRoutine(self):
        self.dialogo.etiqueta.setText("Diálogo abierto desde la ventana principal")
        self.dialogo.exec_()


    
    def sendData(self,args):
        
        item = self.comboBoxPuertos.currentIndex()
        port = serial.Serial(ports[item].device, baudrate=9600, timeout=0.1)

        port.write(args.encode(encoding='ascii'))
        sleep(0.1)
        s = port.read(10)
        print(s)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = MainWindowPHR()
    dialogo.show()
    app.exec_()



