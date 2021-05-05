import numpy as np


class Cursor:
    def __init__(self, line, button):
        self.line = line
        self.button = button
        self.press = None
        if self.line.get_xdata()[0] == self.line.get_xdata()[1]:
            self.orient = 'v'
        elif self.line.get_ydata()[0] == self.line.get_ydata()[1]:
            self.orient = 'h'
        self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes:
            return
        if event.button != 1:
            return
        if self.button.color != '#ec1c24':
            return

        if self.orient == 'v':
            if np.abs(event.xdata - self.line.get_xdata()[0]) > 0.05:
                return
            self.press = self.line.get_xdata()[0], event.xdata
        elif self.orient == 'h':
            if np.abs(event.ydata - self.line.get_ydata()[0]) > 0.05:
                return
            self.press = self.line.get_ydata()[0], event.ydata

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.line.axes:
            return
        if self.orient == 'v':
            x0, xpress = self.press
            dx = event.xdata - xpress
            self.line.set_xdata([x0 + dx, x0 + dx])

            self.line.figure.canvas.draw()
        elif self.orient == 'h':
            y0, ypress = self.press
            dy = event.ydata - ypress
            self.line.set_ydata([y0 + dy, y0 + dy])

            self.line.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.line.figure.canvas.draw()
