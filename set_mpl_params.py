from matplotlib import rcParams

def set_mpl_params():
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
    rcParams["keymap.forward"].append("ctrl+y")
    rcParams["keymap.back"].append("ctrl+z")
    rcParams["figure.edgecolor"] = "#D9D9D9"
    rcParams["figure.facecolor"] = "#D9D9D9"
    rcParams["axes.facecolor"] = "#EFEFEF"
