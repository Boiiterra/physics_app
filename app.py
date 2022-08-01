from tkinter import Tk, Frame, Button, Text, Label, Entry, Toplevel, Menu, TclError
from pyautogui import position as mouse_pos
from tkinter.messagebox import showinfo
from configparser import ConfigParser
from webbrowser import open_new_tab
from PIL import Image, ImageTk
from platform import system
from pyperclip import copy 
from random import randint

from modules import create_tool_tip, NavigationToolbar, convert
from config import config_mpl_cmd, config_mpl_color

# const
AUTHOR = "TerraBoii"
APP_NAME = "Physics app"
WIDTH = 1000
HEIGHT = 600
ARIAL13 = ("Arial", 13)

# File reading section
parser = ConfigParser()
parser.read("data.txt")
# Parameters:
x_pos = parser.get('parameters', 'x')
y_pos = parser.get('parameters', 'y')
_width = parser.get('parameters', 'width')
_state = parser.get('parameters', 'zoomed')
_height = parser.get('parameters', 'height')
# Language
lng_state = parser.get("language", 'state')
current_language = parser.get("language", "language")
# Colors and theme
home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
num_active_fg = parser.get("colors", "num_btn_active_fore")
active_fg = parser.get("colors", "active_foreground")
current_theme = parser.get('theme', "current_theme")
home_btn_fg = parser.get("colors", "home_btn_fore")
main_btn_bg = parser.get("colors", "main_btn_back")
num_bg = parser.get("colors", "num_btn_back")
num_fg = parser.get("colors", "num_btn_fore")
fg = parser.get("colors", "foreground")
bg = parser.get("colors", "background")
# Info
a_u = parser.get("info", "auto_update")


class ToolTip(object):

    def __init__(self, widget, id):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0
        self.id = id

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        mouse_x, mouse_y = mouse_pos()
        if mouse_x <= 1700 and current_language == "eng" and self.id == 0:
            x = mouse_x + 14
            y = mouse_y + 1
        elif mouse_x <= 1600 and current_language == "rus" and self.id == 0:
            x = mouse_x + 14
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "eng" and self.id == 0:
            x = mouse_x - 148
            y = mouse_y + 1
        elif mouse_x > 1600 and current_language == "rus" and self.id == 0:
            x = mouse_x - 214
            y = mouse_y + 1
        elif mouse_x <= 1700 and 0 < self.id < 7:
            x = mouse_x + 14
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "rus" and self.id == 1:
            x = mouse_x - 165
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "rus" and self.id == 2:
            x = mouse_x - 140
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "rus" and self.id == 3:
            x = mouse_x - 150
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "rus" and  4 <= self.id <= 6:
            x = mouse_x - 200
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "eng" and (self.id == 1 or self.id == 4):
            x = mouse_x - 145
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "eng" and (self.id == 2 or self.id == 5):
            x = mouse_x - 150
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "eng" and (self.id == 3 or self.id == 6):
            x = mouse_x - 110
            y = mouse_y + 1
        
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify="left",
                      background="#ffffe0", relief="solid", borderwidth=1,
                      font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text, id):
    toolTip = ToolTip(widget, id)
    def enter(_):
        toolTip.showtip(text)
    def leave(_):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def set_theme():  # This function updates colors after theme changed
    global current_theme, bg, fg, active_fg, home_btn_active_fg, home_btn_fg, main_btn_bg, num_bg, num_fg, num_active_fg
    home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
    num_active_fg = parser.get("colors", "num_btn_active_fore")
    active_fg = parser.get("colors", "active_foreground")
    current_theme = parser.get('theme', "current_theme")
    home_btn_fg = parser.get("colors", "home_btn_fore")
    main_btn_bg = parser.get("colors", "main_btn_back")
    num_bg = parser.get("colors", "num_btn_back")
    num_fg = parser.get("colors", "num_btn_fore")
    fg = parser.get("colors", "foreground")
    bg = parser.get("colors", "background")


def a_u_state_set(state):
    global a_u, parser

    parser.read("data.txt")

    if state == 1:
        parser.set("info", "auto_update", "True")
    elif state == 0:
        parser.set("info", "auto_update", "False")

    with open("data.txt", "w") as configfile:
        parser.write(configfile)
    parser.get("info", "auto_update")


def change_language(language: str):  # This function changes language for whole application
    global parser, current_language, lng_state

    if language == "rus":
        parser.read('data.txt')
        parser.set("language", 'state', 'keep')
        parser.set('language', "language", 'rus')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        lng_state = parser.get('language', 'state')
        current_language = parser.get('language', 'language')
    elif language == "eng":
        parser.read('data.txt')
        parser.set("language", 'state', 'keep')
        parser.set('language', "language", 'eng')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        lng_state = parser.get('language', 'state')
        current_language = parser.get('language', 'language')
    elif language == "unknown":
        parser.read('data.txt')
        parser.set("language", 'state', 'ask')
        parser.set('language', "language", 'unknown')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        lng_state = parser.get('language', 'state')
        current_language = parser.get('language', 'language')


def dark_theme():  # This function changes colors and theme to dark and saves changes to file
    global parser
    parser.read("data.txt")
    parser.set("theme", "current_theme", "dark")
    parser.set("colors", "background", "#000000")
    parser.set("colors", "num_btn_back", "#0a0a0a")
    parser.set("colors", "home_btn_fore", "#474747")
    parser.set("colors", "active_foreground", "#5e5e5e")
    parser.set("colors", "home_bts_active_fore", "#333333")
    parser.set("colors", "num_btn_active_fore", "#5e5e5e")
    parser.set("colors", "main_btn_back", "#000000")
    parser.set("colors", "num_btn_fore", "#8c8c8c")
    parser.set("colors", "foreground", "#ffffff")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()


def light_theme():  # This function changes colors and theme to light and saves changes to file
    global parser
    parser.read("data.txt")
    parser.set('theme', "current_theme", "light")
    parser.set("colors", "num_btn_back", "#999999")
    parser.set("colors", "home_btn_fore", "#404040")
    parser.set("colors", "active_foreground", "#000000")
    parser.set("colors", "home_bts_active_fore", "#5e5e5e")
    parser.set("colors", "num_btn_active_fore", "#787878")
    parser.set("colors", "main_btn_back", "#292929")
    parser.set("colors", "num_btn_fore", "#4d4d4d")
    parser.set("colors", "foreground", "#000000")
    parser.set("colors", "background", "#bababa")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()


def save_window_parameters(_width_, _height_, _x_, _y_, _state_):
    # Saves given params to data.txt file
    global parser
    parser.read("data.txt")
    parser.set('parameters', 'height', _height_)
    parser.set('parameters', 'zoomed', _state_)
    parser.set('parameters', 'width', _width_)
    parser.set('parameters', 'x', _x_)
    parser.set('parameters', 'y', _y_)
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)


class MainAppBody(Tk):  # Main application with page logic

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(f"Physics app - {__version__}")
        try:
            self.iconbitmap("images//main_icon.ico")
        except TclError:
            print("Unable to find icon file")
        # Setting max and min sizes for the app
        self.minsize(width=800, height=600)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())

        # creating window:
        if current_language == "unknown" or lng_state == "ask" or system() == "Linux":
            middle_x = int((self.winfo_screenwidth() - 800) / 2)
            middle_y = int((self.winfo_screenheight() - 600) / 2)
            self.geometry(f"{800}x{600}+{middle_x}+{middle_y}")  # Middle pos on the screen
        else:
            self.geometry(f"{int(_width)}x{int(_height)}+{int(x_pos) - 8}+{(int(y_pos))-31}")  # (- 8) and (- 31) is important

        # Rewriting default delete method in order to save window parameters
        if system() == "Windows":
            self.protocol('WM_DELETE_WINDOW', self.delete_window)
            if _state == 'yes':
                self.state('zoomed')

        def donothing():
            print("Sorry I printed this!")

        def about():
            About(self)

        def full_reset():

            warning_box = Toplevel()
            warning_box.transient(self)
            warning_box.grab_set()
            warning_box.title('Warning - data reset')
            warning_box.geometry("317x102")
            warning_box.resizable(0, 0)
            if current_language == "eng":
                message = "Are you sure that you want to reset\napp's data?"
            elif current_language == "rus":
                message="Вы уверены, что хотите сбросить\nданные приложения?"

            mes_cont = Frame(warning_box)
            mes_cont.pack(side="top", expand=True, fill="x", anchor="w")
            mes_cont.rowconfigure(0, weight=1)
            mes_cont.columnconfigure(0, weight=1)
            mes_cont.columnconfigure(1, weight=1)

            photo = ImageTk.PhotoImage(Image.open('images/warning.png'))
            label = Label(mes_cont, image=photo)
            label.image = photo
            label.grid(row=0, column=0, padx=6)
            Label(mes_cont, text=message, font=("Times New Roman", 11, "bold")).grid(row=0, column=1, sticky="w")

            but_cont = Frame(warning_box)
            but_cont.pack(side="bottom", pady=7)
            but_cont.rowconfigure(0, weight=1)
            but_cont.columnconfigure(0, weight=1)
            but_cont.columnconfigure(1, weight=1)

            def run(do=None):
                if do is not None:
                    change_language("unknown")
                    light_theme()
                    self.destroy()
                else:
                    warning_box.destroy()

            Button(but_cont, text='Yes', command=lambda: run(True), width=7).grid(row=0, column=0, padx=10)
            Button(but_cont, text="No", command=run, width=7).grid(row=0, column=1, padx=10)

        def reset():
            if current_language == "eng":
                message = "Graph's data is reseted:\n- Pressure -> <None>.\n- Volume -> <None>.\n- Temperature -> <None>.\n- Gas -> <None>."
            elif current_language == "rus":
                message = "Данные графика были сброшены:\n- Давление -> <None>.\n- Объем -> <None>.\n- Температура -> <None>.\n- Газ -> <None>."
            showinfo("Graph reset", message)
            self.get_page(MainPage).data_reset()

        def settings():
            self.show_frame(Settings)

        self.menubar = Menu(self)
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New", command=donothing)
        file_menu.add_command(label="Open", command=donothing)
        file_menu.add_command(label="Save", command=donothing)
        file_menu.add_command(label="Save as...", command=donothing)
        file_menu.add_command(label="Reset", command=reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)
        edit_menu = Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="Reset app", command=full_reset)
        edit_menu.add_separator()
        edit_menu.add_command(label="Settings", command=settings)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="About...", command=about)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        if current_language != "unknown" or lng_state != "ask":
            self.add_menu()

        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.bind("<Control q>", lambda _: self.quit())

        self.frames = {}

        frame_collection = (FLaunchPage, MainPage, Settings)

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")
        if lng_state == "ask" or current_language == "unknown":
            self.show_frame(FLaunchPage)
        elif lng_state == "keep":
            self.show_frame(MainPage)

    def delete_window(self):  # saves parameters and then deletes window
        if self.wm_state() == "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), 'yes')
        elif self.wm_state() != "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), 'no')
        self.destroy()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    def add_menu(self):
        self.config(menu=self.menubar)


class About(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, bg=bg)

        self.transient(parent)
        self.grab_set()
        x = (self.winfo_screenwidth() - 313) / 2
        y = (self.winfo_screenheight() - 250) / 2
        self.geometry('{0}x{1}+{2}+{3}'.format(313, 250, int(x), int(y)))
        self.resizable(0, 0)
        self.title('Physics app')

        def call_link(_):
            open_new_tab('https://github.com/TerraBoii')

        def entered(_):
            a_text.config(font=("TkDefaultFont", 12, "underline"), cursor="hand2", fg="blue")
            toolTip.showtip(tip_txt)

        def left(_):
            a_text.config(font=("TkDefaultFont", 12), cursor="", fg=fg)
            toolTip.hidetip()

        a_u_t = None 

        if current_language == "eng":
            if a_u == "False":
                a_u_t = "off"
            elif a_u == "True":
                a_u_t = "on"

            title_t = "Physics app"
            txt3 = f"Auto update - {a_u_t}"
            txt5 = f"App's author - {author}"
            tip_txt = "Link to autor's profile"
            txt1 = f"App version - {__version__}"
            txt2 = f"App's theme - {current_theme}"
            txt4 = f"App's language - {current_language}"
        elif current_language == "rus":
            if a_u == "False":
                a_u_t = "выкл"
            elif a_u == "True":
                a_u_t = "вкл"

            txt4 = f"Язык приложения - {current_language}"
            txt2 = f"Тема приложения - {current_theme}"
            txt1 = f"Версия приложения - {__version__}"
            tip_txt = "Ссылка на профиль создателя"
            txt5 = f"Автор приложения - {author}"
            txt3 = f"Авто обновление - {a_u_t}"
            title_t = "Physics app"

        title = Label(self, text=title_t, font=("TkDefaultFont", 15), pady=5, bg=bg, fg=fg)
        title.pack()

        Button(self, text='OK', font=15, command=self.destroy, pady=10, width=7, highlightbackground=bg, 
               bg=num_bg, fg=fg, bd=0, activebackground=num_bg, activeforeground=active_fg).pack(side="bottom")
        Label(self, font=("Times New Roman", 1), bg=bg).pack()  # Placeholder
        Label(self, width=3, bg=bg).pack(side="left", fill="y")  # Placeholder

        Label(self, text=txt1, font=("TkDefaultFont", 12), anchor="w", bg=bg, fg=fg).pack(fill="x")
        Label(self, text=txt2, font=("TkDefaultFont", 12), anchor="w", bg=bg, fg=fg).pack(fill="x")
        Label(self, text=txt3, font=("TkDefaultFont", 12), anchor="w", bg=bg, fg=fg).pack(fill="x")
        Label(self, text=txt4, font=("TkDefaultFont", 12), anchor="w", bg=bg, fg=fg).pack(fill="x")
        a_text = Label(self, text=txt5, font=("TkDefaultFont", 12), anchor="w", bg=bg, fg=fg)
        a_text.pack(fill="x")
        toolTip = ToolTip(a_text, 0)
        a_text.bind("<Leave>", left)
        a_text.bind("<Enter>", entered)
        a_text.bind("<Button-1>", call_link)


class FLaunchPage(Frame):  # This page launches when you need to choose language

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="black")
        self.controller = controller

        question_text = "\nChoose language:"

        question = Label(self, text=question_text, bg="black", fg="#00ff00", font=("Arial", 40))
        question.pack(side="top")

        hint_text = "You can always change\nlanguage in settings menu"

        bottom_ = Label(self, bg="black", text=hint_text, font=("Arial", 30), fg="#008000")
        bottom_.pack(side="bottom")

        lang_btn_container = Label(self, bg="black", justify="center")
        lang_btn_container.pack(expand=True)

        lang_btn_container.rowconfigure(0, weight=1)
        lang_btn_container.rowconfigure(1, weight=1)
        lang_btn_container.columnconfigure(0, weight=1)

        self.russian = Button(lang_btn_container, text="Русский", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=("Arial", 30), bd=0, highlightbackground="black")
        self.russian.grid(row=0, column=0, sticky="nsew")

        self.english = Button(lang_btn_container, text="English", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=("Arial", 30), bd=0, highlightbackground="black")
        self.english.grid(row=1, column=0, sticky="nsew")

        def entered(_, btn, lang: str):
            btn.config(bg="#008000", activebackground="#00ff00")
            _question_text = _hint_text = ''
            if lang == "eng":
                _question_text = "\nChoose language:"
                _hint_text = "You can always change\nlanguage in settings menu"
            elif lang == "rus":
                _question_text = "\nВыберите язык:"
                _hint_text = "Язык можно\nизменить в настройках"
            question.config(text=_question_text)
            bottom_.config(text=_hint_text)

        def left(_, btn):
            btn.config(bg="black")

        self.english.bind("<Leave>", lambda _: left(_, btn=self.english))
        self.russian.bind("<Button-1>", lambda _: self.new_lang(_, lang="rus"))
        self.russian.bind("<Enter>", lambda _: entered(_, btn=self.russian, lang='rus'))
        self.english.bind("<Enter>", lambda _: entered(_, btn=self.english, lang='eng'))
        self.english.bind("<Button-1>", lambda _: self.new_lang(_, lang="eng"))
        self.russian.bind("<Leave>", lambda _: left(_, btn=self.russian))

        def font_resize_for_flaunchpage(width):
            if width.height <= 620:
                bottom_.config(font=("Arial", 30))
                question.config(font=('Arial', 40))
                self.russian.config(font=('Arial', 30))
                self.english.config(font=('Arial', 30))
            elif 620 < width.height <= 700:
                self.english.config(font=('Arial', 35))
                self.russian.config(font=('Arial', 35))
                question.config(font=('Arial', 45))
                bottom_.config(font=("Arial", 35))
            elif 700 < width.height <= 800:
                bottom_.config(font=("Arial", 40))
                question.config(font=('Arial', 50))
                self.russian.config(font=('Arial', 40))
                self.english.config(font=('Arial', 40))
            elif width.height > 800:
                self.english.config(font=('Arial', 45))
                self.russian.config(font=('Arial', 45))
                question.config(font=('Arial', 55))
                bottom_.config(font=("Arial", 45))

        self.bind("<Configure>", font_resize_for_flaunchpage)

    def new_lang(self, _, lang: str, _from = None):
        change_language(lang)
        self.controller.add_menu()
        page = self.controller.get_page(MainPage)
        page.set_main_lang()
        page = self.controller.get_page(Settings)
        page.set_lang_settings()

        if _from is None:  # We don't need to go to main page after switching language in settings
            self.controller.show_frame(MainPage)


class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.left_part = Frame(self, bg=bg)
        self.left_part.grid(row=0, column=0, sticky="nsew")

        self.right_part = Frame(self, bg=bg)
        self.right_part.grid(row=0, column=1, sticky="nsew")

        self.hint = ""
        self.p_tip = ""
        self.t_tip = ""
        self.v_tip = ""
        self.temp_pr = "None"
        self.volume_pr = "None"
        self.pressure_pr = "None"
        font_vi = ("TkDefaultFont", 13, "bold")

        self.pr_data_i = Label(self.left_part, font=font_vi, bg=bg, fg=fg)
        self.pr_data_i.pack(side="top", anchor="nw", pady=7, padx=45)

        self.cont_pr = Label(self.left_part, bg=bg)
        self.cont_pr.pack(side='left', anchor="nw", padx=30)
        self.cont_pr.rowconfigure(0, weight=1)
        self.cont_pr.rowconfigure(1, weight=1)
        self.cont_pr.columnconfigure(0, weight=1)
        self.cont_pr.columnconfigure(1, weight=1)
        self.cont_pr.columnconfigure(2, weight=1)

        self.new_data_i = Label(self.right_part, font=font_vi, bg=bg, fg=fg)
        self.new_data_i.pack(side="top", anchor="ne", pady=7, padx=45)

        self.cont_new = Label(self.right_part, bg=bg)
        self.cont_new.pack(side='right', anchor="ne", padx=30)
        self.cont_new.rowconfigure(0, weight=1)
        self.cont_new.rowconfigure(1, weight=1)
        self.cont_new.rowconfigure(2, weight=1)
        self.cont_new.columnconfigure(0, weight=1)
        self.cont_new.columnconfigure(1, weight=1)
        self.cont_new.columnconfigure(2, weight=1)

        # Info
        self.tp_v = Label(self.cont_pr, text="T", bg=bg, fg=fg, font=font_vi)
        self.tp_v.grid(row=0, column=0, sticky="nsew")
        self.vp_v = Label(self.cont_pr, text="V", bg=bg, fg=fg, font=font_vi)
        self.vp_v.grid(row=0, column=1, sticky="nsew")
        self.pp_v = Label(self.cont_pr, text="P", bg=bg, fg=fg, font=font_vi)
        self.pp_v.grid(row=0, column=2, sticky="nsew")

        self.tn_v = Label(self.cont_new, text="T", bg=bg, fg=fg, font=font_vi)
        self.tn_v.grid(row=0, column=0, sticky="nsew")
        self.vn_v = Label(self.cont_new, text="V", bg=bg, fg=fg, font=font_vi)
        self.vn_v.grid(row=0, column=1, sticky="nsew")
        self.pn_v = Label(self.cont_new, text="P", bg=bg, fg=fg, font=font_vi)
        self.pn_v.grid(row=0, column=2, sticky="nsew")

        # Previous data
        self.tp_e = Entry(self.cont_pr, width=10, font=font_vi, disabledbackground=num_bg, disabledforeground=fg,
                          bd=0, justify="center", highlightthickness=0)
        self.tp_e.grid(row=1, column=0, pady=2, padx=5)
        self.vp_e = Entry(self.cont_pr, width=10, font=font_vi, disabledbackground=num_bg, disabledforeground=fg,
                          bd=0, justify="center", highlightthickness=0)
        self.vp_e.grid(row=1, column=1, pady=2, padx=5)
        self.pp_e = Entry(self.cont_pr, width=10, font=font_vi, disabledbackground=num_bg, disabledforeground=fg,
                          bd=0, justify="center", highlightthickness=0)
        self.pp_e.grid(row=1, column=2, pady=2, padx=5)
        # New data
        self.tn_e = Entry(self.cont_new, width=10, font=font_vi, highlightbackground=num_bg, bg=num_bg, fg=fg, bd=0, justify="center")
        self.tn_e.grid(row=1, column=0, pady=2, padx=5)
        self.vn_e = Entry(self.cont_new, width=10, font=font_vi, highlightbackground=num_bg, bg=num_bg, fg=fg, bd=0, justify="center")
        self.vn_e.grid(row=1, column=1, pady=2, padx=5)
        self.pn_e = Entry(self.cont_new, width=10, font=font_vi, highlightbackground=num_bg, bg=num_bg, fg=fg, bd=0, justify="center")
        self.pn_e.grid(row=1, column=2, pady=2, padx=5)

        self.insert_prev_data()

        self.tp_e.bind("<Button-1>", lambda _: copy(self.temp_pr) if self.temp_pr != "None" else ...)
        self.vp_e.bind("<Button-1>", lambda _: copy(self.volume_pr) if self.volume_pr != "None" else ...)
        self.pp_e.bind("<Button-1>", lambda _: copy(self.pressure_pr) if self.pressure_pr != "None" else ...)

        self.set_main_lang()


    def insert_prev_data(self, clear=False):
        self.tp_e.config(state="normal")
        self.vp_e.config(state="normal")
        self.pp_e.config(state="normal")

        if clear: 
            self.tp_e.delete(0, "end")
            self.vp_e.delete(0, "end")
            self.pp_e.delete(0, "end")

        self.tp_e.insert("end", self.temp_pr)
        self.vp_e.insert("end", self.volume_pr)
        self.pp_e.insert("end", self.pressure_pr)

        if not clear:
            self.tn_e.insert("end", 0)
            self.vn_e.insert("end", 0)
            self.pn_e.insert("end", 0)

        self.tp_e.config(state="disabled")
        self.vp_e.config(state="disabled")
        self.pp_e.config(state="disabled")


    def data_reset(self):
        self.temp_pr = "None"
        self.volume_pr = "None"
        self.pressure_pr = "None"
        self.insert_prev_data(True)


    def set_main_lang(self):
        if current_language == "eng":
            self.hint = "Click to copy"
            self.p_tip = "Presure, Pascal"
            self.t_tip = "Temperature, Kelvin"
            self.v_tip = "Volume, cubic metre"
            self.new_data_i.config(text="New data")
            self.pr_data_i.config(text="Previous data")
        elif current_language == "rus":
            self.pr_data_i.config(text="Предыдущие данные")
            self.new_data_i.config(text="Новые данные")
            self.hint = "Нажми, чтобы скопировать"
            self.t_tip = "Температура, Кельвин"
            self.p_tip = "Давление, Паскалей"
            self.v_tip = "Объём, кубометров"

        CreateToolTip(self.tp_v, self.t_tip, 1)
        CreateToolTip(self.vp_v, self.v_tip, 2)
        CreateToolTip(self.pp_v, self.p_tip, 3)
        CreateToolTip(self.tn_v, self.t_tip, 1)
        CreateToolTip(self.vn_v, self.v_tip, 2)
        CreateToolTip(self.pn_v, self.p_tip, 3)

        CreateToolTip(self.tn_e, self.t_tip, 4)
        CreateToolTip(self.vn_e, self.v_tip, 5)
        CreateToolTip(self.pn_e, self.p_tip, 6)
        CreateToolTip(self.tp_e, f"{self.t_tip}\n{self.hint}", 4)
        CreateToolTip(self.vp_e, f"{self.v_tip}\n{self.hint}", 5)
        CreateToolTip(self.pp_e, f"{self.p_tip}\n{self.hint}", 6)


    def mainpage_theme(self):
        self.config(bg=bg)
        self.cont_pr.config(bg=bg)
        self.cont_new.config(bg=bg)
        self.left_part.config(bg=bg)
        self.right_part.config(bg=bg)
        self.tp_v.config(bg=bg, fg=fg)
        self.vp_v.config(bg=bg, fg=fg)
        self.pp_v.config(bg=bg, fg=fg)
        self.tn_v.config(bg=bg, fg=fg)
        self.vn_v.config(bg=bg, fg=fg)
        self.pn_v.config(bg=bg, fg=fg)
        self.pr_data_i.config(bg=bg, fg=fg)
        self.new_data_i.config(bg=bg, fg=fg)
        self.tn_e.config(bg=num_bg, fg=fg, highlightbackground=num_bg)
        self.vn_e.config(bg=num_bg, fg=fg, highlightbackground=num_bg)
        self.pn_e.config(bg=num_bg, fg=fg, highlightbackground=num_bg)
        self.tp_e.config(disabledbackground=num_bg, disabledforeground=fg)
        self.vp_e.config(disabledbackground=num_bg, disabledforeground=fg)
        self.pp_e.config(disabledbackground=num_bg, disabledforeground=fg)


class Settings(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        # Separator or placeholder
        self.place_h0 = Label(self, bg=bg, font=('Arial', 25))
        self.place_h0.pack()

        self.language_changers_container = Label(self, bg=bg)
        self.language_changers_container.pack(anchor='n')

        self.language_changers_container.rowconfigure(0, weight=1)
        self.language_changers_container.columnconfigure(0, weight=1)
        self.language_changers_container.columnconfigure(1, weight=1)
        self.language_changers_container.columnconfigure(2, weight=1)

        self.language_info = Button(self.language_changers_container, bg=bg, disabledforeground=fg,
                                    font=("Arial", 35), state='disabled', bd=0, highlightbackground=bg)
        self.language_info.grid(row=0, column=0, sticky="nsew")

        self.english_lang_btn = Button(self.language_changers_container, text="English", bg=num_bg, fg=num_fg,
                                       font=("Arial", 35), disabledforeground=num_bg, highlightbackground=num_bg,
                                       activeforeground=num_active_fg, activebackground=num_bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="eng"))
        self.english_lang_btn.grid(row=0, column=1, padx=5)

        self.russian_lang_btn = Button(self.language_changers_container, text="Русский", bg=bg, fg=fg,
                                       font=("Arial", 35), disabledforeground=bg, highlightbackground=bg,
                                       activeforeground=active_fg, activebackground=bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="rus"))
        self.russian_lang_btn.grid(row=0, column=2)

        # Separator or placeholder
        self.place_h1 = Label(self, bg=bg, font=('Arial', 30))
        self.place_h1.pack()

        self.themes_changers_container = Label(self, bg=bg)
        self.themes_changers_container.pack(anchor='n')

        self.themes_changers_container.rowconfigure(0, weight=1)
        self.themes_changers_container.columnconfigure(0, weight=1)
        self.themes_changers_container.columnconfigure(1, weight=1)
        self.themes_changers_container.columnconfigure(2, weight=1)
        self.themes_changers_container.columnconfigure(3, weight=1)
        
        self.theme_info = Label(self.themes_changers_container, bg=bg, fg=fg, font=("Arial", 35))
        self.theme_info.grid(row=0, column=0, sticky="nsew")

        self.dark_theme_btn = Button(self.themes_changers_container, bg=num_bg, fg=num_fg,
                                     font=("Arial", 35), command=self.change_theme_to_dark, bd=0, highlightbackground=num_bg,
                                     activeforeground=num_active_fg, activebackground=num_bg, disabledforeground=num_bg)
        self.dark_theme_btn.grid(row=0, column=1, sticky='nsew', padx=5)

        self.light_theme_btn = Button(self.themes_changers_container, bg=bg, fg=fg,
                                      font=("Arial", 35), highlightbackground=bg,
                                      activeforeground=active_fg, activebackground=bg, bd=0, disabledforeground=bg,
                                      command=self.change_theme_to_light)
        self.light_theme_btn.grid(row=0, column=3, sticky='nsew')

        self.place_h2 = Label(self, bg=bg, font=('Arial', 30))
        self.place_h2.pack()

        self.update_container = Label(self, bg=bg)
        self.update_container.pack(anchor="n")

        self.update_container.rowconfigure(0, weight=1)
        self.update_container.columnconfigure(0, weight=1)
        self.update_container.columnconfigure(1, weight=1)
        self.update_container.columnconfigure(2, weight=1)

        def a_u_state(new_state, button):
            a_u_state_set(new_state)
            if button == 0:
                self.a_update_on.config(state="disabled", cursor="")
                self.a_update_off.config(state="normal", cursor="hand2")
            elif button == 1:
                self.a_update_on.config(state="normal", cursor="hand2")
                self.a_update_off.config(state="disabled", cursor="")

        self.update_info = Label(self.update_container, bg=bg, fg=fg, font=("Arial", 35))
        self.update_info.grid(row=0, column=0, sticky="nsew")

        self.a_update_on = Button(self.update_container, text="On", bg=num_bg, fg=num_fg, highlightbackground=num_bg, bd=0,
                                  font=("Arial", 35), command=lambda: a_u_state(1, 0), activebackground=num_bg, activeforeground=num_active_fg,
                                  disabledforeground=num_bg)
        self.a_update_on.grid(row=0, column=1, sticky="nsew", padx=5)

        self.a_update_off = Button(self.update_container, text="Off", bg=bg, fg=fg, highlightbackground=bg, bd=0,
                                   font=("Arial", 35), command=lambda: a_u_state(0, 1), activebackground=bg, activeforeground=active_fg,
                                   disabledforeground=bg)
        self.a_update_off.grid(row=0, column=2, sticky="nsew") 

        if a_u == "True":
            self.a_update_on.config(state="disabled")
        elif a_u == "False":
            self.a_update_off.config(state="disabled")

        # Separator or placeholder
        self.place_h3 = Label(self, bg=bg, font=('Arial', 20))
        self.place_h3.pack()

        self.home_button = Button(self, bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                  activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                  disabledforeground=num_bg, command=lambda: self.controller.show_frame(MainPage),
                                  highlightbackground=num_bg)
        self.home_button.pack(fill='both', side='bottom', expand=True)

        # Checking for current theme"", cursor="arrow")

        self.bind("<Configure>", lambda params: self.font_changer(params.width))

        if current_theme == "light":
            self.light_theme_btn.config(state="disabled", cursor="")
            self.dark_theme_btn.config(state="normal", cursor="hand2")
        elif current_theme == "dark":
            self.light_theme_btn.config(state="normal", cursor="hand2")
            self.dark_theme_btn.config(state="disabled", cursor="")

        if a_u == "True":
            self.a_update_on.config(state="disabled", cursor="")
            self.a_update_off.config(state="normal", cursor="hand2")
        elif a_u == "False":
            self.a_update_on.config(state="normal", cursor="hand2")
            self.a_update_off.config(state="disabled", cursor="")

        self.set_lang_settings()

    def font_changer(self, width):
        """Changing font size based on window width"""
        if width <= 959:
            self.theme_info.config(font=('Arial', 42))
            self.home_button.config(font=('Arial', 45))
            self.dark_theme_btn.config(font=('Arial', 42))
            self.light_theme_btn.config(font=('Arial', 42))
        elif 959 < width <= 1160:
            self.light_theme_btn.config(font=('Arial', 50))
            self.dark_theme_btn.config(font=('Arial', 50))
            self.home_button.config(font=('Arial', 55))
            self.theme_info.config(font=('Arial', 50))
        elif width > 1160:
            self.theme_info.config(font=('Arial', 55))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Arial', 55))
            self.light_theme_btn.config(font=('Arial', 55))

    def language_changer(self, _lang_: str):
        """Changes language from setting page and fixes its font"""
        _page = self.controller.get_page(FLaunchPage)  # Getting access to FLaunchPage in oreder to use new_lang method
        _page.new_lang('', lang=_lang_, _from='')
        self.font_changer(self.winfo_width())  # Changing font size so everything will fit in the window

    def set_lang_settings(self):
        if current_language == "eng":
            self.russian_lang_btn.config(state='normal', cursor="hand2")
            self.english_lang_btn.config(state='disabled', cursor="")
            self.update_info.config(text='Auto update:')
            self.language_info.config(text='Language:')
            self.light_theme_btn.config(text='Light')
            self.dark_theme_btn.config(text='Dark')
            self.theme_info.config(text='Theme:')
            self.home_button.config(text='Home')
            self.a_update_off.config(text="Off")
            self.a_update_on.config(text="On")
        elif current_language == 'rus':
            self.a_update_on.config(text="Вкл")
            self.theme_info.config(text='Тема:')
            self.home_button.config(text='Назад')
            self.a_update_off.config(text="Выкл")
            self.language_info.config(text='Язык:')
            self.dark_theme_btn.config(text='Тёмная')
            self.light_theme_btn.config(text='Светлая')
            self.update_info.config(text="Авто обновление:")
            self.russian_lang_btn.config(state='disabled', cursor="")
            self.english_lang_btn.config(state='normal', cursor="hand2")
        self.font_changer(self.winfo_width())

    def settings_theme_update(self):
        self.config(bg=bg)
        self.place_h0.config(bg=bg)
        self.place_h1.config(bg=bg)
        self.place_h2.config(bg=bg)
        self.place_h3.config(bg=bg)
        self.update_container.config(bg=bg)
        self.theme_info.config(bg=bg, fg=fg)
        self.update_info.config(bg=bg, fg=fg)
        self.themes_changers_container.config(bg=bg)
        self.language_changers_container.config(bg=bg)
        self.language_info.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.a_update_off.config(bg=bg, fg=fg, highlightbackground=bg, activebackground=bg, activeforeground=active_fg,
                                 disabledforeground=bg)
        self.light_theme_btn.config(bg=bg, fg=fg, activeforeground=active_fg, activebackground=bg, disabledforeground=bg,
                                    highlightbackground=bg)
        self.russian_lang_btn.config(bg=bg, fg=fg, disabledforeground=bg, activeforeground=active_fg, activebackground=bg,
                                     highlightbackground=bg)
        self.a_update_on.config(bg=num_bg, fg=num_fg, highlightbackground=num_bg, activebackground=num_bg,
                                activeforeground=num_active_fg, disabledforeground=num_bg)
        self.dark_theme_btn.config(bg=num_bg, fg=num_fg, activeforeground=num_active_fg, activebackground=num_bg,
                                   disabledforeground=num_bg, highlightbackground=num_bg)
        self.english_lang_btn.config(bg=num_bg, fg=num_fg, disabledforeground=num_bg, activeforeground=num_active_fg,
                                     activebackground=num_bg, highlightbackground=num_bg)
        self.home_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg,
                                disabledforeground=num_bg, highlightbackground=num_bg)

    def pages_update(self):
        self.settings_theme_update()
        page = self.controller.get_page(MainPage)
        page.mainpage_theme()

    def change_theme_to_dark(self):
        self.light_theme_btn.config(state='normal', cursor="hand2")
        self.dark_theme_btn.config(state='disabled', cursor="")
        dark_theme()
        self.pages_update()

    def change_theme_to_light(self):
        self.dark_theme_btn.config(state='normal', cursor="hand2")
        self.light_theme_btn.config(state='disabled', cursor="")
        light_theme()
        self.pages_update()


if __name__ == "__main__":
    MainAppBody().mainloop()
