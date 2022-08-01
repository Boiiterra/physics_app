from matplotlib import rcParams


def config_mpl_cmd():
    """Change rcParams for matplotlib plots"""
    # Remove unnecessary params
    rcParams["keymap.copy"] = []
    rcParams["keymap.help"] = []
    rcParams["keymap.quit"] = []
    rcParams["keymap.save"] = []
    rcParams["keymap.xscale"] = []
    rcParams["keymap.yscale"] = []
    rcParams["keymap.fullscreen"] = []
    rcParams["keymap.back"].remove("c")
    rcParams["keymap.forward"].remove("v")
    rcParams["keymap.back"].remove("backspace")
    # Change params
    rcParams["keymap.home"] = ["h", "home", "р"]
    # Add params
    rcParams["keymap.forward"].append("ctrl+y")
    rcParams["keymap.grid_minor"].append("П")
    rcParams["keymap.back"].append("ctrl+z")
    rcParams["keymap.grid"].append("п")
    rcParams["keymap.zoom"].append("щ")
    rcParams["keymap.pan"].append("з")


def config_mpl_color(figure_color, axes_color, grid_color, text_color):
    """Change rcParams for matplotlib plots"""
    rcParams["figure.edgecolor"] = figure_color
    rcParams["figure.facecolor"] = figure_color
    rcParams["axes.labelcolor"] = text_color
    rcParams["axes.edgecolor"] = text_color
    rcParams["axes.facecolor"] = axes_color
    rcParams["xtick.color"] = text_color
    rcParams["ytick.color"] = text_color
    rcParams["grid.color"] = grid_color
    rcParams["text.color"] = text_color
