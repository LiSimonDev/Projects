from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont, QTextCursor
import threads
from pyautogui import sleep
import VisualBot
import loader

class Help(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.text = QtWidgets.QTextEdit("")
        self.text.setReadOnly(True)
        with open("help.html", 'r') as f:
            self.text.textCursor().insertHtml(f.read())
        self.text.setFont(QFont(self.font().family(), 13))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.setGeometry(0, 0, 600, 500)
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.text.moveCursor(QTextCursor.Start)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisualBot")

        self.data_order = ['img', 'delay', 'clicks', 'x', 'y', 'next cfg', 'error', 'active']

        self.slot = 1

        self.open = True

        self.threads_switch = {'t1':False, 't2':False}

        self.actions = []

        self.configs = {}

        self.help_window = Help()

        self.start = QtWidgets.QPushButton("Start (F7)")
        self.start.clicked.connect(self.open_thread_timer)

        self.stop = QtWidgets.QPushButton("Stop (F8)")
        self.stop.clicked.connect(self.stop_routine)
        self.stop.setDisabled(True)

        top_lab_inf = QtWidgets.QLabel('Start in: ')
        self.top_lab = QtWidgets.QLabel('5')

        save_but = QtWidgets.QPushButton('Save')
        save_but.clicked.connect(self.save_cfg)

        test_but = QtWidgets.QPushButton('Test')
        test_but.clicked.connect(VisualBot.test)

        help_but = QtWidgets.QPushButton('Help')
        help_but.clicked.connect(self.activate_help)

        loop_lab = QtWidgets.QLabel('Loop')
        self.loop_but = QtWidgets.QCheckBox()

        self.cfg_buts = []
        for i in range(9):
            self.cfg_buts.append(QtWidgets.QPushButton(str(i+1)))

        add_button = QtWidgets.QPushButton("add action")
        add_button.clicked.connect(self.add_action)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.setAlignment(Qt.AlignBottom)
        top_lay = QtWidgets.QVBoxLayout()
        top_lay.setAlignment(Qt.AlignTop)

        top_add_lay = QtWidgets.QHBoxLayout()
        top_add_lay.addStretch()
        top_add_lay.addWidget(add_button)
        top_add_lay.addStretch()

        top_info_lay = QtWidgets.QHBoxLayout()
        top_info_lay.addStretch()
        top_info_lay.addWidget(top_lab_inf)
        top_info_lay.addWidget(self.top_lab)
        i = 0
        for b in self.cfg_buts:
            i += 1
            b.clicked.connect(lambda ignore, i=i: self.change_routine(i))
            b.setMaximumWidth(20)
            top_info_lay.addWidget(b)
        top_info_lay.addWidget(loop_lab)
        top_info_lay.addWidget(self.loop_but)
        top_info_lay.addWidget(save_but)
        top_info_lay.addWidget(test_but)
        top_info_lay.addWidget(help_but)
        top_info_lay.addStretch()



        self.top_act_lay = QtWidgets.QVBoxLayout()

        top_lay.addLayout(top_info_lay)
        top_lay.addLayout(self.top_act_lay)
        top_lay.addLayout(top_add_lay)
        top_lay.addStretch()

        bot_lay = QtWidgets.QHBoxLayout()
        bot_lay.addStretch()
        bot_lay.addWidget(self.start)
        bot_lay.addWidget(self.stop)
        bot_lay.addStretch()

        main_lay.addLayout(top_lay)
        main_lay.addLayout(bot_lay)
        self.setLayout(main_lay)

        self.load_cfg()

    def start_routine(self):
        if not self.open:
            self.open = True
            return
        self.start.setDisabled(True)
        self.stop.setDisabled(False)
        self.open_thread_start()

    def close_routine_for1(self):
        self.open = False

    def stop_routine(self):
        self.stop.setDisabled(True)
        self.start.setDisabled(False)

        if self.threads_switch['t1']:
            self.worker.stop()

        if self.threads_switch['t2']:
            self.worker_t.stop()


    def add_action(self, data = False):
        if len(self.actions) > 9:
            return
        action = QtWidgets.QHBoxLayout()
        action.setAlignment(Qt.AlignTop)

        label_p = QtWidgets.QLabel("Img Path:")
        line_p = QtWidgets.QLineEdit("")
        line_p.setMinimumWidth(300)
        action.addWidget(label_p)
        action.addWidget(line_p)

        label_d = QtWidgets.QLabel("Delay:")
        line_d = QtWidgets.QLineEdit("")
        action.addWidget(label_d)
        action.addWidget(line_d)

        label_c = QtWidgets.QLabel("Clicks:")
        line_c = QtWidgets.QLineEdit("")
        action.addWidget(label_c)
        action.addWidget(line_c)

        label_cx = QtWidgets.QLabel("X:")
        line_cx = QtWidgets.QLineEdit("")
        action.addWidget(label_cx)
        action.addWidget(line_cx)

        label_cy = QtWidgets.QLabel("Y:")
        line_cy = QtWidgets.QLineEdit("")
        action.addWidget(label_cy)
        action.addWidget(line_cy)

        label_n = QtWidgets.QLabel("Next:")
        line_n = QtWidgets.QLineEdit("")
        action.addWidget(label_n)
        action.addWidget(line_n)

        label_e = QtWidgets.QLabel("Error:")
        line_e = QtWidgets.QLineEdit("")
        action.addWidget(label_e)
        action.addWidget(line_e)

        chk_act = QtWidgets.QCheckBox("Active")
        action.addWidget(chk_act)
        chk_act.click()



        del_but = QtWidgets.QPushButton("Delete")
        del_but.clicked.connect(lambda: self.delete_action(action))
        action.addWidget(del_but)

        self.actions.append(action)
        self.top_act_lay.addLayout(action)

        if data != False:
            line_p.setText(str(data['img']))
            line_d.setText(str(data['delay']))
            line_c.setText(str(data['clicks']))
            line_cx.setText(str(data['x']))
            line_cy.setText(str(data['y']))
            line_n.setText(str(data['next cfg']))
            line_e.setText(str(data['error']))
            if data['active'] == 'False':
                chk_act.click()

    def delete_action(self, action):
        for i in reversed(range(action.count())):
            action.itemAt(i).widget().setParent(None)
        self.actions.remove(action)
        action.deleteLater()

    def open_thread_start(self):
        data = []
        for action in self.actions:
            data.append(self.unwrap_action_data(action))
        self.thread = QThread()
        self.worker = threads.start_sequence(data, self.loop_but.isChecked(), self.configs)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start_seq)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.unlock_thread('t1'))
        self.thread.finished.connect(self.stop_routine)
        self.thread.start()
        self.threads_switch['t1'] = True


    def open_thread_timer(self):
        self.start.setDisabled(True)
        self.stop.setDisabled(False)
        self.thread_t = QThread()
        self.worker_t = threads.timer(5)
        self.worker_t.moveToThread(self.thread_t)

        self.thread_t.started.connect(self.worker_t.decrement)
        self.worker_t.progress.connect(self.edit_top_info)

        self.worker_t.finished.connect(self.thread_t.quit)
        self.worker_t.finished.connect(self.worker_t.deleteLater)
        self.thread_t.finished.connect(self.thread_t.deleteLater)
        self.thread_t.finished.connect(lambda: self.unlock_thread('t2'))
        self.thread_t.finished.connect(self.start_routine)

        self.worker_t.c.connect(self.thread_t.quit)
        self.worker_t.c.connect(self.worker_t.deleteLater)
        self.worker_t.c.connect(self.close_routine_for1)


        self.thread_t.start()
        self.threads_switch['t2'] = True


    def edit_top_info(self, time):
        self.top_lab.setText(str(time))

    def unwrap_action_data(self, action):
        data = {}
        data_type_num = 0
        switch_b = 0
        for i in range(action.count()):
            wid = action.itemAt(i).widget()
            if isinstance(wid, QtWidgets.QLineEdit):
                data[self.data_order[data_type_num]] = wid.text()
                data_type_num += 1
            elif isinstance(wid, QtWidgets.QCheckBox) and switch_b == 0:
                switch_b += 1
                data['active'] = wid.isChecked()
        return data

    def save_cfg(self):
        data = {}
        i = 0
        for action in self.actions:
            i += 1
            data[str(i)] = self.unwrap_action_data(action)
        if len(data) == 0:
            return
        loader.save_config(data, self.slot)
        self.load_cfg(self.slot)

    def load_cfg(self, routine = 1):
        data = loader.load_config()
        self.configs = data
        self.change_routine(routine)

    def change_routine(self, slot):
        self.slot = slot
        for i in reversed(range(len(self.actions))):
            self.delete_action(self.actions[i])
        for action_data in self.configs[str(slot)].items():
            print(action_data[1])
            self.add_action(action_data[1])


        for but in self.cfg_buts:
            but.setStyleSheet("QPushButton"                             
                             "{"
                             "}"
                             )

        self.cfg_buts[slot-1].setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             )




    def unlock_thread(self, t):
        self.threads_switch[t] = False

    def from_key_start(self): #direct call of open_thread_timer crashes
        self.start.click()

    def activate_help(self):
        self.help_window.show()




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    app.exec_()
