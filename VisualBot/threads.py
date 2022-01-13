from PyQt5.QtCore import QObject, QThread, pyqtSignal
from pyautogui import sleep
import VisualBot
import scan

class start_sequence(QObject):
    finished = pyqtSignal()
    def __init__(self, data, loop, alldata):
        super().__init__()
        self.data = data.copy()
        self.thread()
        self.active = True
        self.chk_loop = loop
        self.alldata = alldata.copy()
        self.next_cfg = '0'
        self.err = ''

    def start_seq(self):
        ret = self.look_for_then_click(self.data, self.chk_loop)
        while ret == '1':
            ret = self.look_for_then_click(self.data, self.chk_loop)
        print(ret)
        self.finished.emit()

    def look_for_then_click(self, data, chk_loop):
        print('starting')
        loop = True
        while loop:
            loop = chk_loop
            act_no = 0
            for act in data:
                if act['active']:
                    if not self.active:
                        return 'Canceled'
                    if act['delay'] == '':
                        act['delay'] = 0
                    if act['x'] != '' and act['y'] != '':
                        x = float(act['x'])
                        y = float(act['y'])
                        if act['clicks'] != '':
                            for _ in range(int(act['clicks'])):
                                if not self.active:
                                    return 'Canceled'
                                scan.click(x, y, act['delay'])
                        else:
                            scan.click(x, y, act['delay'])

                    else:
                        i = 0
                        x, y, z = scan.get_click_point(act['img'])
                        while not z:
                            if not self.active:
                                return 'Canceled'
                            sleep(0.1)
                            print('asdf')
                            x, y, z = scan.get_click_point(act['img'])
                            i += 1
                            if i == 1:  # drops search after 10 tries
                                self.load_next_cfg(self.alldata[act['error']].copy())
                                self.err = act['error']
                                print(act['img'])
                                break
                        if z:
                            scan.click(x, y, act['delay'])
                    if act['next cfg'] != '':
                        self.next_cfg = act['next cfg']
                    else:
                        self.next_cfg = ''
                act_no += 1
                if act_no == len(data) and self.next_cfg != '':
                    if self.err != '':
                        self.load_next_cfg(self.alldata[self.next_cfg].copy())
                    else:
                        self.load_next_cfg(self.alldata[self.err].copy())
                    sleep(1)
                    return '1'
        return 'Success'

    def load_next_cfg(self, dat):
        self.data = []
        keys = dat.keys()
        for i in range(9):
            if str(i) in keys:
                new_data = dat[str(i)]

                if type(new_data['active']) != bool:
                    if new_data['active'] == 'True':
                        new_data['active'] = True
                    else:
                        new_data['active'] = False

                self.data.append(new_data)



    def stop(self):
        self.active = False

class timer(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    c = pyqtSignal()

    def __init__(self, time):
        super().__init__()
        self.time = time
        self.active = True

    def decrement(self):
        while self.time > 0:
            if not self.active:
                print('Canceled timer')
                self.c.emit()
                return
            self.time -= 1
            self.progress.emit(self.time)
            sleep(1)
        self.finished.emit()

    def stop(self):
        self.active = False
