import time
import matplotlib
matplotlib.use('TKAgg')
import numpy
from matplotlib import pyplot
from matplotlib import animation

WAVELENGTH = 6.                 # units
PERIOD     = 5000.              # ms
VELOCITY   = WAVELENGTH/PERIOD  # units/ms
CONVERSION = 20.                # don't ask
VLINE      = 7                  # x coordinate to draw vertical reference line
DIFFERENCE = VLINE - WAVELENGTH
DT         = 1./50              # frames per second

time_elapsed  = 0.

fig = pyplot.figure()
ax = pyplot.axes(xlim=(0, 14), ylim=(-2, 2))
wavelength_text = ax.text(0.02, 0.55, 'Wavelength = %.1f units' % WAVELENGTH, transform=ax.transAxes)
period_seconds = PERIOD/1000.
period_text = ax.text(0.02, 0.50, 'Period = %.1f seconds' % period_seconds, transform=ax.transAxes)
time_text = ax.text(0.02, 0.45, '', transform=ax.transAxes)
ax.axvline(VLINE, color = 'r', linestyle = '--')
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

def animate(i):
    global time_elapsed
    time_elapsed += DT
    time_text.set_text('Time = %.1f seconds' % time_elapsed)
    x = numpy.linspace(0, WAVELENGTH, 1000)
    x = x + DIFFERENCE + (VELOCITY * CONVERSION * i)
    if (x[0] > VLINE):
        time_elapsed = 0
        return line, time_text
    k = 2 * numpy.pi/WAVELENGTH
    y = 0.6 * numpy.sin(k * (x - DIFFERENCE - (VELOCITY * CONVERSION * i)))
    line.set_data(x, y)
    return line, time_text

# 50 frames per second
t0 = time.time()
animate(0)
t1 = time.time()
interval = 1000 * DT - (t1 - t0)
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int(50 * PERIOD/1000), interval=interval, blit=True, repeat=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
anim.save('six_wl.mp4', fps=30)

pyplot.show()
