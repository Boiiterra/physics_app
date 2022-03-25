from tkinter import Tk, Frame, Radiobutton, Button, Text, Label, Entry, TclError
from pyautogui import position as mouse_pos
from configparser import ConfigParser
from webbrowser import open_new_tab
from platform import system
from pyperclip import copy


__version__ = "0.1"
author = "TerraBoii"

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


        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (FLaunchPage, )

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")
        if lng_state == "ask" or current_language == "unknown":
            self.show_frame(FLaunchPage)
        elif lng_state == "keep":
            self.show_frame(FLaunchPage)

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


class FLaunchPage(Frame):  # This page launches when you need to choose language

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="black")
        self.controller = controller

        question_text = "\nChoose language:"

        question = Label(self, text=question_text, bg="black", fg="#00ff00", font=("Arial", 40))
        question.pack(side="top")

        hint_text = "Note: you can always change\nlanguage in settings menu"

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
                _hint_text = "Note: you can always change\nlanguage in settings menu"
            elif lang == "rus":
                _question_text = "\nВыберите язык:"
                _hint_text = "Подсказка: всегда можно\nизменить язык в настройках"
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
        # page = self.controller.get_page(RectanglesAPage)
        # page.set_lang_rectanglesaspage()
        # page = self.controller.get_page(RectanglesPPage)
        # page.set_lang_rectanglesppage()
        # page = self.controller.get_page(PerimetersPage)
        # page.set_lang_perimeterspage()
        # page = self.controller.get_page(SettingsPage)
        # page.set_lang_settingspage()
        # page = self.controller.get_page(SquaresAPage)
        # page.set_lang_squaresapage()
        # page = self.controller.get_page(SquaresPPage)
        # page.set_lang_squaresppage()
        # page = self.controller.get_page(GeometryPage)
        # page.set_lang_geometrypage()
        # page = self.controller.get_page(SubjectsPage)
        # page.set_lang_subjectspage()
        # page = self.controller.get_page(AreasPage)
        # page.set_lang_squarespage()
        # page = self.controller.get_page(MainPage)
        # page.set_lang_mainpage()

        if _from is None:  # We don't need to go to main page after switching language in settings
            # self.controller.show_frame(MainPage)
            print("oh crap")


if __name__ == "__main__":
    app = MainAppBody()
    app.mainloop()