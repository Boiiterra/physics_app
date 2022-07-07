from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class NavigationToolbar(NavigationToolbar2Tk):
    """Display necessary buttons:\n
    Home, Back, Forward, Pan and Zoom"""

    NavigationToolbar2Tk.toolitems = (
        ("Home", "Reset to original view", "home", "home"),
        ("Back", "Back to previous view", "back", "back"),
        ("Forward", "Forward to next view", "forward", "forward"),
        (None, None, None, None),
        ("Pan", "Pan axes with left mouse, zoom with right", "move", "pan"),
        ("Zoom", "Zoom to rectangle", "zoom_to_rect", "zoom"),
        (None, None, None, None),
    )