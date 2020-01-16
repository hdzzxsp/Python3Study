from initGame import *
from Painter import Painter
import  os

mpath = os.path.dirname(__file__)
# 定义地图
painter = Painter(global_map, global_mapIndex, global_STEP, global_gateCount)
painter.setDataByMap()
painter.paintMap()

# 播放声音
soundname = mpath+'\\bgm.mp3'
painter.playSound(soundname)

# 启动游戏
painter.startPlay()
