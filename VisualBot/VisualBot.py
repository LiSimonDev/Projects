import gui
import scan
import keyboard

def test():
    scan.test('img1.png')
    scan.test('img2.png')
    scan.test('img3.png')
    scan.test('img4.png')

def ktest(txt):
    print(txt)

if __name__ == "__main__":
    app = gui.QtWidgets.QApplication([])

    widget = gui.MyWidget()
    keyboard.add_hotkey('f8', widget.stop_routine)
    keyboard.add_hotkey('f7', widget.from_key_start)
    widget.resize(800, 600)
    widget.show()

    app.exec_()

