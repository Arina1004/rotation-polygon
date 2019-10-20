canvas_width = 1000
canvas_height = 600

radius = 300
square_size = 50

action = 'stop'

INIT = 'INIT'
DRAW_START = 'DRAW_START'
ADD_VERTEX = 'ADD_VERTEX'
NEW_POLYGON = 'NEW_POLYGON'
ADD_VERTEX_POLYGON = 'ADD_VERTEX_POLYGON'
DRAW_END = 'DRAW_END'

moving_point = -1

last_state = INIT
state = INIT

polygons = []

time = 0