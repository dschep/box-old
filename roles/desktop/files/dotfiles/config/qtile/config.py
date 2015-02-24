from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

mod = 'mod1'

keys = [
    # Switch between windows
    Key([mod], 'j', lazy.layout.down()),
    Key([mod], 'k', lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up()),

    # grow/shrink monad master
    Key([mod], 'l', lazy.layout.grow()),
    Key([mod], 'h', lazy.layout.shrink()),

    # Spawn terminal
    Key([mod, 'shift'], 'Return', lazy.spawn('x-terminal-emulator')),

    # lock screen terminal
    Key([mod, 'shift'], 'l', lazy.spawn('lxlock')),

    # Toggle between different layouts as defined below
    Key([mod], 'space', lazy.nextlayout()),
    Key([mod, 'shift'], 'space', lazy.nextlayout()),

    # Close window
    Key([mod, 'shift'], 'c', lazy.window.kill()),

    # restart & quit
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),

    # prompt
    Key([mod], 'p', lazy.spawncmd(prompt='run')),

    # Toggle float
    Key([mod, 'control'], 'space', lazy.window.toggle_floating()),

    # toggle fullscreen
    Key([mod], 'f', lazy.window.toggle_fullscreen()),
]

groups = [Group(i) for i in '123456789']

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.MonadTall(),
    layout.Zoomy(),
    layout.Floating(),
    layout.Max(),
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()

@hook.subscribe.client_new
def grouper(window):
    instance, class_ = window.window.get_wm_class()

    rules = [
        (['Chromium-browser (/home/dschep/.config/chromium-dev)'], [], 1, False),
        ([], ['workvim', 'workterm'], '2', False),
        (['celerity.hipchat.com__chat', 'socialcode.hipchat.com__chat'], [], 7, False),
        (['Chromium-browser'], [], 8, False),
        ([], ['Firefox'], 9, False),
        ([], ['mplayer2', 'plugin-container', 'Plugin-container'], None, True),
    ]

    for instances, classes, group, float_ in rules:
        if instance in instances or class_ in classes:
            if group is not None:
                window.togroup(group)
            window.floating = float_



dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = 'qtile'
