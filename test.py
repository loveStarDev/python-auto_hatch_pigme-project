import datetime
import os
import sys
import api2
import api3
import threading
import pandas as pd
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# main ui를 읽어옵니다.
form_class = uic.loadUiType("./egg/main.ui")[0]


class IOT(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 변수 선언
        self.current_folder_path = os.getcwd()
        self.batch_file = "sender.bat"
        self.empty_img = QPixmap()
        self.setting_file = None
        self.is_exist = None
        self.th = None
        self.th1 = None
        self.fan = None

        # UI 세팅
        self.hide_all()

        # 이벤트 등록
        self.action_setting.triggered.connect(self.show_setting)
        self.action_setchange.triggered.connect(self.show_change)
        self.action_reg.triggered.connect(self.show_reg)
        self.action_help.triggered.connect(self.show_help)
        self.action_delete.triggered.connect(self.show_edit)

        self.btn_x1.clicked.connect(self.hide_all)
        self.btn_x2.clicked.connect(self.hide_all)
        self.btn_x3.clicked.connect(self.hide_all)
        self.btn_x4.clicked.connect(self.hide_all)

        self.action_init.triggered.connect(self.init_setting)
        self.btn_del.clicked.connect(self.del_bird)
        self.btn_reg.clicked.connect(self.reg_bird)
        self.cb_bird.currentTextChanged.connect(self.fill_option)

        self.init_load()
        self.set_bird()

        self.btn_rolling.clicked.connect(self.rolling)
        self.btn_start.clicked.connect(self.save_setting)

    def return_time(self):
        now = datetime.datetime.now()
        return now

    def check_time(self):
        if self.is_exist:
            status = pd.read_csv('./status.csv')
            now = self.return_time()

            saved_date = datetime.datetime.strptime(status.iloc[0]['checktime'], '%Y-%m-%d %H:%M:%S.%f')
            roll_time = now - saved_date
            left_time = int(roll_time.total_seconds() / 60)

            if left_time >= int(status.iloc[0]['set_roll']):
                left_time = 0
                status.loc.__setitem__((0, 'checktime'), datetime.datetime.now())
                status.to_csv('./status.csv')

                # motor On code
                api3.req('PUT', 'Motor')
                print('send req')

            left_str = "남은 전란 시간 : " + str(int(status.iloc[0]['set_roll']) - left_time) + " 분"

            self.lb_rolling.setText(left_str)

            self.th1 = threading.Timer(10, self.check_time).start()
            """self.th1.daemon = True
            self.th1.start()"""

        else:
            return 0

    def rolling(self):
        status = pd.read_csv('./status.csv')
        status.loc.__setitem__((0, 'checktime'), str(datetime.datetime.now()))
        status.to_csv('./status.csv')

        now = self.return_time()

        saved_date = datetime.datetime.strptime(status.iloc[0]['checktime'], '%Y-%m-%d %H:%M:%S.%f')
        roll_time = now - saved_date
        left_time = int(roll_time.total_seconds() / 60)

        # motor On code
        api3.req('PUT', 'Motor')
        print('send req')

        left_str = "남은 전란 시간 : " + str(int(status.iloc[0]['set_roll']) - left_time) + " 분"

        self.lb_rolling.setText(left_str)

    def set_now(self):
        temp, hum = api2.return_value()
        status = pd.read_csv('./status.csv')
        pix = QPixmap()

        if temp is None:
            QMessageBox.about(self, '연결', '연결상태를 확인하세요')
            return 0

        if self.is_exist:
            self.lb_non.setText(str(temp))
            self.lb_nsuep.setText(str(hum))

            if float(status.iloc[0]['set_tem']) < temp:
                self.fan = True
                api3.req('PUT', "Fan")
                print('send req')

        if self.is_exist:
            # self.th.start()
            threading.Timer(4.2, self.set_now).start()
            if (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days == 0:
                pix.load('./egg/egg7.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 3:
                pix.load('./egg/egg6.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 6:
                pix.load('./egg/egg5.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 9:
                pix.load('./egg/egg4.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 12:
                pix.load('./egg/egg3.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 15:
                pix.load('./egg/egg2.png')
            elif (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 18:
                pix.load('./egg/egg1.png')
            else:
                pix.load('./egg/egg0.png')

            self.lb_egg.setPixmap(QPixmap(pix))
            print('start thread')
        else:
            self.lb_non.setText('')
            self.lb_nsuep.setText('')
            self.lb_egg.setPixmap(self.empty_img)
            print(self.is_exist)
            print('end thread')
            return 0

    def del_bird(self):
        reply = QMessageBox.information(self, '삭제', '삭제 하시겠습니까?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            bird = pd.read_csv('./bird.csv')
            row = self.listWidget.currentRow()
            temp = self.listWidget.item(row).text()
            self.listWidget.takeItem(row)
            self.cb_bird.removeItem(row + 1)
            bird = bird.drop(bird[bird.bird == temp].index)
            bird = bird.loc[:, ['bird', 'set_tem', 'set_hum', 'set_roll', 'days']]
            bird.to_csv('./bird.csv')
            QMessageBox.about(self, '삭제', '삭제되었습니다')
        elif reply == QMessageBox.No:
            pass

    def set_bird(self):
        bird = pd.read_csv('./bird.csv')
        bird = bird.loc[:, ['bird']]
        self.cb_bird.addItem('선택하시오')
        for b in bird['bird']:
            self.cb_bird.addItem(b)
            self.listWidget.addItem(b)

    def init_load(self, ch=True):
        status = pd.read_csv('./status.csv')
        status = status.loc[:, ['bird', 'set_tem', 'set_hum', 'set_roll', 'name', 'sday', 'eday', 'checktime']]

        try:
            self.lb_name.setText(str(status.iloc[0]['name']))
            self.lb_son.setText(str(status.iloc[0]['set_tem']))
            self.lb_ssuep.setText(str(status.iloc[0]['set_hum']))
            self.lb_sdate.setText(str(datetime.date.today()))
            self.lb_sdate.setText('SET : ' + str(status.iloc[0]['sday']))
            self.lb_edate.setText('END : ' + str(status.iloc[0]['eday']))

            if (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days <= 3:
                self.lb_dday.setStyleSheet('color:red; font: 47pt "HY헤드라인M"')
            else:
                self.lb_dday.setStyleSheet('color:black; font: 47pt "HY헤드라인M"')
            if (datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days == 0:
                self.lb_dday.setText('D - Day')
            else:
                self.lb_dday.setText('D - ' + str((datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days))

            self.is_exist = True
            self.action_setting.setEnabled(False)
            self.action_setchange.setEnabled(True)

            if ch:
                self.set_now()
                self.check_time()

        except Exception as ex:
            print(str(ex))
            print(187)
            self.is_exist = False
            self.action_setting.setEnabled(True)
            self.action_setchange.setEnabled(False)
            self.lb_rolling.setText('')
            self.lb_name.setText('')
            self.lb_dday.setText('')
            self.lb_sdate.setText('')
            self.lb_edate.setText('')
            self.lb_son.setText('')
            self.lb_ssuep.setText('')
            self.lb_non.setText('')
            self.lb_nsuep.setText('')

    def save_setting(self):
        if self.btn_start.text() == '시작':
            temp = pd.DataFrame(
                {'bird': [self.cb_bird.currentText()], 'set_tem': [self.le_on.text()], 'set_hum': [self.le_suep.text()],
                 'set_roll': [self.le_roll.text()], 'name': [self.le_name.text()], 'sday': [datetime.date.today()],
                 'eday': [datetime.date.today() + datetime.timedelta(days=int(self.le_birth.text()))], 'checktime': [self.return_time()]})

            temp.to_csv('./status.csv')
            QMessageBox.about(self, '시작', '설정이 완료되었습니다')
            self.gb_setting.hide()
            self.init_load()

        else:
            status = pd.read_csv('./status.csv')
            status.loc.__setitem__((0, 'set_tem'), self.le_on.text())
            status.loc.__setitem__((0, 'set_hum'), self.le_suep.text())
            status.loc.__setitem__((0, 'set_roll'), self.le_roll.text())
            status.loc.__setitem__((0, 'name'), self.le_name.text())
            status.loc.__setitem__((0, 'eday'), datetime.date.today() + datetime.timedelta(days=int(self.le_birth.text())))
            status.loc.__setitem__((0, 'HatchTime'), self.le_rdays.text())

            status = status.loc[:, ['bird', 'set_tem', 'set_hum', 'set_roll', 'name', 'sday', 'eday', "checktime"]]
            status.to_csv('./status.csv')
            QMessageBox.about(self, '변경', '설정이 변경되었습니다')
            self.gb_setting.hide()
            self.init_load(ch=False)

    def init_setting(self):
        reply = QMessageBox.information(self, '초기화', '초기화 하시겠습니까?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.is_exist:
                self.is_exist = False
                status = pd.read_csv('./status.csv')
                status = status.drop(0)
                self.lb_dday.setStyleSheet('color:black; font: 47pt "HY헤드라인M"')
                status = status.loc[:, ['bird', 'set_tem', 'set_hum', 'set_roll', 'name', 'sday', 'eday', "checktime"]]
                status.to_csv('./status.csv')
                QMessageBox.about(self, '초기화', '초기화되었습니다')
                self.init_load(False)
            else:
                pass
        else:
            pass

    def fill_option(self):
        if self.cb_bird.currentText() == '선택하시오':
            self.le_on.setText('')
            self.le_suep.setText('')
            self.le_roll.setText('')
            self.le_name.setText('')
            self.le_birth.setText('')
        else:
            bird = pd.read_csv('./bird.csv')
            temp = bird['bird'] == self.cb_bird.currentText()
            temp = bird[temp]
            self.le_on.setText(str(temp.iloc[0]['set_tem']))
            self.le_suep.setText(str(temp.iloc[0]['set_hum']))
            self.le_roll.setText(str(temp.iloc[0]['set_roll']))
            self.le_birth.setText(str(temp.iloc[0]['days']))

    def reg_bird(self):
        bird = pd.read_csv('./bird.csv', )
        if self.le_rbird.text() is None or self.le_ron.text() is None or self.le_rroll.text() is None or self.le_rsuep.text() is None or self.le_rdays.text() is None:
            QMessageBox.about(self, '경고', '아래 빈칸을 모두 입력하시오')
        else:
            temp = pd.DataFrame(
                {'bird': [self.le_rbird.text()], 'set_tem': [self.le_ron.text()], 'set_hum': [self.le_rsuep.text()],
                 'set_roll': [self.le_rroll.text()], 'days': [self.le_rdays.text()]})
            bird = pd.concat([bird, temp], sort=False, join='inner')
            bird.to_csv('./bird.csv', encoding='utf-8-sig')
            self.cb_bird.addItem(self.le_rbird.text())
            self.listWidget.addItem(self.le_rbird.text())
            QMessageBox.about(self, '저장', '저장되었습니다!')
            self.gb_reg.hide()

    def show_change(self):
        status = pd.read_csv('./status.csv')
        self.btn_start.setText("설정 변경")
        for i in range(self.cb_bird.count()):
            if str(status.iloc[0]['bird']) == self.cb_bird.itemText(i):
                self.cb_bird.setCurrentIndex(i)
        self.le_on.setText(str(status.iloc[0]['set_tem']))
        self.le_suep.setText(str(status.iloc[0]['set_hum']))
        self.le_roll.setText(str(status.iloc[0]['set_roll']))
        self.le_name.setText(str(status.iloc[0]['name']))
        self.le_birth.setText(
            str((datetime.datetime.strptime(status.iloc[0]['eday'], '%Y-%m-%d').date() - datetime.date.today()).days))
        self.gb_setting.show()

    """
    **** show/hide event function ****
    hide_all : 버튼을 눌렀을시 뜨는 GroupBox 모두 hide 한다.
    show_그룹박스명 : 메뉴의 action 버튼을 누르면 그룹박스가 show 된다.
    [목적] UI창 관리
    """

    def show_help(self):
        self.hide_all()
        self.gb_howto.show()

    def show_setting(self):
        self.hide_all()
        self.btn_start.setText('시작')
        self.gb_setting.show()

    def show_edit(self):
        self.hide_all()
        self.gb_edit.show()

    def show_reg(self):
        self.hide_all()
        self.le_rbird.setText('')
        self.le_ron.setText('')
        self.le_rsuep.setText('')
        self.le_rroll.setText('')
        self.le_rdays.setText('')
        self.gb_reg.show()

    def hide_all(self):
        self.gb_edit.hide()
        self.gb_reg.hide()
        self.gb_setting.hide()
        self.gb_howto.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoWindow = IOT()
    demoWindow.show()
    app.exec_()
