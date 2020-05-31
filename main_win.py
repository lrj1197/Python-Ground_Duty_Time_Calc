from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
import pandas as pd
from math import *
import datetime
import webbrowser
import SETTINGS

class Main_Win(QWidget):

    def __init__(self):
        super().__init__()
        self.dur = 0
        self.leg_0 = 1
        self.leg_1 = 1
        self.trans_types_dict = {'ICN Pick Up':90/60,
                                'ICN Drop Off':90/60,
                                'Scene':60/60,
                                'IFT':30/60,
                                'Paitent Drop Off':30/60,
                                'Paitent Pick Up':30/60,
                                'Fuel Stop':0,
                                'RTB':0}
        try:
            self.df = pd.read_csv('Hospital_locs.csv')
            self.df_TT = pd.read_csv('Travel_Time.csv')
        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            error_dialog = QErrorMessage()
            error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))
        if (1):
            self.calc = QPushButton('Calculate', self)
            self.calc.setCheckable(True)
            self.calc.move(10, 10)
            self.calc.setStyleSheet("background-color: green")
            self.calc.clicked.connect(self.CALC)

            self.exit = QPushButton("Exit", self)
            self.exit.setCheckable(True)
            self.exit.move(10, 40)
            self.exit.setStyleSheet("background-color: red")
            self.exit.clicked.connect(self.EXIT)

            self.set = QPushButton('Settings', self)
            self.set.setCheckable(True)
            self.set.move(10, 130)
            self.set.setStyleSheet("background-color: orange")
            self.set.clicked.connect(self.SET)

            self.help = QPushButton('Help', self)
            self.help.setCheckable(True)
            self.help.move(10, 100)
            self.help.setStyleSheet("background-color: orange")
            self.help.clicked.connect(self.HELP)

            self.clear = QPushButton('Clear', self)
            self.clear.setCheckable(True)
            self.clear.move(10, 70)
            self.clear.setStyleSheet("background-color: blue")
            self.clear.clicked.connect(self.CLEAR)

            self.destination_lst = QTextEdit(self)
            self.destination_lst.move(300,100)
            self.destination_lst.resize(200,200)
            self.destination_lst.setReadOnly(True)
            self.destination_lst_L = QLabel('Destination list',self)
            self.destination_lst_L.move(300,75)

            self.trans_type_lst = QTextEdit(self)
            self.trans_type_lst.move(550,100)
            self.trans_type_lst.resize(200,200)
            self.trans_type_lst.setReadOnly(True)
            self.trans_type_lst_L = QLabel('Transport list',self)
            self.trans_type_lst_L.move(550,75)

            self.end_time = QLineEdit(self)
            self.end_time.move(100,200)
            self.end_time.resize(100,40)
            f = self.end_time.font()
            f.setPointSize(20)
            self.end_time.setFont(f)
            self.end_time_L = QLabel("End Time (HH:MM)",self)
            self.end_time_L.move(50,170)
            self.end_time_L.setFont(QFont('Times', 18))
            self.end_time.setReadOnly(True)

            self.end_dur = QLineEdit(self)
            self.end_dur.move(110,100)
            self.end_dur.resize(70,30)
            self.end_dur.setReadOnly(True)
            self.end_dur_L = QLabel("Duration (HRS)",self)
            self.end_dur_L.move(110,80)

            self.start_loc = QComboBox(self)
            self.start_loc.move(100, 10)
            self.start_loc.addItem("Start")
            self.start_loc.addItems(['Leb Base', 'Manchester Base', 'Burlington Base'])

            self.end_loc = QComboBox(self)
            self.end_loc.move(300, 40)
            self.end_loc.resize(150, 25)
            self.end_loc.addItem("Destination")
            self.end_loc.addItems(self.df['Location'])
            self.end_loc.addItems(self.df_TT['Hospital'])
            self.end_loc.setMaxVisibleItems(10)
            self.end_loc.currentIndexChanged.connect(self._add_item_to_dest_list)

            self.msg = QTextEdit(self)
            self.msg.move(300,350)
            self.msg.resize(450,150)
            self.msg.setReadOnly(True)
            self.msg_L = QLabel("Messages",self)
            self.msg_L.move(500, 325)

            self.ifr = QCheckBox("IFR",self)
            self.ifr.move(230, 100)

            self.vfr = QCheckBox("VFR",self)
            self.vfr.move(230, 140)

            self.trans_meth = QComboBox(self)
            self.trans_meth.move(100, 40)
            self.trans_meth.addItem("Transport method")
            self.trans_meth.addItems(['Air', 'Ground'])

            self.trans_type = QComboBox(self)
            self.trans_type.move(550, 40)
            self.trans_type.addItem("Transport Type")
            self.trans_type.addItems(list(self.trans_types_dict.keys()))
            self.trans_type.currentIndexChanged.connect(self._add_item_to_trans_list)

        self.label = QLabel(self)
        pixmap = QPixmap('DHlogo_icon.jpg')
        self.label.setPixmap(pixmap)
        self.label.move(50,250)
        self.label.resize(200,100)
        self.label.setScaledContents(True)
        self.version = QLabel("Version {}".format(SETTINGS.__VERSION__), self)
        self.version.move(50,375)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('DHMC Duty Time Calculator')
        webbrowser.open('https://www.google.com/maps/', new=2)
        self.setStyleSheet('color: rgb(250,250,250); background-color: rgb(77,77,77);')
        self.show()

    def _add_item_to_dest_list(self):
        if self.end_loc.currentText() == "Destination":
            pass
        else:
            self.destination_lst.append("Leg {} ->{}\n".format(self.leg_1,self.end_loc.currentText()))
            self.leg_1 += 1

    def _add_item_to_trans_list(self):
        if self.trans_type.currentText() == "Transport type":
            pass
        else:
            self.trans_type_lst.append("Leg {} ->{}\n".format(self.leg_0,self.trans_type.currentText()))
            self.leg_0 += 1

    def _get_dist_from_lat_long(lat1,lat2,long1,long2,travel_meth):
        if travel_meth == 'Air':
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * asin(sqrt(a))
            # Radius of earth in kilometers. Use 3956 for miles
            r = 3956
            v = 125*1.15
            # calculate the result
            return round((c * r/v),3)
        elif travel_meth == 'Ground':
            pass
        else:
            exc_type, exc_obj, tb = sys.exc_info()
            e = 'Not a valid travel method'
            error_dialog = QErrorMessage()
            error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))

    def CALC(self):
        # this is going to change a lot in the next few commits
        self.end_time.setText("")
        self.dur = 0
        nodes = []
        # The math module contains a function named
        # radians which converts from degrees to radians.
        # seq 2
        try: #seq 3

            destinations = self.destination_lst.toPlainText()
            total_travel_time = 0
            if self.trans_meth.currentText() == 'Ground':
                GTT = GroundTravelTimeDialog(self)
                if GTT.exec_():
                    time = GTT.TravelTime.text()
                    try:
                        time_hrs = float(time.split(":")[0])
                        time_min = float(time.split(":")[1])
                        total_travel_time += time_hrs + time_min/60
                    except:
                        exc_type, exc_obj, tb = sys.exc_info()
                        error_dialog = QErrorMessage()
                        error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))
                trans_nodes = self.trans_type_lst.toPlainText().split('\n')
                for i in range(len(trans_nodes)): # error raised here 5/30/20
                    if trans_nodes[i] == "":
                        pass
                    else:
                        node = trans_nodes[i].split('->')[1].rstrip()
                        total_travel_time += self.trans_types_dict[node]
            else:

                if self.ifr.isChecked() == True and self.vfr.isChecked() == False:
                    self.dur += 20/60
                elif self.ifr.isChecked() == False and self.vfr.isChecked() == True:
                     self.dur += 10/60
                elif self.ifr.isChecked() == False and self.vfr.isChecked() == False:
                     self.dur += 0
                else:
                    self.msg.append("Error 1")
                for i in range(len(destinations.split('\n'))):
                    node = destinations.split('\n')[i].split('->')[1].rstrip()
                    nodes.append(node)
                    if len(node) > 1:
                        if (node in list(self.df['Location'])) == True:
                            if self.trans_meth.currentText() == 'Air':
                                if i == 0:
                                    lon1 = radians(self.df[self.df['Location'] == self.start_loc.currentText()]['long'])
                                    lon2 = radians(self.df[self.df['Location'] == nodes[-1:]]['long'])
                                    lat1 = radians(self.df[self.df['Location'] == self.start_loc.currentText()]['lat'])
                                    lat2 = radians(self.df[self.df['Location'] == nodes[-1:]]['lat'])
                                elif i < len(destinations.split('\n')):
                                    lon1 = radians(self.df[self.df['Location'] == nodes[-2:-1]]['long'])
                                    lon2 = radians(self.df[self.df['Location'] == nodes[-1:]]['long'])
                                    lat1 = radians(self.df[self.df['Location'] == node[-2:-1]]['lat'])
                                    lat2 = radians(self.df[self.df['Location'] == nodes[-1:]]['lat'])
                                else:
                                    lon1 = radians(self.df[self.df['Location'] == nodes[-2:-1]]['long'])
                                    lon2 = radians(self.df[self.df['Location'] == nodes[-1:]]['long'])
                                    lat1 = radians(self.df[self.df['Location'] == node[-2:-1]]['lat'])
                                    lat2 = radians(self.df[self.df['Location'] == nodes[-1:]]['lat'])
                                total_travel_time += self._get_dist_from_lat_long(lat1,lat2,long1,long2,'Air')
                            elif self.trans_meth.currentText() == 'Ground':
                                pass
                            else:
                                exc_type, exc_obj, tb = sys.exc_info()
                                error_dialog = QErrorMessage()
                                error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))
                        elif (node[1].rstrip() in list(self.df_TT['Hospital'])) == True:
                            if self.trans_meth.currentText() == 'Air':
                                pass
                                if self.start_loc == 'Leb base':
                                    if self.ifr.isChecked() == True and self.vfr.isChecked() == False:
                                        time = self.df_TT['VFR DHMC'].split(':')
                                        if time[0] == "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                        elif time[0] != "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                            total_travel_time += float(time[0]) # already in hrs
                                    elif self.ifr.isChecked() == False and self.vfr.isChecked() == True:
                                        time = self.df_TT['IFR from DHMC'].split(':')
                                        if time[0] == "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                        elif time[0] != "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                            total_travel_time += float(time[0]) # already in hrs
                                elif start_loc == 'Manchester base':
                                    if self.ifr.isChecked() == True and self.vfr.isChecked() == False:
                                        time = self.df_TT['IFR from KMHT'].split(':')
                                        if time[0] == "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                        elif time[0] != "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                            total_travel_time += float(time[0]) # already in hrs
                                    elif self.ifr.isChecked() == False and self.vfr.isChecked() == True:
                                        time = self.df_TT['VFR MHT'].split(':')
                                        if time[0] == "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                        elif time[0] != "" and time[1] != "":
                                            total_travel_time += float(time[1])/60 # put everything into hrs
                                            total_travel_time += float(time[0]) # already in hrs
                                elif start_loc == 'Burlington base':
                                    pass
                                    # if self.ifr.isChecked() == True and self.vfr.isChecked() == False:
                                    #     time = self.df_TT['VFR DHMC']
                                    # elif self.ifr.isChecked() == False and self.vfr.isChecked() == True:
                                    #     time = self.df_TT['IFR DHMC']
                                # Hospital,Mileage,Ground,VFR DHMC,VFR KMHT,IFR from DHMC,IFR from KMHT,Base
                            elif self.trans_meth.currentText() == 'Ground':
                                pass
                            else:
                                exc_type, exc_obj, tb = sys.exc_info()
                                e = 'Not a valid travel method'
                                error_dialog = QErrorMessage()
                                error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))
                        else:
                            print(node[1].rstrip())

                take_off_landing_t = 6/60
                total_travel_time = round(total_travel_time + take_off_landing_t + self.dur,3)
            self.end_dur.setText("{}".format(round(total_travel_time,2)))
            current_date_and_time = datetime.datetime.now()
            hours_added = datetime.timedelta(hours = total_travel_time)
            est_end_time = current_date_and_time + hours_added
            if est_end_time.hour < 10:
                if est_end_time.minute < 10:
                    self.end_time.setText("0{}:0{}".format(est_end_time.hour,est_end_time.minute))
                else:
                    self.end_time.setText("0{}:{}".format(est_end_time.hour,est_end_time.minute))
            else:
                if est_end_time.minute < 10:
                    self.end_time.setText("{}:0{}".format(est_end_time.hour,est_end_time.minute))
                else:
                    self.end_time.setText("{}:{}".format(est_end_time.hour,est_end_time.minute))
        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            error_dialog = QErrorMessage()
            error_dialog.showMessage('ERROR: {} on line {}'.format(e, tb.tb_lineno))

    def EXIT(self):
        sys.exit()

    def SET(self):
        if sys.platform.startswith('linux'):
            os.system("nano {}".format("SETTINGS.py"))
        elif sys.platform.startswith('win32'):
            os.system("notepad {}".format("SETTINGS.py"))
        elif sys.platform.startswith('darwin'):
            pass
        else:
            pass

    def HELP(self):
        if sys.platform.startswith('linux'):
            os.system("nano {}".format("README"))
        elif sys.platform.startswith('win32'):
            os.system("notepad {}".format("README"))
        elif sys.platform.startswith('darwin'):
            pass
        else:
            pass

    def CLEAR(self):
        self.destination_lst.clear()
        self.trans_type_lst.clear()
        self.end_dur.setText("")
        self.end_time.setText("")
        self.end_loc.setCurrentText("Destination")
        self.trans_type.setCurrentText("Transport type")
        self.start_loc.setCurrentText("Start")
        self.leg_0 = 1
        self.leg_1 = 1

class GroundTravelTimeDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(GroundTravelTimeDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Ground Travel Time")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.TravelTime = QLineEdit(self)
        self.TravelTime_L = QLabel("Travel Time (HH:MM)",self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.TravelTime_L)
        self.layout.addWidget(self.TravelTime)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = Main_Win()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
