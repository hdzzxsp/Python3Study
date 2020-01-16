from initGame import *
from Painter import Painter

# 定义地图
painter = Painter(global_map, global_mapIndex, global_STEP, global_gateCount)
painter.setDataByMap()
painter.paintMap()

# 启动游戏
painter.startPlay()
