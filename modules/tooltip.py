from pyautogui import position as mouse_pos
from tkinter import Toplevel, Label


class ToolTip:
    def __init__(self, widget, id, lang):
        self.tipwindow = None
        self.widget = widget
        self.x = self.y = 0
        self.lang = lang
        self.id = id

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        mouse_x, mouse_y = mouse_pos()
        if mouse_x <= 1700 and self.lang == "eng" and self.id == 0:
            x = mouse_x + 14
        elif mouse_x <= 1600 and self.lang == "rus" and self.id == 0:
            x = mouse_x + 14
        elif mouse_x > 1700 and self.lang == "eng" and self.id == 0:
            x = mouse_x - 148
        elif mouse_x > 1600 and self.lang == "rus" and self.id == 0:
            x = mouse_x - 214
        elif mouse_x <= 1700 and 0 < self.id < 7:
            x = mouse_x + 14
        elif mouse_x > 1700 and self.lang == "rus" and self.id == 1:
            x = mouse_x - 165
        elif mouse_x > 1700 and self.lang == "rus" and self.id == 2:
            x = mouse_x - 140
        elif mouse_x > 1700 and self.lang == "rus" and self.id == 3:
            x = mouse_x - 150
        elif mouse_x > 1700 and self.lang == "rus" and 4 <= self.id <= 6:
            x = mouse_x - 200
        elif mouse_x > 1700 and self.lang == "eng" and (self.id == 1 or self.id == 4):
            x = mouse_x - 145
        elif mouse_x > 1700 and self.lang == "eng" and (self.id == 2 or self.id == 5):
            x = mouse_x - 150
        elif mouse_x > 1700 and self.lang == "eng" and (self.id == 3 or self.id == 6):
            x = mouse_x - 110

        y = mouse_y + 1

        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "10", "normal"),
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def create_tool_tip(widget, text, id, lang):
    toolTip = ToolTip(widget, id, lang)

    def enter(_):
        toolTip.showtip(text)

    def leave(_):
        toolTip.hidetip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
