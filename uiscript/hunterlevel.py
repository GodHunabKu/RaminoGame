import uiScriptLocale

BOARD_WIDTH = 500
BOARD_HEIGHT = 520

window = {
    "name": "HunterLevelWindow",
    "style": ("movable", "float",),
    "x": 0,
    "y": 0,
    "width": BOARD_WIDTH,
    "height": BOARD_HEIGHT,
    "children":
    (
        {
            "name": "BaseWindow",
            "type": "window",
            "style": ("not_pick",),
            "x": 0,
            "y": 0,
            "width": BOARD_WIDTH,
            "height": BOARD_HEIGHT,
        },
    ),
}
