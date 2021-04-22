from aenum import Enum, NoAlias
import color


class TileType(Enum, settings=NoAlias):
    EM_HID = color.GREY
    BO_HID = color.GREY
    EM_VIS = color.LIGHT_GREY
    BO_VIS = color.RED
    EM_FLA = color.GREEN
    BO_FLA = color.GREEN
