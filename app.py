from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pylab as plt
import numpy as np

from tkinter import Label, Entry, OptionMenu, StringVar, Tk, Frame, Button, Toplevel, Menu
from random import choice

from tkinter.messagebox import askyesno, showinfo
from webbrowser import open_new_tab
from PIL import ImageTk, Image
from decimal import Decimal

from modules import create_tool_tip, NavigationToolbar, tmpr_convert
from config import config_mpl_cmd, config_mpl_color

# const
AUTHOR = "TerraBoii"
APP_NAME = "Physics app"
WIDTH = 1000
HEIGHT = 600
ARIAL13 = ("Arial", 13)
DIGITS = 3 # * digits after dot: 3 -> 0.001;


# temp or session variables
# * data stores [[Process: int, Pressure: int | decimal, Volume: int | Decimal, Temperature: int | Decimal], ...]; Default/On-launch value -> [] (empty list)
# ! DO NOT STORE NUMPY NDARRAY IN DATA | DATA STORES ONLY THOSE VALUES THAT ARE ENTERED BY USER
data: list[list[int | Decimal]] = []
temperature: str = "k"  # * ONLY stores: "c" | "f" | "k" ; Default is "k" (c -> Celsius, f -> Fahrenheit, k -> Kelvin)
# * Only stores two of the "new_*" entries from main_page: needed in validator for iso processes
blocked_entries: list[Entry] = []
current_process: int = False  # * Chosen process by user -> isochoric -- 1, isotherm -- 2, isobaric -- 3, adiabatic -- 4 or polytrophic -- 5
current_graph: int = 0 # * Graph chosen by user -> P(v) -- 0 (default), P(T) -- 1, V(T) -- 2
degree_of_freedom: int = 3  # * It is number of degree of freedom for atoms in gas, default -> 3 (Monoatomic gas); diatomic -> 5; multi-atomic -> 6


# * Change only when finished adding new features or fixed something. 
# ! NO LETTERS IN VERSION STRING
# * Version examples: "0.1.0125", "2.1.2", etc.
# ! NO: "v0.1xd" | Reason: "I don't like it" - TerraBoii
version = "0.1"


ef = "#EFEFEF"
# Settings data ??? Will be reimplemented or not ???
# Theme
current_theme = "light"
# Global colors
bg = "#D9D9D9"
fg = "#000000"
dis_fg = "#848484" # Disabled foreground
# Menubar specific colors
menu_active_bg = "#E9E9E9"
# Buttons specific colors
btn_active_bg = "#CDCDCD"
btn_normal_bg = "#C0C0C0"
# Entries specific colors
entry_bg = "#ffffff"
entry_border = "#000000"
# mpl colors
axes_color = "#FFFFFF"
grid_color = "#b0b0b0"
text_color = "#000000"
# language
current_language = "rus"
# graph position
graph_pos: bool = True # * False -> right side; True -> left side (default)

config_mpl_cmd()
config_mpl_color(bg, axes_color, grid_color, text_color)


def change_theme(new_theme: str):
    global current_theme
    current_theme = new_theme


class WrongArgument(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MainAppBody(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(f"{APP_NAME} - {version}")  # App's title
        # TODO: Create icon for the app
        # self.iconbitmap("icon.ico")  # icon file
        self.geometry(
            f"{WIDTH}x{HEIGHT}+{(self.winfo_screenwidth() - WIDTH) // 2}+{(self.winfo_screenheight() - HEIGHT) // 2}"
        )  # MIddle of the screen
        self.resizable(0, 0)

        def destroy():
            match current_language:
                case "rus":
                    msg = "Вы уверены, что хотите выйти?\nYes -> Да        No -> Нет"
                case "eng":
                    msg = "Do you want to exit?"
            test = askyesno("Exit?", msg)
            if test:
                self.destroy()

        # Menu bar with help button
        menubar = Menu(self, tearoff=0, bd=1, bg=bg)
        # File submenu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: print("Export"))
        file_menu.add_command(label="Import", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: print("Import"))
        file_menu.add_command(label="Clear", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: print("Clear"))
        file_menu.add_separator(background=bg)
        file_menu.add_command(label="Quit", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=destroy)
        menubar.add_cascade(label="File", menu=file_menu, background=bg, foreground=fg, activebackground=menu_active_bg, activeforeground=fg)
        # Edit submenu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Settings", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: Settings(self))
        menubar.add_cascade(label="Edit", menu=edit_menu, background=bg, foreground=fg, activebackground=menu_active_bg, activeforeground=fg)

        menubar.add_command(label="\u22EE", activebackground=bg, background=bg, foreground=fg, activeforeground=fg)
        # Help submenu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: Help(self))
        help_menu.add_separator(background=bg)
        help_menu.add_command(label="About", background=bg, foreground=fg, activeforeground=fg, activebackground=menu_active_bg, command=lambda: About(self))
        menubar.add_cascade(label="Help", menu=help_menu, background=bg, foreground=fg, activebackground=menu_active_bg, activeforeground=fg)
        self.config(menu=menubar)

        # Place page into app
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (
            MainPage,
        )  # * ALL PAGES MUST BE LISTED HERE!!! (Frame classes). All listed pages are going to be constructed

        for frame in frame_collection:
            current_frame = frame(container, self)
            self.frames[frame] = current_frame
            current_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

        # Creating attributes (menu) to call from methods
        self.menubar = menubar
        self.file_menu = file_menu
        self.help_menu = help_menu
        self.edit_menu = edit_menu

        if current_language == "rus":
            self.set_lang_menu(True)

    def set_lang_menu(self, from_main_app_body: bool = None):
        # * If in `MainAppBody class` usage -> if current_language == "rus": self.set_lang_menu(True)
        # * If in `Settings` -> after current_language is changed, parent.set_lang_menu()
        # ! Anywhere else -> DO NOT USE
        match current_language, from_main_app_body:
            case "eng", None:
                self.menubar.entryconfig("Помощь...", label="Help")
                self.menubar.entryconfig("Изменить", label="Edit")
                self.menubar.entryconfig("Файл", label="File")
                self.file_menu.entryconfig("Импортировать", label="Import")
                self.file_menu.entryconfig("Экспортировать", label="Export")
                self.file_menu.entryconfig("Очистить", label="Clear")
                self.file_menu.entryconfig("Выйти", label="Quit")
                self.edit_menu.entryconfig("Настройки", label="Settings")
                self.help_menu.entryconfig("Помощь", label="Help")
                self.help_menu.entryconfig("О приложении", label="About")
            case "eng", _:
                raise WrongArgument(f'Got wrong arguments "{current_language}" and "{from_main_app_body}"')
            case "rus", None:
                raise WrongArgument(f'Got wrong arguments "{current_language}" and "{from_main_app_body}"')
            case "rus", _:
                self.menubar.entryconfig("Help", label="Помощь...")
                self.menubar.entryconfig("Edit", label="Изменить")
                self.menubar.entryconfig("File", label="Файл")
                self.file_menu.entryconfig("Import", label="Импортировать")
                self.file_menu.entryconfig("Export", label="Экспортировать")
                self.file_menu.entryconfig("Clear", label="Очистить")
                self.file_menu.entryconfig("Quit", label="Выйти")
                self.edit_menu.entryconfig("Settings", label="Настройки")
                self.help_menu.entryconfig("Help", label="Помощь")
                self.help_menu.entryconfig("About", label="О приложении")

    def show_frame(self, cont):
        """This is used to show any page (page MUST be listed in frame_collection)"""
        self.frames[cont].tkraise()

    def get_page(self, page_class):
        """Gets methods of the given page and its variables with "self." in front of them, ex.: self.variable_name)"""
        return self.frames[page_class]


class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Side for graph
        graph_cont = Frame(self, height=HEIGHT, width=(WIDTH // 2), bg=bg)
        graph_cont.grid(row=0, column=0, sticky="nsew")
        # graph_cont.pack(side="left", expand=True, fill="both")

        def change_graph_to(new_graph: int):
            global current_graph
            match new_graph:
                case 0: # P(V)
                    graph_pv.config(state="disabled", cursor="")
                    graph_pt.config(state="normal", cursor="hand2")
                    graph_vt.config(state="normal", cursor="hand2")

                    ax.clear()
                    if data:
                        if len(data) == 1:
                            ax.plot(data[0][2], data[0][1], "bo")
                    ax.set_title("P(V)")
                    ax.set_ylabel("P")
                    ax.set_xlabel("V")
                    canvas.draw()

                    current_graph = new_graph
                case 1: # P(T)
                    graph_pv.config(state="normal", cursor="hand2")
                    graph_pt.config(state="disabled", cursor="")
                    graph_vt.config(state="normal", cursor="hand2")

                    ax.clear()
                    if data:
                        if len(data) == 1:
                            ax.plot(data[0][3], data[0][1], "bo")
                    ax.set_title("P(T)")
                    ax.set_ylabel("P")
                    ax.set_xlabel("T")
                    canvas.draw()

                    current_graph = new_graph
                case 2: # V(T)
                    graph_pv.config(state="normal", cursor="hand2")
                    graph_pt.config(state="normal", cursor="hand2")
                    graph_vt.config(state="disabled", cursor="")

                    ax.clear()
                    if data:
                        if len(data) == 1:
                            ax.plot(data[0][3], data[0][2], "bo")
                    ax.set_title("V(T)")
                    ax.set_ylabel("V")
                    ax.set_xlabel("T")
                    canvas.draw()

                    current_graph = new_graph
                case _:
                    if isinstance(new_graph, int):
                        raise TypeError(f"Expected int but got {type(new_graph)}")
                    else:
                        raise ValueError(f'Unsupported value "{new_graph}"')

        # Container with buttons that change graphs
        graph_changer = Frame(graph_cont, bg=bg)
        graph_changer.pack(pady=(4, 0))

        gc_info = Label(
            graph_changer, font=ARIAL13, bg=bg, fg=fg
        )
        gc_info.grid(row=0, column=0, columnspan=3)

        graph_pv = Button(
            graph_changer,
            activeforeground=fg,
            background=btn_normal_bg,
            command=lambda: change_graph_to(0),
            activebackground=btn_active_bg,
            disabledforeground=dis_fg,
            font=ARIAL13,
            text="P(V)",
            padx=10,
            fg=fg,
            bd=0,
        )
        graph_pv.grid(row=1, column=0, padx=(0, 20), pady=5)

        graph_pt = Button(
            graph_changer,
            activeforeground=fg,
            background=btn_normal_bg,
            command=lambda: change_graph_to(1),
            activebackground=btn_active_bg,
            disabledforeground=dis_fg,
            font=ARIAL13,
            text="P(T)",
            padx=10,
            fg=fg,
            bd=0,
        )
        graph_pt.grid(row=1, column=1, padx=20, pady=5)

        graph_vt = Button(
            graph_changer,
            activeforeground=fg,
            background=btn_normal_bg,
            command=lambda: change_graph_to(2),
            activebackground=btn_active_bg,
            disabledforeground=dis_fg,
            font=ARIAL13,
            text="V(T)",
            padx=10,
            fg=fg,
            bd=0,
        )
        graph_vt.grid(row=1, column=2, padx=(20, 0), pady=5)

        fig = plt.Figure(figsize=(5, 5), dpi=100)
        t = np.arange(0, ((2 * np.pi) + 0.001), 0.001)
        ax = fig.add_subplot(111)
        ax.plot(t, t)

        canvas = FigureCanvasTkAgg(fig, master=graph_cont)
        # canvas.draw()
        change_graph_to(0) # * Default graph -> 0

        toolbar = NavigationToolbar(canvas, graph_cont, pack_toolbar=False)
        toolbar.update()

        canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.pack(side="bottom", fill="x", expand=False, padx=(5, 0))
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Side for data
        data_cont = Frame(self, height=HEIGHT, width=(WIDTH // 2) ,bg=bg)
        data_cont.grid(row=0, column=1, sticky="snew")
        # data_cont.pack(side="right")

        # Previous data (READ ONLY)
        prev_data = Frame(data_cont, bg=bg)
        prev_data.pack(pady=(4, 0))

        p_info = Label(prev_data, font=ARIAL13 + ("underline",), bg=bg, fg=fg)
        p_info.grid(row=0, column=0, columnspan=3)

        # New data (CAN BE MODIFIED)
        new_data = Frame(data_cont, bg=bg)
        new_data.pack(pady=(4, 0))

        n_info = Label(new_data, font=ARIAL13 + ("underline",), bg=bg, fg=fg)
        n_info.grid(row=0, column=0, columnspan=3)

        validator = (
            parent.register(self.__validator),
            "%W",
            "%P",
        )  # widget name, value

        # Temperature (t)
        # Previous
        big_t_pd = Label(prev_data, text="T", font=ARIAL13, bg=bg, fg=fg)
        big_t_pd.grid(row=1, column=0, sticky="nsew")
        prev_t = Entry(
            prev_data,
            width=10,
            cursor="",
            justify="center",
            disabledbackground=bg,
            highlightbackground=entry_border,
            disabledforeground=fg,
            state="disabled",
            font=ARIAL13,
            bd=0,
        )
        prev_t.grid(row=2, column=0, pady=2, padx=5)
        # New
        big_t_nd = Label(new_data, text="T", font=ARIAL13, bg=bg, fg=fg)
        big_t_nd.grid(row=1, column=0, sticky="nsew")
        new_t = Entry(
            new_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        new_t.grid(row=2, column=0, pady=2, padx=5)

        # Volume (v)
        # Previous
        big_v_pd = Label(prev_data, text="V", font=ARIAL13, bg=bg, fg=fg)
        big_v_pd.grid(row=1, column=1, sticky="nsew")
        prev_v = Entry(
            prev_data,
            width=10,
            cursor="",
            justify="center",
            disabledbackground=bg,
            highlightbackground=entry_border,
            disabledforeground=fg,
            state="disabled",
            font=ARIAL13,
            bd=0,
        )
        prev_v.grid(row=2, column=1, pady=2, padx=5)
        # New
        big_v_nd = Label(new_data, text="V", font=ARIAL13, bg=bg, fg=fg)
        big_v_nd.grid(row=1, column=1, sticky="nsew")
        new_v = Entry(
            new_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        new_v.grid(row=2, column=1, pady=2, padx=5)

        # Pressure (p)
        # Previous
        big_p_pd = Label(prev_data, text="P", font=ARIAL13, bg=bg, fg=fg)
        big_p_pd.grid(row=1, column=2, sticky="nsew")
        prev_p = Entry(
            prev_data,
            width=10,
            cursor="",
            justify="center",
            disabledbackground=bg,
            highlightbackground=entry_border,
            disabledforeground=fg,
            state="disabled",
            font=ARIAL13,
            bd=0,
        )
        prev_p.grid(row=2, column=2, pady=2, padx=5)
        # New
        big_p_nd = Label(new_data, text="P", font=ARIAL13, bg=bg, fg=fg)
        big_p_nd.grid(row=1, column=2, sticky="nsew")
        new_p = Entry(
            new_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        new_p.grid(row=2, column=2, pady=2, padx=5)

        def decrease():
            global degree_of_freedom

            if gas_atoms.cget("text") == "3+":
                increase_btn.config(state="normal", bg=btn_normal_bg)
                gas_atoms.config(text="3")

            gas_atoms.config(text=f"{int(gas_atoms.cget('text'))-1}")

            match int(gas_atoms.cget("text")):
                case 1:
                    degree_of_freedom = 3
                case 2:
                    degree_of_freedom = 5
                case 3:
                    degree_of_freedom = 6

            if gas_atoms.cget("text") == "1":
                decrease_btn.config(state="disabled", bg=bg)

        def increase():
            global degree_of_freedom

            if gas_atoms.cget("text") == "1":
                decrease_btn.config(state="normal", bg=btn_normal_bg)
            gas_atoms.config(text=f"{int(gas_atoms.cget('text'))+1}")

            match int(gas_atoms.cget("text")):
                case 1:
                    degree_of_freedom = 3
                case 2:
                    degree_of_freedom = 5
                case 3:
                    degree_of_freedom = 6

            if gas_atoms.cget("text") == "3":
                increase_btn.config(state="disabled", bg=bg)
                gas_atoms.config(text="3+")

        gas_cont = Frame(data_cont, bg=bg)
        gas_cont.pack(pady=(5, 0))

        gas_info = Label(gas_cont, font=ARIAL13, fg=fg, bg=bg)
        gas_info.grid(row=0, column=0)

        minus = ImageTk.PhotoImage(Image.open("images/remove.png").resize((25, 25)))
        decrease_btn = Button(
            gas_cont,
            image=minus,
            height=25,
            bd=0,
            bg=bg,
            activebackground=btn_active_bg,
            command=decrease,
            cursor="hand2",
            state="disabled",
        )
        decrease_btn.image = minus
        decrease_btn.grid(row=0, column=1)

        gas_atoms = Label(
            gas_cont, font=ARIAL13, justify="center", width=4, fg=fg, bg=bg, text="1"
        )
        gas_atoms.grid(row=0, column=2)

        plus = ImageTk.PhotoImage(Image.open("images/add.png").resize((25, 25)))
        increase_btn = Button(
            gas_cont,
            image=plus,
            height=25,
            bd=0,
            bg=btn_normal_bg,
            activebackground=btn_active_bg,
            command=increase,
            cursor="hand2",
        )
        increase_btn.image = plus
        increase_btn.grid(row=0, column=3)

        def set_process(name: str):
            global current_process
            if not current_process:
                check_data_btn.config(state="normal", cursor="hand2")
                add_dot_btn.config(state="normal", cursor="hand2")
                refresh_graph_bnt.config(state='normal', cursor="hand2")
            match name:
                case "Isochoric" | "Изохорный":
                    # isochoric
                    self.process_var.set(name)
                    # Button statuses
                    match current_language:
                        case "eng":
                            chosen_process['menu'].entryconfigure("Isochoric", state="disabled")
                            chosen_process['menu'].entryconfigure("Isotherm", state="normal")
                            chosen_process['menu'].entryconfigure("Isobaric", state="normal")
                            chosen_process['menu'].entryconfigure("Adiabatic", state="normal")
                            chosen_process['menu'].entryconfigure("Polytrophic", state="normal")
                        case "rus":
                            chosen_process['menu'].entryconfigure("Изохорный", state="disabled")
                            chosen_process['menu'].entryconfigure("Изотермический", state="normal")
                            chosen_process['menu'].entryconfigure("Изобарный", state="normal")
                            chosen_process['menu'].entryconfigure("Адиабатный", state="normal")
                            chosen_process['menu'].entryconfigure("Политропный", state="normal")
                    # Entries statuses
                    new_t.config(state="normal", cursor="xterm")
                    new_v.config(state="disabled")
                    new_p.config(state="normal", cursor="xterm")
                    current_process = 1
                case "Isotherm" | "Изотермический":
                    # isotherm
                    self.process_var.set(name)
                    # Button statuses
                    match current_language:
                        case "eng":
                            chosen_process['menu'].entryconfigure("Isochoric", state="normal")
                            chosen_process['menu'].entryconfigure("Isotherm", state="disabled")
                            chosen_process['menu'].entryconfigure("Isobaric", state="normal")
                            chosen_process['menu'].entryconfigure("Adiabatic", state="normal")
                            chosen_process['menu'].entryconfigure("Polytrophic", state="normal")
                        case "rus":
                            chosen_process['menu'].entryconfigure("Изохорный", state="normal")
                            chosen_process['menu'].entryconfigure("Изотермический", state="disabled")
                            chosen_process['menu'].entryconfigure("Изобарный", state="normal")
                            chosen_process['menu'].entryconfigure("Адиабатный", state="normal")
                            chosen_process['menu'].entryconfigure("Политропный", state="normal")
                    # Entries statuses
                    new_t.config(state="disabled")
                    new_v.config(state="normal", cursor="xterm")
                    new_p.config(state="normal", cursor="xterm")
                    current_process = 2
                case "Isobaric" | "Изобарный":
                    # isobaric
                    self.process_var.set(name)
                    # Button statuses
                    match current_language:
                        case "eng":
                            chosen_process['menu'].entryconfigure("Isochoric", state="normal")
                            chosen_process['menu'].entryconfigure("Isotherm", state="normal")
                            chosen_process['menu'].entryconfigure("Isobaric", state="disabled")
                            chosen_process['menu'].entryconfigure("Adiabatic", state="normal")
                            chosen_process['menu'].entryconfigure("Polytrophic", state="normal")
                        case "rus":
                            chosen_process['menu'].entryconfigure("Изохорный", state="normal")
                            chosen_process['menu'].entryconfigure("Изотермический", state="normal")
                            chosen_process['menu'].entryconfigure("Изобарный", state="disabled")
                            chosen_process['menu'].entryconfigure("Адиабатный", state="normal")
                            chosen_process['menu'].entryconfigure("Политропный", state="normal")
                    # Entries statuses
                    new_t.config(state="normal", cursor="xterm")
                    new_v.config(state="normal", cursor="xterm")
                    new_p.config(state="disabled")
                    current_process = 3
                case "Adiabatic" | "Адиабатный":
                    # adiabatic
                    self.process_var.set(name)
                    # Button statuses
                    match current_language:
                        case "eng":
                            chosen_process['menu'].entryconfigure("Isochoric", state="normal")
                            chosen_process['menu'].entryconfigure("Isotherm", state="normal")
                            chosen_process['menu'].entryconfigure("Isobaric", state="normal")
                            chosen_process['menu'].entryconfigure("Adiabatic", state="disabled")
                            chosen_process['menu'].entryconfigure("Polytrophic", state="normal")
                        case "rus":
                            chosen_process['menu'].entryconfigure("Изохорный", state="normal")
                            chosen_process['menu'].entryconfigure("Изотермический", state="normal")
                            chosen_process['menu'].entryconfigure("Изобарный", state="normal")
                            chosen_process['menu'].entryconfigure("Адиабатный", state="disabled")
                            chosen_process['menu'].entryconfigure("Политропный", state="normal")
                    # Entries statuses
                    new_t.config(state="normal", cursor="xterm")
                    new_v.config(state="normal", cursor="xterm")
                    new_p.config(state="normal", cursor="xterm")
                    current_process = 4
                case "Polytrophic" | "Политропный":
                    # polytrophic
                    self.process_var.set(name)
                    # Button statuses
                    match current_language:
                        case "eng":
                            chosen_process['menu'].entryconfigure("Isochoric", state="normal")
                            chosen_process['menu'].entryconfigure("Isotherm", state="normal")
                            chosen_process['menu'].entryconfigure("Isobaric", state="normal")
                            chosen_process['menu'].entryconfigure("Adiabatic", state="normal")
                            chosen_process['menu'].entryconfigure("Polytrophic", state="disabled")
                        case "rus":
                            chosen_process['menu'].entryconfigure("Изохорный", state="normal")
                            chosen_process['menu'].entryconfigure("Изотермический", state="normal")
                            chosen_process['menu'].entryconfigure("Изобарный", state="normal")
                            chosen_process['menu'].entryconfigure("Адиабатный", state="normal")
                            chosen_process['menu'].entryconfigure("Политропный", state="disabled")
                    # Entries statuses
                    new_t.config(state="normal", cursor="xterm")
                    new_v.config(state="normal", cursor="xterm")
                    new_p.config(state="normal", cursor="xterm")
                    current_process = 5
                case _:
                    if isinstance(name, str):
                        raise ValueError(f'Got unsupported value -> "{name}".')
                    else:
                        raise TypeError(f'Expected <str> but got "{type(name)}".')

        process_cont = Frame(data_cont, bg=bg)
        process_cont.pack(pady=(5, 0))

        process_info = Label(process_cont, font=ARIAL13 + ("underline",), bg=bg, fg=fg)
        process_info.grid(row=0, column=0, padx=(0, 10))

        self.process_var = StringVar()

        match current_language:
            case "eng":
                processes = ["Isochoric", "Isotherm", "Isobaric", "Adiabatic", "Polytrophic"]
            case "rus":
                processes = ["Изохорный", "Изотермический", "Изобарный", "Адиабатный", "Политропный"]
            case _:
                raise ValueError(f"Unsupported language '{current_language}'")

        chosen_process = OptionMenu(process_cont, self.process_var, *processes, command=set_process)
        chosen_process.config(font=ARIAL13, fg=fg, bg=btn_normal_bg, activebackground=btn_active_bg, bd=0, justify="center", indicatoron=False, state="disabled")
        chosen_process["menu"].config(font=ARIAL13, fg=fg, bg=btn_normal_bg, activebackground=btn_active_bg, bd=0)
        chosen_process.grid(row=0, column=1, sticky="nsew")

        # Functional buttons

        func_btn_cont = Frame(data_cont, bg=bg)
        func_btn_cont.pack(pady=(35, 0))

        def change_prev(pressure: str = None, volume: str = None, temperature: str = None, insert: bool = False):
            """To clear prev_* no params needed"""
            prev_p["state"] = "normal"
            prev_v["state"] = "normal"
            prev_t["state"] = "normal"
            prev_p.delete(0, "end")
            prev_v.delete(0, "end")
            prev_t.delete(0, "end")
            if insert:
                prev_p.insert(0, pressure)
                prev_v.insert(0, volume)
                prev_t.insert(0, temperature)
            prev_p["state"] = "disabled"
            prev_v["state"] = "disabled"
            prev_t["state"] = "disabled"

        def reset_page():
            global current_process
            current_process = False

            match current_language:
                case "eng":
                    chosen_process['menu'].entryconfigure("Isochoric", state="normal")
                    chosen_process['menu'].entryconfigure("Isotherm", state="normal")
                    chosen_process['menu'].entryconfigure("Isobaric", state="normal")
                    chosen_process['menu'].entryconfigure("Adiabatic", state="normal")
                    chosen_process['menu'].entryconfigure("Polytrophic", state="normal")
                    self.process_var.set("not chosen")
                case "rus":
                    chosen_process['menu'].entryconfigure("Изохорный", state="normal")
                    chosen_process['menu'].entryconfigure("Изотермический", state="normal")
                    chosen_process['menu'].entryconfigure("Изобарный", state="normal")
                    chosen_process['menu'].entryconfigure("Адиабатный", state="normal")
                    chosen_process['menu'].entryconfigure("Политропный", state="normal")
                    self.process_var.set("не выбран")
            chosen_process["state"] = "disabled"

            new_t.config(state="disabled", cursor="")
            new_v.config(state="disabled", cursor="")
            new_p.config(state="disabled", cursor="")
            begin_btn.config(state="normal", cursor="hand2")
            check_data_btn.config(state="disabled", cursor="")
            add_dot_btn.config(state="disabled", cursor="")
            refresh_graph_bnt.config(state='disabled', cursor="")
            del_prev_btn.config(state="disabled", cursor="")
            clear_graph_btn.config(state="disabled", cursor="")

        def check_data():
            if blocked_entries:
                print("data is here")
            else:
                match current_language:
                    case "rus":
                        msg = "Перед проверкой данных необходимо их ввести."
                    case "eng":
                        msg = "Befoure checking data you need to enter it."
                showinfo("Info -- no data", msg)

        def add_dot(first: bool = False, _data: list[str] = None):
            if blocked_entries:
                print("data is here")
            elif first:
                data.append([None, *_data])
                chosen_process["state"] = "normal"
                refresh_graph()
                change_prev(*_data, True)
            else:
                match current_language:
                    case "rus":
                        msg = "Для добавления новой точки необходимо ввести данные."
                    case "eng":
                        msg = "For adding new dot you need to enter some data."
                showinfo("Info -- no data", msg)

        def refresh_graph(is_empty: bool = False):
            if is_empty:
                ax.clear()
                match current_graph:
                    case 0:
                        ax.set_title("P(V)")
                        ax.set_ylabel("P")
                        ax.set_xlabel("V")
                    case 1:
                        ax.set_title("P(T)")
                        ax.set_ylabel("P")
                        ax.set_xlabel("T")
                    case 2:
                        ax.set_title("V(T)")
                        ax.set_ylabel("V")
                        ax.set_xlabel("T")
                canvas.draw()
            elif data:
                ax.clear()
                match current_graph:
                    case 0:
                        ax.set_title("P(V)")
                        ax.set_ylabel("P")
                        ax.set_xlabel("V")
                        if len(data) == 1:
                            ax.plot(data[0][2], data[0][1], "bo")
                    case 1:
                        ax.set_title("P(T)")
                        ax.set_ylabel("P")
                        ax.set_xlabel("T")
                        if len(data) == 1:
                            ax.plot(data[0][3], data[0][1], "bo")
                    case 2:
                        ax.set_title("V(T)")
                        ax.set_ylabel("V")
                        ax.set_xlabel("T")
                        if len(data) == 1:
                            ax.plot(data[0][3], data[0][2], "bo")
                canvas.draw()
            else:
                match current_language:
                    case "rus":
                        msg =  "Перед перерисовкой графика необходимо ввести данные."
                    case "eng":
                        msg = "Before refreshing graph you need to enter data."
                showinfo("Info -- no data", msg)

        def del_prev_dot():
            if data:
                if len(data) == 1:
                    reset_page()
                data.pop(-1)
                refresh_graph(not data)
                change_prev()
                match current_language:
                    case "rus":
                        msg = "Предыдущая точка удалена."
                    case "eng":
                        msg = "Previus dot is removed."
                showinfo("Info -- dot removed", msg)
            else:
                match current_language:
                    case "rus":
                        msg = "До удаления предыдущей точки необходимо ввести данные."
                    case "eng":
                        msg = "Before removing previus dot you need to enter data."
                showinfo("Info -- no data", msg)

        def clear_graph():
            global data
            if data:
                reset_page()
                data = []
                refresh_graph(not data)
                change_prev()
                match current_language:
                    case "rus":
                        msg = "График и все точки удалёны."
                    case "eng":
                        msg = "Graph and all dots are deleted."
                showinfo("Info -- graph deleted", msg)
            else:
                match current_language:
                    case "rus":
                        msg = "До очистки графика необходимо ввести данные."
                    case "eng":
                        msg = "Before clearing graph you need to enter data."
                showinfo("Info -- no data", msg)

        begin_btn = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, fg=fg, bg=btn_normal_bg, activebackground=btn_active_bg, activeforeground=fg, disabledforeground=dis_fg, cursor="hand2", command=lambda: NewDotPrompt(self))
        begin_btn.pack()

        check_data_btn = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, disabledforeground=dis_fg, cursor="hand2", command=check_data)
        check_data_btn.pack(pady=(10, 0))

        add_dot_btn = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, disabledforeground=dis_fg, cursor="hand2", command=add_dot)
        add_dot_btn.pack(pady=(15, 0))

        refresh_graph_bnt = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, disabledforeground=dis_fg, cursor="hand2", command=refresh_graph)
        refresh_graph_bnt.pack(pady=(5, 0))

        del_prev_btn = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, disabledforeground=dis_fg, cursor="hand2", command=del_prev_dot)
        del_prev_btn.pack(pady=(20, 0))

        clear_graph_btn = Button(func_btn_cont, bd=0, font=ARIAL13, width=30, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, disabledforeground=dis_fg, cursor="hand2", command=clear_graph)
        clear_graph_btn.pack(pady=(5, 0))

        match current_process:
            case False:
                new_t.config(state="disabled", cursor="")
                new_v.config(state="disabled", cursor="")
                new_p.config(state="disabled", cursor="")
                check_data_btn.config(state="disabled", cursor="")
                add_dot_btn.config(state="disabled", cursor="")
                refresh_graph_bnt.config(state='disabled', cursor="")
                del_prev_btn.config(state="disabled", cursor="")
                clear_graph_btn.config(state="disabled", cursor="")
            case _:
                raise ValueError("There is NO default process!")

        # Variables -> attributes, to call from methods and other pages, classes
        # Containers
        self.graph_cont = graph_cont
        self.data_cont = data_cont
        self.prev_data = prev_data
        self.new_data = new_data
        self.gas_cont = gas_cont
        self.process_cont = process_cont
        self.func_btn_cont = func_btn_cont
        # Info labels
        self.gc_info = gc_info
        self.p_info = p_info
        self.n_info = n_info
        self.gas_info = gas_info
        self.process_info = process_info
        # Big letters
        self.big_t_nd = big_t_nd
        self.big_t_pd = big_t_pd
        self.big_v_nd = big_v_nd
        self.big_v_pd = big_v_pd
        self.big_p_nd = big_p_nd
        self.big_p_pd = big_p_pd
        # Entries
        self.prev_t = prev_t
        self.new_t = new_t
        self.prev_v = prev_v
        self.new_v = new_v
        self.prev_p = prev_p
        self.new_p = new_p
        self.gas_atoms = gas_atoms
        # Process
        self.chosen_process = chosen_process
        # Butttons
        self.begin_btn = begin_btn
        self.check_data_btn = check_data_btn
        self.add_dot_btn = add_dot_btn
        self.refresh_graph_bnt = refresh_graph_bnt
        self.del_prev_btn = del_prev_btn
        self.clear_graph_btn = clear_graph_btn
        # Used in NewDotPrompt
        self.add_dot = add_dot
        # Used in set_lang_mainpage (Only when lang is changed from settings) 
        self.set_process = set_process

        self.set_lang_mainpage()  # Setting text based on language

    def set_lang_mainpage(self, changed: bool = False):
        if current_language == "eng":
            self.p_tip = "Presure, Pascal"
            self.process_var.set("not chosen")
            self.t_tip = "Temperature, Kelvin"
            self.v_tip = "Volume, cubic metre"
            self.n_info.config(text="New data:")
            self.p_info.config(text="Previous data:")
            self.process_info.config(text="Process:")
            self.add_dot_btn.config(text="Add new dot")
            self.begin_btn.config(text="Add first dot")
            self.gc_info.config(text="Change graph to:")
            self.check_data_btn.config(text="Check data")
            self.clear_graph_btn.config(text="Clear graph")
            self.refresh_graph_bnt.config(text="Refresh graph")
            self.gas_info.config(text="Amount of atoms in gas: ")
            self.del_prev_btn.config(text="Delete previous parameter")
            if changed:
                self.chosen_process['menu'].delete(0, 'end')
                self.chosen_process['menu'].add_command(label="Isochoric", command=lambda: self.set_process("Isochoric"))
                self.chosen_process['menu'].add_command(label="Isotherm", command=lambda: self.set_process("Isotherm"))
                self.chosen_process['menu'].add_command(label="Isobaric", command=lambda: self.set_process("Isobaric"))
                self.chosen_process['menu'].add_command(label="Adiabatic", command=lambda: self.set_process("Adiabatic"))
                self.chosen_process['menu'].add_command(label="Polytrophic", command=lambda: self.set_process("Polytrophic"))
        elif current_language == "rus":
            self.refresh_graph_bnt.config(text="Перерисовать график")
            self.del_prev_btn.config(text="Удалить предыдущую точку")
            self.gas_info.config(text="Количество атомов в газе: ")
            self.begin_btn.config(text="Добавить первую точку")
            self.check_data_btn.config(text="Проверить данные")
            self.clear_graph_btn.config(text="Очистить график")
            self.gc_info.config(text="Изменить график на:")
            self.add_dot_btn.config(text="Добавить точку")
            self.p_info.config(text="Предыдущие данные:")
            self.process_info.config(text="Процесс:")
            self.n_info.config(text="Новые данные:")
            self.t_tip = "Температура, Кельвин"
            self.p_tip = "Давление, Паскалей"
            self.process_var.set("не выбран")
            self.v_tip = "Объём, кубометров"
            if changed:
                self.chosen_process['menu'].delete(0, 'end')
                self.chosen_process['menu'].add_command(label="Изохорный", command=lambda: self.set_process("Изохорный"))
                self.chosen_process['menu'].add_command(label="Изотермический", command=lambda: self.set_process("Изотермический"))
                self.chosen_process['menu'].add_command(label="Изобарный", command=lambda: self.set_process("Изобарный"))
                self.chosen_process['menu'].add_command(label="Адиабатный", command=lambda: self.set_process("Адиабатный"))
                self.chosen_process['menu'].add_command(label="Политропный", command=lambda: self.set_process("Политропный"))

        create_tool_tip(self.big_t_pd, self.t_tip)
        create_tool_tip(self.big_t_nd, self.t_tip)
        create_tool_tip(self.big_v_pd, self.v_tip)
        create_tool_tip(self.big_v_nd, self.v_tip)
        create_tool_tip(self.big_p_pd, self.p_tip)
        create_tool_tip(self.big_p_nd, self.p_tip)

        create_tool_tip(self.prev_t, self.t_tip)
        create_tool_tip(self.prev_v, self.v_tip)
        create_tool_tip(self.prev_p, self.p_tip)
        create_tool_tip(self.new_t, self.t_tip)
        create_tool_tip(self.new_v, self.v_tip)
        create_tool_tip(self.new_p, self.p_tip)

    def swap_pos_data_graph(self):
        """Used ONLY from settings menu."""
        self.graph_cont.grid_forget()
        self.data_cont.grid_forget()

        match graph_pos:
            case True:
                column_g = 0
                column_d = 1
            case False:
                column_g = 1
                column_d = 0
            case _:
                raise TypeError(f'Expected to get boolean type but got "{type(graph_pos)}"')

        self.graph_cont.grid(row=0, column=column_g, sticky="nsew")
        self.data_cont.grid(row=0, column=column_d, sticky="nsew")

    def set_theme_mainpage(self): # ! Called ONLY from set_global_theme
        print("I should change colors when this ability will be added back. :P")

    def __validator(self, widget_name, value):
        global blocked_entries

        # Get entry class based on widget's name user is typing in
        entry = [
            widget
            for widget in [self.new_t, self.new_v, self.new_p]
            if widget_name == str(widget)
        ][0]

        another_entries: list[Entry] = None # ! Do not change this

        allowed = "0123456789.,"

        # TODO: Create some sort of highlighter when entered value is equals to 0 | Feature
        # * If digits equals to 0 it works fine
        # Change font color to red if entered value is equals to 0

        # if value != "" and all(symbol in allowed for symbol in value):
        #     if any(symbol in ".," for symbol in value) and value.replace(',', '.').count(".") > 0 and DIGITS > 0:
        #         splited_value = [part for part in value.replace(',', '.').split(".", 1) if part]
        #         # print(splited_value, "<- list | value ->", value)
        #     print("".join(value.replace(',', '.').split('.')))#, "from", f"{value[:(value.replace(',', '.').index('.'))]}")
        #     # entry.config(fg="#ff0000")
        # elif value.isdigit():
        #     entry.config(fg=fg)
        # elif value == "":
        #     entry.config(fg=fg)

        # Run through list and run function on all elements in that list using generator
        if value != "" and all(symbol in allowed for symbol in value):
            another_entries = [widget for widget in [self.new_t, self.new_v, self.new_p]if widget != entry and widget.cget("state") == "normal"]
            if another_entries:
                blocked_entries = another_entries
            [entry.config(state="disabled") for entry in another_entries]
        elif value == "" and all(symbol in allowed for symbol in value):
            [entry.config(state="normal") for entry in blocked_entries]
            blocked_entries = []

        # Entry validation, allowed values
        if all(symbol in allowed for symbol in value) and (
            (value.count(".") <= 1 and value.count(",") == 0)
            or (value.count(",") <= 1 and value.count(".") == 0)
        ):
            # limit decimal value to `digits` after dot/comma --> 0.000
            if "." in value.replace(',', '.'):
                if len(value[value.replace(',', '.').index(".") + 1 :]) > DIGITS:
                    return False
            return True
        else:
            return False


class NewDotPrompt(Toplevel):
    def __init__(self, main_page: MainPage):
        Toplevel.__init__(self, main_page.master.master, bg=bg)

        width, height = 261, 190

        self.transient(main_page.master.master)
        self.wait_visibility()
        self.grab_set()
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")
        self.resizable(0, 0)

        match current_language:
            case "rus":
                add_txt = "Добавить"
                volume_txt = "Объём:"
                cancel_txt = "Отмена"
                pressure_txt = "Давление:"
                title = "Данные первой точки:"
                temperature_txt = "Температура:"
                app_title = "Добавить первую точку"
            case "eng":
                temperature_txt = "Temperature:"
                app_title = "Add first dot"
                pressure_txt = "Pressure:"
                title = "First dot info:"
                volume_txt = "Volume:"
                cancel_txt = "Cancel"
                add_txt = "Add"

        self.title(app_title)

        # Title
        Label(self, bg=bg, fg=fg, font=ARIAL13+("underline",), text=title).pack(pady=(5, 10))

        fd_data = Frame(self, bg=bg)
        fd_data.pack()

        validator = (self.register(self.__validator),"%W", "%P")  # widget_name, value

        temperature_lbl = Label(fd_data, text=temperature_txt, font=ARIAL13, bg=bg, fg=fg)
        temperature_lbl.grid(row=0, column=0, sticky="nsew")
        temperature_data = Entry(
            fd_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        temperature_data.grid(row=0, column=1, pady=2, padx=5)

        volume_lbl = Label(fd_data, text=volume_txt, font=ARIAL13, bg=bg, fg=fg)
        volume_lbl.grid(row=1, column=0, sticky="nsew")
        volume_data = Entry(
            fd_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        volume_data.grid(row=1, column=1, pady=2, padx=5)

        pressure_lbl = Label(fd_data, text=pressure_txt, font=ARIAL13, bg=bg, fg=fg)
        pressure_lbl.grid(row=2, column=0, sticky="nsew")
        pressure_data = Entry(
            fd_data,
            width=10,
            bg=entry_bg,
            justify="center",
            validatecommand=validator,
            highlightbackground=entry_border,
            disabledforeground=dis_fg,
            disabledbackground=bg,
            validate="key",
            font=ARIAL13,
            fg=fg,
            bd=0,
        )
        pressure_data.grid(row=2, column=1, pady=2, padx=5)

        btn_cont = Frame(self)
        btn_cont.pack(side="bottom", pady=5)

        def add_first_dot(*_data):
            match current_language:
                case "rus":
                    msg = "Обнаружен нуль в данных!"
                case "eng":
                    msg = "Zero is found in data!"
            if not Decimal(0) in list(map(Decimal, [el.replace(",", ".") for el in _data])):
                main_page.begin_btn.config(state="disabled", cursor="")
                main_page.add_dot(True, _data)
                main_page.del_prev_btn.config(state="normal", cursor="hand2")                    
                main_page.clear_graph_btn.config(state="normal", cursor="hand2")
                self.destroy()
            else:
                showinfo("Info -- zero found", msg)

        add_btn = Button(btn_cont, text=add_txt, command=lambda: add_first_dot(pressure_data.get(), volume_data.get(), temperature_data.get()), bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, bd=0, font=ARIAL13, disabledforeground=dis_fg, state="disabled")
        add_btn.grid(row=0, column=0, padx=10, pady=5)
        cancel_btn = Button(btn_cont, text=cancel_txt, command=self.destroy, bg=btn_normal_bg, fg=fg, activeforeground=fg, activebackground=btn_active_bg, bd=0, font=ARIAL13)
        cancel_btn.grid(row=0, column=1, padx=10, pady=5)

        # Used in __validator
        self.add_btn = add_btn
        self.entered_data = []
        self.temperature_data = temperature_data
        self.volume_data = volume_data
        self.pressure_data = pressure_data

    def __validator(self, widget_name, value):

        # entry = [widget for widget in [self.temperature_data, self.volume_data, self.pressure_data] if widget_name == str(widget)][0]

        allowed = "0123456789.,"

        # Unlock add_btn
        if all(symbol in allowed for symbol in value) and len(value) > 0:
            if not widget_name in self.entered_data:
                self.entered_data.append(widget_name)
            if len(self.entered_data) == 3:
                self.add_btn["state"] = "normal"
        elif len(value) == 0:
            self.entered_data = [__entry for __entry in self.entered_data if __entry != widget_name]
            if len(self.entered_data) < 3:
                self.add_btn["state"] = "disabled"

        # TODO: Create some sort of highlighter when entered value is equals to 0 | Feature
        # * If digits equals to 0 it works fine
        # Change font color to red if entered value is equals to 0

        # if value != "" and all(symbol in allowed for symbol in value):
        #     if any(symbol in ".," for symbol in value) and value.replace(',', '.').count(".") > 0 and DIGITS > 0:
        #         splited_value = [part for part in value.replace(',', '.').split(".", 1) if part]
        #         # print(splited_value, "<- list | value ->", value)
        #     print("".join(value.replace(',', '.').split('.')))#, "from", f"{value[:(value.replace(',', '.').index('.'))]}")
        #     # entry.config(fg="#ff0000")
        # elif value.isdigit():
        #     entry.config(fg=fg)
        # elif value == "":
        #     entry.config(fg=fg)

        # Entry validation, allowed values
        if all(symbol in allowed for symbol in value) and (
            (value.count(".") <= 1 and value.count(",") == 0)
            or (value.count(",") <= 1 and value.count(".") == 0)
        ):
            # limit decimal value to `digits` after dot/comma --> 0.000
            if "." in value.replace(',', '.'):
                if len(value[value.replace(',', '.').index(".") + 1 :]) > DIGITS:
                    return False
            return True
        else:
            return False



class About(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, bg=bg)

        width, height = 231, 200

        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")
        self.resizable(0, 0)

        match current_language:
            case "rus":
                title = "О приложении"
                author_title = "Автор:"
                version_title = "Версия:"
                license_title = "Лицензия:"
            case "eng":
                version_title = "Version:"
                license_title = "License:"
                author_title = "Author:"
                title = "About"

        self.title(title)

        # Title
        Label(self, bg=bg, fg=fg, font=ARIAL13+("bold",), text=f"{APP_NAME}").pack(pady=(5, 10))

        # Version
        version_cont = Frame(self, bg=bg)
        version_cont.pack(pady=(5, 0), padx=(5, 0), fill="x")
        Label(version_cont, fg=fg, bg=bg, font=ARIAL13, text=version_title).grid(row=0, column=0)
        Label(version_cont, fg=fg, bg=bg, font=ARIAL13, text=version).grid(row=0, column=1)

        # Author
        author_cont = Frame(self, bg=bg)
        author_cont.pack(pady=(5, 0), padx=(5, 0), fill="x")
        Label(author_cont, fg=fg, bg=bg, font=ARIAL13, text=author_title).grid(row=0, column=0)
        author = Label(author_cont, bd=0, fg=fg, bg=bg, font=ARIAL13, text=AUTHOR, cursor="hand2")
        author.grid(row=0, column=1)
        author.bind("<Enter>", lambda _: author.config(fg="#0000FF", font=ARIAL13+("underline",)))
        author.bind("<Leave>", lambda _: author.config(fg=fg, font=ARIAL13))
        author.bind("<1>", lambda _: open_new_tab("https://github.com/TerraBoii"))

        # License
        license_cont = Frame(self, bg=bg)
        license_cont.pack(pady=(5, 0), padx=(5, 0), fill="x")
        Label(license_cont, fg=fg, bg=bg, font=ARIAL13, text=license_title).grid(row=0, column=0)
        Label(license_cont, fg=fg, bg=bg, font=ARIAL13, text="MIT license").grid(row=0, column=1)

        Button(self, text='OK', font=ARIAL13, bg=btn_normal_bg, fg=fg, activebackground=btn_active_bg, activeforeground=fg, cursor="hand2", command=self.destroy, width=7).pack(side="bottom", pady=(0, 10))


class Help(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, bg=bg)

        width, height = 200 + 31, 200 # * Do not change "+ 31" for width

        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")
        self.resizable(0, 0)

        match current_language:
            case "rus":
                title = "Помощь"
            case "eng":
                title = "Help"

        self.title(title)


class Settings(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, bg=bg)

        width, height = 281, 250

        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")
        self.resizable(0, 0)

        # Settings title label
        setting_title = Label(self, bg=bg, fg=fg, font=ARIAL13)
        setting_title.pack(pady=(12, 0))

        options = {"Справа": False, "Слева": True, "On the right": False, "On the left": True,
                   "English": "eng", "Русский": "rus",
                   "Светлая": "light", "Тёмная": "dark", "Light": "light", "Dark": "dark"}

        # Graph position settings
        def change_graph_pos(to_pos: str):
            match to_pos:
                case "On the right":
                    graph_pos_var.set("On the right")
                    choose_graph_pos['menu'].delete(0, 'end')
                    choose_graph_pos['menu'].add_command(label="On the left", command=lambda: change_graph_pos("On the left"))
                case "On the left":
                    graph_pos_var.set("On the left")
                    choose_graph_pos['menu'].delete(0, 'end')
                    choose_graph_pos['menu'].add_command(label="On the right", command=lambda: change_graph_pos("On the right"))
                case "Справа":
                    graph_pos_var.set("Справа")
                    choose_graph_pos['menu'].delete(0, 'end')
                    choose_graph_pos['menu'].add_command(label="Слева", command=lambda: change_graph_pos("Слева"))
                case "Слева":
                    graph_pos_var.set("Слева")
                    choose_graph_pos['menu'].delete(0, 'end')
                    choose_graph_pos['menu'].add_command(label="Справа", command=lambda: change_graph_pos("Справа"))

        graph_pos_var = StringVar()

        graph_set_cont = Frame(self, bg=bg)
        graph_set_cont.pack(pady=(5, 0), fill="x", padx=(5, 0))

        graph_title = Label(graph_set_cont, bg=bg, fg=fg, font=ARIAL13+("underline",))
        graph_title.grid(row=0, column=0)

        match graph_pos, current_language:
            case True, "eng":
                graph_pos_options = ["On the right"]
                graph_pos_var.set("On the left")
            case False, "eng":
                graph_pos_options = ["On the left"]
                graph_pos_var.set("On the right")
            case True, "rus":
                graph_pos_options = ["Справа"]
                graph_pos_var.set("Слева")
            case False, "rus":
                graph_pos_options = ["Слева"]
                graph_pos_var.set("Справа")

        choose_graph_pos = OptionMenu(graph_set_cont, graph_pos_var, *graph_pos_options, command=change_graph_pos)
        choose_graph_pos.config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, indicatoron=False, bg=btn_normal_bg, activebackground=btn_active_bg, direction="right")
        choose_graph_pos["menu"].config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        choose_graph_pos.grid(row=0, column=1)

        # Change language
        lang = StringVar()

        lang_cont = Frame(self, bg=bg)
        lang_cont.pack(pady=(5, 0), fill="x", padx=(5, 0))

        lang_title = Label(lang_cont, bg=bg, fg=fg, font=ARIAL13+("underline",))
        lang_title.grid(row=0, column=0)

        match current_language:
            case "rus":
                lang_options = ["English"]
                lang.set("Русский")
            case "eng":
                lang_options = ["Русский"]
                lang.set("English")

        def change_lang(to_lang: str):
            global current_language
            match to_lang:
                case "English":
                    lang.set("English")
                    self.set_lang_settings("eng", True)
                    choose_lang['menu'].delete(0, 'end')
                    choose_lang['menu'].add_command(label="Русский", command=lambda: change_lang("Русский"))
                case "Русский":
                    lang.set("Русский")
                    self.set_lang_settings("rus", True)
                    choose_lang['menu'].delete(0, 'end')
                    choose_lang['menu'].add_command(label="English", command=lambda: change_lang("English"))
                case _:
                    print(F"What is -> '{to_lang}', {type(to_lang)}")

        choose_lang = OptionMenu(lang_cont, lang, *lang_options, command=change_lang)
        choose_lang.config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, indicatoron=False, bg=btn_normal_bg, activebackground=btn_active_bg, direction="right")
        choose_lang["menu"].config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        choose_lang.grid(row=0, column=1)

        # Change theme
        theme = StringVar()

        theme_cont = Frame(self, bg=bg)
        theme_cont.pack(pady=(5, 0), fill="x", padx=(5, 0))

        theme_title = Label(theme_cont, bg=bg, fg=fg, font=ARIAL13+("underline",))
        theme_title.grid(row=0, column=0)

        match current_language, current_theme:
            case "rus", 'light':
                theme_options = ["Тёмная"]
                theme.set("Светлая")
            case "eng", "light":
                theme_options = ["Dark"]
                theme.set("Light")
            case "rus", 'dark':
                theme_options = ["Светлая"]
                theme.set("Тёмная")
            case "eng", "dark":
                theme_options = ["Light"]
                theme.set("Dark")

        def change_theme(to_theme: str):
            match to_theme:
                case "Light":
                    theme.set("Light")
                    choose_theme['menu'].delete(0, 'end')
                    choose_theme['menu'].add_command(label="Dark", command=lambda: change_theme("Dark"))
                case "Dark":
                    theme.set("Dark")
                    choose_theme['menu'].delete(0, 'end')
                    choose_theme['menu'].add_command(label="Light", command=lambda: change_theme("Light"))
                case "Светлая":
                    theme.set("Светлая")
                    choose_theme['menu'].delete(0, 'end')
                    choose_theme['menu'].add_command(label="Тёмная", command=lambda: change_theme("Тёмная"))
                case "Тёмная":
                    theme.set("Тёмная")
                    choose_theme['menu'].delete(0, 'end')
                    choose_theme['menu'].add_command(label="Светлая", command=lambda: change_theme("Светлая"))
                case _:
                    print(F"What is -> '{to_theme}', {type(to_theme)}")

        choose_theme = OptionMenu(theme_cont, theme, *theme_options, command=change_theme)
        choose_theme.config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, indicatoron=False, bg=btn_normal_bg, activebackground=btn_active_bg, direction="right")
        choose_theme["menu"].config(font=ARIAL13, bd=0, fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        choose_theme.grid(row=0, column=1)

        # Bottom buttons
        def confirm():
            global graph_pos, current_language, current_theme
            if graph_pos != options[graph_pos_var.get()]:
                graph_pos = options[graph_pos_var.get()]
                parent.get_page(MainPage).swap_pos_data_graph()
            if current_language != options[lang.get()]:
                current_language = options[lang.get()]
                parent.get_page(MainPage).set_lang_mainpage(True)
            if current_theme != options[theme.get()]:
                self.set_global_theme(options[theme.get()])
            cancel()

        def cancel():
            self.destroy()

        btn_cont = Frame(self, bg=bg)
        btn_cont.pack(side="bottom", pady=(0, 10))
        confirm_btn = Button(btn_cont, font=ARIAL13, bd=0, bg=btn_normal_bg, fg=fg, activebackground=btn_active_bg, activeforeground=fg, cursor="hand2", command=confirm)
        confirm_btn.grid(row=0, column=0, padx=(0, 2))
        cancel_btn = Button(btn_cont, font=ARIAL13, bd=0, bg=btn_normal_bg, fg=fg, activebackground=btn_active_bg, activeforeground=fg, cursor="hand2", command=cancel)
        cancel_btn.grid(row=0, column=1, padx=(2, 0))

        # Variables -> attributes, to call from methods
        # Containers
        self.graph_set_cont = graph_set_cont
        self.btn_cont = btn_cont
        self.lang_cont = lang_cont
        self.theme_cont = theme_cont
        # Labels
        self.setting_title = setting_title
        self.graph_title = graph_title
        self.lang_title = lang_title
        self.theme_title = theme_title
        # Option menus
        self.choose_graph_pos = choose_graph_pos
        self.choose_lang = choose_lang
        self.choose_theme = choose_theme
        # Buttons
        self.confirm_btn = confirm_btn
        self.cancel_btn = cancel_btn
        # Variables (*var)
        self.graph_pos_var = graph_pos_var
        self.lang = lang
        self.theme = theme
        # Functions
        self.change_graph_pos = change_graph_pos
        self.change_lang = change_lang
        self.change_theme = change_theme

        self.set_lang_settings()

    def set_lang_settings(self, lang: str = None, preview: bool = False):
        if lang is None:
            lang = current_language
        match lang:
            case "rus":
                self.title("Настройки")
                self.cancel_btn.config(text="Отмена")
                self.confirm_btn.config(text="Подтвердить")
                self.setting_title.config(text="Настройки:")
                self.lang_title.config(text="Текущий язык:")
                self.theme_title.config(text="Текущая тема:")
                self.graph_title.config(text="Положение графика:")
                if preview:
                    match self.theme.get():
                        case "Light":
                            self.theme.set("Светлая")
                            self.choose_theme['menu'].delete(0, 'end')
                            self.choose_theme['menu'].add_command(label="Тёмная", command=lambda: self.change_theme("Тёмная"))
                        case "Dark":
                            self.theme.set("Тёмная")
                            self.choose_theme['menu'].delete(0, 'end')
                            self.choose_theme['menu'].add_command(label="Светлая", command=lambda: self.change_theme("Светлая"))
                    match self.graph_pos_var.get():
                        case "On the right":
                            self.graph_pos_var.set("Справа")
                            self.choose_graph_pos['menu'].delete(0, 'end')
                            self.choose_graph_pos['menu'].add_command(label="Слева", command=lambda: self.change_graph_pos("Слева"))
                        case "On the left":
                            self.graph_pos_var.set("Слева")
                            self.choose_graph_pos['menu'].delete(0, 'end')
                            self.choose_graph_pos['menu'].add_command(label="Справа", command=lambda: self.change_graph_pos("Справа"))
            case "eng":
                self.cancel_btn.config(text="Cancel")
                self.confirm_btn.config(text="Confirm")
                self.setting_title.config(text="Settings:")
                self.theme_title.config(text="Current theme:")
                self.graph_title.config(text="Graph position:")
                self.lang_title.config(text="Current language:")
                self.title("Settings")
                if preview:
                    match self.theme.get():
                        case "Светлая":
                            self.theme.set("Light")
                            self.choose_theme['menu'].delete(0, 'end')
                            self.choose_theme['menu'].add_command(label="Dark", command=lambda: self.change_theme("Dark"))
                        case "Тёмная":
                            self.theme.set("Dark")
                            self.choose_theme['menu'].delete(0, 'end')
                            self.choose_theme['menu'].add_command(label="Light", command=lambda: self.change_theme("Light"))
                    match self.graph_pos_var.get():
                        case "Справа":
                            self.graph_pos_var.set("On the right")
                            self.choose_graph_pos['menu'].delete(0, 'end')
                            self.choose_graph_pos['menu'].add_command(label="On the left", command=lambda: self.change_graph_pos("On the left"))
                        case "Слева":
                            self.graph_pos_var.set("On the left")
                            self.choose_graph_pos['menu'].delete(0, 'end')
                            self.choose_graph_pos['menu'].add_command(label="On the right", command=lambda: self.change_graph_pos("On the right"))

    def set_theme_settings(self): # ! Called ONLY from set_global_theme
        self.config(bg=bg)
        # Containers
        self.graph_set_cont.config(bg=bg)
        self.btn_cont.config(bg=bg)
        self.lang_cont.config(bg=bg)
        self.theme_cont.config(bg=bg)
        # Labels
        self.setting_title.config(bg=bg,fg=fg)
        self.graph_title.config(bg=bg, fg=fg)
        self.lang_title.config(bg=bg, fg=fg)
        # Option menus
        self.choose_graph_pos.config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        self.choose_graph_pos["menu"].config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        self.choose_lang.config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        self.choose_lang["menu"].config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        self.choose_theme.config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        self.choose_theme["menu"].config(fg=fg, activeforeground=fg, bg=btn_normal_bg, activebackground=btn_active_bg)
        # Buttons
        self.confirm_btn.config(bg=btn_normal_bg, fg=fg, activebackground=btn_active_bg, activeforeground=fg)
        self.cancel_btn.config(bg=btn_normal_bg, fg=fg, activebackground=btn_active_bg, activeforeground=fg)

    def set_global_theme(self, theme):
        change_theme(theme)
        self.set_theme_settings()
        self.parent.get_page(MainPage).set_theme_mainpage()


if __name__ == "__main__":
    MainAppBody().mainloop()
