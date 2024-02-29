import subprocess as sp
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
alt = "mod1"
terminal = "kitty"
rofi = "rofi -show run"
browser = "firefox"
editor = "code"
colors = ["#ef0a55","#b0b0b0","#0fafa1","#fff","#000"]
keys = [
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "q", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(rofi), desc="Spawn a Rofi"),
    Key([mod], "f", lazy.spawn(browser), desc="Spawn a Default Browser"),
    Key([mod], "c", lazy.spawn(editor), desc="Spawn a Default Editor")
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in ["", "󰈹", "󰨞", "", "󰓇", "", "󰒋", "󰖣"]]

for i, group in enumerate(groups):
    areaNumber = str(i+1)
    keys.extend([
            # mod1 + group number = switch to group
            Key([mod], areaNumber, lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key([mod, "shift"], areaNumber, lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(margin=5, border_focus="#eddc87", border_width=2),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Hack Nerd Font Mono Regular",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def left_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=25,
        background=bg_color,
        foreground=fg_color)

def right_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=35,
        background=bg_color,
        foreground=fg_color)

def show_icon(icon, bg_color, fg_color):
    return widget.TextBox(
        text=icon,
        padding=0,
        fontsize=30,
        background=bg_color,
        foreground=fg_color)

def local_con(bg_color, fg_color):
    ip = sp.check_output('hostname -I', shell=True)
    ip = str(ip)[2:][:-1]
    if ip.count(' ') > 1:
        vpn = ip.split(' ')[1]
        ip = ip.split(' ')[0]
    else:
        vpn="NO"
    return widget.TextBox(
        text=f"Local:{ip[:-3]} VPN:{vpn} ",
        padding=0,
        fontsize=16,
        background=bg_color,
        foreground=fg_color)

screens = [
    Screen(
        top=bar.Bar(
            [
              widget.GroupBox(
                active="#fff",
                inactive="#222",
                fontsize=20,
                highlight_method='text',
                block_highlight_text_color="#ff0",
                disable_drag=True,
                margin_y=2,
                padding_x=12,
                center_aligned=True,
                urgent_text="#f00",
                use_mouse_wheel=False,
                rounded=False,
                highlight_color="#000",
                this_current_screen_border=["#d6cf85", "#d6cf85"],
            ),
              widget.WindowName(),
              left_arrow("#000","#662903"),
              local_con("#662903", "#ccc"),
              left_arrow("#662903","#75712e"),
              widget.PulseVolume(fmt="Sound: {}", background="#75712e", fontsize=16,),
              left_arrow("#75712e", "#3e0f70"),
              widget.Clock(format="%d/%m/%Y", background="#3e0f70"),
              left_arrow("#3e0f70", "#114455"),
              widget.Clock(format="%H:%M:%S ", background="#114455"),
            ],
            28,
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
