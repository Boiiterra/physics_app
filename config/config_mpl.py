from matplotlib import rcParams


def config_mpl(figure_color, axes_color):
    """Manipulate rcParams for matplotlib plots"""
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
    rcParams["keymap.back"].append("ctrl+z")
    rcParams["keymap.forward"].append("ctrl+y")
    rcParams["figure.edgecolor"] = figure_color
    rcParams["figure.facecolor"] = figure_color
    rcParams["axes.facecolor"] = axes_color
