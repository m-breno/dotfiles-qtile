#       _   _ _     
#  __ _| |_(_) |___ 
# / _` |  _| | / -_)
# \__, |\__|_|_\___|
#    |_| config by m-breno

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from libqtile.backend.wayland.inputs import InputConfig
#from qtile_extras.widget import StatusNotifier
#from libqtile.extension.dmenu import DmenuRun

#    __              
#   / /_____ __ _____
#  /  '_/ -_) // (_-<
# /_/\_\\__/\_, /___/
#          /___/     

# super = "mod4", alt = "mod1"
mod = "mod4"

keys = [
    # Launch apps
    Key([mod], "Return", lazy.spawn("foot"), desc = "Launch terminal"),
    Key([mod, "shift"], "w", lazy.spawn("librewolf"), desc = "Launch Web Browser"),
    Key([mod, "shift"], "f", lazy.spawn("thunar"), desc = "Launch File Manager"),
    Key([mod, "shift"], "d", lazy.spawn("discord"), desc = "Launch Discord"),

    # Spawn a command using a prompt widget
    Key([mod], "d", lazy.spawncmd(), desc = "Spawn a command using a prompt widget"),
    # Kill focused window
    Key([mod], "w", lazy.window.kill(), desc = "Kill focused window"),
    
    # Toggle fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc = "Toggle fullscreen on the focused window",),
    # Toggle floating
    Key([mod], "Space", lazy.window.toggle_floating(), desc = "Toggle floating on the focused window"),
    # Reload config
    Key([mod, "shift"], "r", lazy.reload_config(), desc = "Reload the config"),
    # Exit Qtile
    Key([mod, "shift"], "q", lazy.shutdown(), desc = "Shutdown Qtile"),

    # Switch between groups
    Key([mod], "Tab", lazy.screen.next_group(), desc = "Switch to next group"),
    Key([mod, "shift"], "Tab", lazy.screen.prev_group(), desc = "Switch to previous group"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(),     desc = "Move focus to left"),
    Key([mod], "j", lazy.layout.down(),     desc = "Move focus down"),
    Key([mod], "k", lazy.layout.up(),       desc = "Move focus up"),
    Key([mod], "l", lazy.layout.right(),    desc = "Move focus to right"),
    Key(["mod1"], "Tab", lazy.layout.next(), desc = "Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),    desc = "Move window to the left"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),    desc = "Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),      desc = "Move window up"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),   desc = "Move window to the right"),

    # Grow/shrink windows
    Key([mod, "control"], "h", lazy.layout.grow_left(),  desc = "Grow window to the left"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),  desc = "Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),    desc = "Grow window up"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc = "Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc = "Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc = "Toggle between split and unsplit sides of stack",
    ),

    # Toggle between different layouts as defined below
    #Key([mod], "Tab", lazy.next_layout(), desc = "Toggle between layouts"),


    # System keys
    # Screenshot
    Key([], "Print", lazy.spawn("grim ~/Pictures/Screenshots/screenshot-$(date '+%y.%m.%d-%H:%M:%S').png | wl-copy")),
    Key([mod], "Print", lazy.spawn("slurp | grim -g - ~/Pictures/Screenshots/screenshot-$(date '+%y.%m.%d-%H:%M:%S').png | wl-copy")),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    
    # Media
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"), 

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brillo -A 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brillo -U 5"))
]

# Drag floating windows.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start = lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start = lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Add key bindings to switch VTs in Wayland.
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc = f"Switch to VT{vt}"
        )
    )

                             
#   ___ ________  __ _____  ___
#  / _ `/ __/ _ \/ // / _ \(_-<
#  \_, /_/  \___/\_,_/ .__/___/
# /___/             /_/(aka. workspaces)

groups = [
    Group(
        "1",
        label = "TERM",
        matches = [Match(wm_class = "foot")]
    ),
    Group(
        "2",
        label = "WEB",
        matches = [Match(wm_class = "librewolf")],
        layout = "max"
    ),
    Group(
        "3",
        label = "FILES",
        matches = [
            Match(wm_class = "Thunar"),
            Match(wm_class = "qbittorrent"),
        ],
        layout = "floating"
    ),
    Group(
        "4",
        label = "DOC",
        matches = [
            Match(wm_class = "obsidian")
        ],
        layout = "max"
    ),
    Group(
        "5",
        label = "MEDIA",
        matches = [
            Match(wm_class = "mpv"),
            Match(wm_class = "music"),
            Match(wm_class = "ru-turikhay-tlauncher-bootstrap-Bootstrap")
        ],
        layout = "floating"
    ),
    Group(
        "6",
        label = "CHAT",
        matches = [
            Match(wm_class = "discord"),
            Match(wm_class = "ZapZap")
        ],
        layout = "max"
    ),
    Group(
        "7",
        label = "ETC",
        matches = [
            Match(wm_class = "org.pulseaudio.pavucontrol"),
            Match(wm_class = "nwg-look"),
            Match(wm_class = "nmtui")
        ],
        layout = "monadtall"
    )
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc = f"Switch to group {i.name}"),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc = f"Switch to & move focused window to group {i.name}",
            )
        ]
    )

#    __                    __    
#   / /__ ___ _____  __ __/ /____
#  / / _ `/ // / _ \/ // / __(_-<
# /_/\_,_/\_, /\___/\_,_/\__/___/
#        /___/                   

layouts = [
    layout.Columns(
        border_focus = "#ffffff",
        border_focus_stack = ["#d75f5f", "#8f3d3d"],
        border_normal = "#242424",
        border_width = 1,

        margin = 5,
        margin_on_single = 0,

        wrap_focus_columns = False,
        wrap_focus_rows = False,
        wrap_focus_stacks = False
    ),
    layout.Max(),
    layout.MonadTall(),
]

#          _    __         __    
#  _    __(_)__/ /__ ____ / /____
# | |/|/ / / _  / _ `/ -_) __(_-<
# |__,__/_/\_,_/\_, /\__/\__/___/
#              /___/             

widget_defaults = dict(
    font = "Terminus",
    foreground = "#AAAAAA",
    fontsize = 10,
    padding = 3
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(
                    borderwidth = 1,
                    highlight_method = "text",
                    this_current_screen_border = "#FFFFFF",
                    active = "#808080",
                    inactive = "#242424",
                    this_screen_border = "#0000FF",
                    padding = 2
                ),
                widget.Prompt(
                    prompt = "RUN: "
                ),
                widget.WindowName(
                    format = "{state} {class}"
                ),

                widget.Notify(),
                widget.StatusNotifier(),
                #StatusNotifier(),
                #widget.Wttr(
                #    format = "%c%t (H%h)"
                #),
                #widget.Mpd2(
                #    mouse_callbacks = {
                #        "Button3": lazy.spawn("foot -a music ncmpcpp")
                #    },
                #    mouse_buttons = {1: "toggle", 4: "previous", 5: "next"},
                #    idle_format = "MPD: IDLE",
                #    status_format = "MPD: {play_status} {artist} - {title}",
                #    color_progress = "#FFFFFF"
                #),
                #widget.Mpris2(),
                widget.CPU(
                    format = "CPU: {load_percent}%",
                    update_interval = 5,
                    foreground = "#FF00FF"
                    #foreground = "#FF00FF"
                ),
                widget.ThermalSensor(
                    tag_sensor = "Package id 0",
                    update_interval = 5,
                    foreground = "#FF40FF"
                    #foreground = "#FF00FF"
                ),
                widget.Memory(
                    format = "MEM: {MemPercent:.0f}%",
                    update_interval = 5,
                    foreground = "#5555FF"
                    #foreground = "#FF0000"
                ),
                widget.Wlan(
                    interface = "wlo1",
                    disconnected_message = "NET: DIS",
                    use_ethernet = True,
                    ethernet_interface = "enp1s0",
                    ethernet_message = "NET: ETH",
                    format = "NET: CON ({percent:2.0%})",
                    mouse_callbacks = {
                        "Button3": lazy.spawn("foot -a nmtui nmtui")
                    },
                    foreground = "#55FFFF"
                    #foreground = "#FF8000"
                ),
                widget.Volume(
                    step = 5,
                    unmute_format = "VOL: {volume}%",
                    mute_format = "VOL: MUTE",
                    volume_app = "pavucontrol",
                    foreground = "#00FF00"
                    #foreground = "#FFFF00"
                ),
                widget.Backlight(
                    backlight_name = "intel_backlight",
                    change_command = "brillo -S {0}",
                    step = 5,
                    format = "BRI: {percent:2.0%}",
                    foreground = "#FFFF00"
                    #foreground = "#00FF00"
                ),
                widget.Battery(
                    charge_char = "+",
                    discharge_char = "-",
                    empty_char = "x",
                    format = "BAT: {char}{percent:2.0%} ({hour:d}h{min:02d}m)",
                    show_short_text = False,
                    foreground = "#FF8000"
                    #foreground = "#55FFFF"
                ),
                widget.Clock(
                    format = "%a %d/%m %H:%M:%S"
                ),
                widget.QuickExit(
                    default_text = "[X]",
                    countdown_format = "[{}]",
                    foreground = "#FF0000"
                    #foreground = "#5555FF"
                ),
            ],
            16,
            background = "#000000",
            border_width = [1, 0, 0, 0],
            border_color = ["242424", "000000", "000000", "000000"],
            margin = [-1, 0, 0, 0]
        ),

        wallpaper = "/usr/share/backgrounds/archlinux/archwave.png",
        #wallpaper = "/home/breno/Imagens/arch_outline.png",
        wallpaper_mode = "fill"
    ),
]

#          _               __      
#  _    __(_)__  ______ __/ /__ ___
# | |/|/ / / _ \/ __/ // / / -_|_-<
# |__,__/_/_//_/_/  \_,_/_/\__/___/

# Always floating windows
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class = "confirmreset"),  # gitk
        Match(wm_class = "makebranch"),  # gitk
        Match(wm_class = "maketag"),  # gitk
        Match(wm_class = "ssh-askpass"),  # ssh-askpass
        Match(title = "branchdialog"),  # gitk
        Match(title = "pinentry"),  # GPG key password entry
        Match(wm_class = "thunar"),
        Match(title = "Picture-in-Picture"),
        Match(wm_class = "nwg-look"),
        Match(wm_class = "Extensão: (Bitwarden Gerenciador de Senhas) - Bitwarden — Mozilla Firefox"),
        Match(wm_class = "org.pulseaudio.pavucontrol"),
        Match(wm_class = "music"),
        Match(wm_class = "nmtui")
    ],
    border_width=1,
    border_focus="#FFFFFF",
    border_normal="#000000",
)

# Auto switch to group
@hook.subscribe.client_managed
def auto_switch(window):
    if window.group.name != qtile.current_group.name:
        window.group.cmd_toscreen()

# Pin windows/show on all groups
sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window

@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return

@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)

@hook.subscribe.client_managed
def auto_sticky_windows(window):
    info = window.info()
    if info["name"] == "Picture-in-Picture":
        sticky_windows.append(window)

keys.extend([
    Key([mod], "p", toggle_sticky_windows(), desc="Toggle state of sticky for current window"),
]),

follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

#    _                __ 
#   (_)__  ___  __ __/ /_
#  / / _ \/ _ \/ // / __/
# /_/_//_/ .__/\_,_/\__/ 
#       /_/              

wl_input_rules = {
    "type:pointer": InputConfig(
        pointer_accel = -0.5,
        accel_profile = "flat",
        natural_scroll = False,
    ),
    "type:touchpad": InputConfig(
        click_method = "clickfinger",
        tap = True,
        drag = True,
        natural_scroll = True,
    ),
    "type:keyboard": InputConfig(
        kb_layout = "br",
        kb_options = "caps:escape,altwin:menu_win",
    )
}

wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"
