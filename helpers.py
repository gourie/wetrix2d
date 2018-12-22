# NEW CODE for VPython 7
from vpython import *

MARGIN = 0.1
TITLE_BAR = 22

# noinspection PyPackageRequirements
def open_display(title = "VPython Window", width=1200, height=600, bg_color=color.black):
    d = canvas(title=title,
               width=width, height=height,
               center=vector(0,0,0) + vector(width, height, 0) / 2.0, background=bg_color)
    return d

SILENT = 0
WARN = 1
INFO = 2
DEBUG = 3

LOG_LEVEL = DEBUG

def debug(msg, *args):
    if LOG_LEVEL >= DEBUG:
        log("D", msg, args)
        
def info(msg, *args):
    if LOG_LEVEL >= INFO:
        log("I", msg, args)
        
def warn(msg, *args):
    if LOG_LEVEL >= WARN:
        log("W", msg, args)
        
def log(tag, msg, args):
    if LOG_LEVEL > SILENT:
        if len(args) > 0:
            print("[{}] {} -- {}".format(tag, msg, args))
        else:
            print("[{}] {}".format(tag, msg))

# small test script that draws border and one box at top
scene = open_display()
box_unit_size = 10
for i in range(120):
    box(pos=vector(i*box_unit_size, 0, 0), length=box_unit_size, height=box_unit_size, width=1, color=color.gray(0.5))
while True:
    rate(30)
    box(pos=vector(scene.width/2.0, scene.height, 0), length=box_unit_size, height=box_unit_size, width=1, color=color.blue)



# OLD CODE for VPython 6
# from visual import window, display, frame, vector, curve, color, rate
#
# MARGIN = 0.1
# TITLE_BAR = 22
#
# def open_display(title = "VPython Window", width = 800, height = 600, ll_pos = (0,0), visible_bounds=False):
#   d = display(title = title, width = width, height = height + TITLE_BAR)
#   d.select()
#   d.autocenter = False
#   d.center = vector(ll_pos) + vector(width, height) / 2.0
#   d.autoscale = True
#   d.bounds = frame()
#   ll_pos = vector(ll_pos)
#   corners = [ll_pos,
#              ll_pos + vector(    0, height),
#              ll_pos + vector(width, height),
#              ll_pos + vector(width,      0),
#              ll_pos]
#   c = curve(frame = d.bounds, radius = 0, color = color.white, pos = corners)
#   d.autoscale = False
#   c.visible = visible_bounds
#   return d

# while True:
#     rate(30)
#     ev = scene.waitfor('click keydown')
#     if ev.event == 'click':
#         loc = ev.pos
#         box(pos=loc, length=box_unit_size, height=box_unit_size, width=1, color=color.green)
#         print('You clicked at', ev.pos)
#     else:
#         print('You pressed key ' + ev.key)
