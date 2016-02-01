import time
import matplotlib
matplotlib.use('TKAgg')
import numpy
from matplotlib import pyplot
from matplotlib import animation

WAVELENGTH = 6.                 # units
PERIOD     = 3000.              # ms
VELOCITY   = WAVELENGTH/PERIOD  # units/ms
CONVERSION = 20.                # don't ask
VLINE      = 7                  # x coordinate to draw vertical reference line
DIFFERENCE = VLINE - WAVELENGTH

fig = pyplot.figure()
ax = pyplot.axes(xlim=(0, 14), ylim=(-2, 2))
wavelength_text = ax.text(0.02, 0.95, 'Wavelength = %.1f units' % WAVELENGTH, transform=ax.transAxes)
ax.axvline(VLINE, color = 'r', linestyle = '--')
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line, 

def animate(i):
    x = numpy.linspace(0, WAVELENGTH, 1000)
    x = x + DIFFERENCE + (VELOCITY * CONVERSION * i)
    if (x[0] > VLINE):
        return line,
    k = 2 * numpy.pi/WAVELENGTH
    y = numpy.sin(k * (x - DIFFERENCE - (VELOCITY * CONVERSION * i)))
    line.set_data(x, y)
    return line, 

# 50 frames per second
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int(50 * PERIOD/1000), interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('six_wavelength.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

pyplot.show()
