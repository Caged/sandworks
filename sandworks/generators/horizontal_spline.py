from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack
from numpy import array

from sand import Sand
from ..lib.sand_spline import SandSpline
from ..lib.color import hex_to_rgb_decimal


def guide_iterator(x, y):
    while True:
        yield array([[x, y]])


def generate(args):
    # Number of lines
    line_count = args.lines

    # Margin as a percent of total canvas size
    margin = 0.01

    gamma = 1.5

    # What frame to write out
    save_frame = args.save_every

    # TODO: Step.  Appears to be jitter multiplier for points along the spline
    # Causes the sand to be more "windswept" towards the later points
    step = 0.0000003 * 0.15

    # The number of points along the spline.  More points means a denser-looking spline.
    point_count = 1000

    # Convert colors to RGB decimal
    sand_color = hex_to_rgb_decimal(args.color)
    bg_color = hex_to_rgb_decimal(args.bg_color)

    # Set alpha
    sand_color.append(0.001)
    bg_color.append(1)

    sand = Sand(args.size)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    splines = []

    # For each y column
    for index, ypos in enumerate(linspace(margin, 1.0 - margin, line_count)):
        # TODO: 4?  Not sure what purpose this number serves.
        pnum = 4 + index
        guide = guide_iterator(0.5, ypos)

        x = linspace(-1, 1.0, pnum) * (1.0 - 2 * margin) * 0.5
        y = zeros(pnum, 'float')
        path = column_stack([x, y])
        scale = arange(pnum).astype('float') * step

        spline = SandSpline(guide, path, point_count, scale)
        splines.append(spline)

    j = 0
    while True:
        for s in splines:
            xy = next(s)
            sand.paint_dots(xy)
            if not j % (save_frame * line_count):
                sand.write_to_png('tmp/frame-{}.png'.format(j), gamma)
            j += 1

    # the_iterator = spline_iterator()
    # while True:
    #     try:
    #         itt, xy
    #     except Exception as e:
    #         raise
  # while True:
  #   try:
  #     itt, xy = next(si)
  #     sand.paint_dots(xy)
  #     if not itt%(500*GRID_Y):
  #       sand.write_to_png(fn.name(), GAMMA)
  #   except Exception as e:
  #     sand.write_to_png(fn.name(), GAMMA)
  #     traceback.print_exc(file=sys.stdout)
  #     itt = 0
  # while True:
  #   for s in splines:
  #     xy = next(s)
  #     itt += 1
  #     yield itt, xy
