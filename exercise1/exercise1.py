from math import sin, pi, exp
from matplotlib import pyplot as plt
import numpy as np
REFRESH_RATE = 0.01  # Time to wait for window inputs inbetween drawing. In seconds.

class FunctionPlotter:
    """
    Abstract class representing a generic plotting window of a function
    param 'function': lambda function to be drawn, must take one variable only
    param 'resolution': The resolution to draw. Not measured in any specific unit.
    param 'borders': The initial borders of the plot window ((x_min,x_max), (y_min, y_max)) 
    """
    def __init__(self, function, resolution=300, borders=((0,1),(0,1))):
        plt.ion()  # Enable interactive mode

        # Set member variables
        self.function = function            
        self.resolution = int(resolution)

        # Initialize figure and plot
        self.fig, self.ax = plt.subplots()
        self.plot, = self.ax.plot([borders[0][0],borders[0][1]], [borders[1][0], borders[1][1]])
        self.update()

    def update(self):
        # Infinite plot
        x,y = self.calculate_xy()
        self.plot.set_xdata(x)
        self.plot.set_ydata(y)

    def calculate_xy():
        """
        Method implemented in children. Must return two lists x and y which
        specify what points to draw on the plot.
        """
        pass

class InfinitePlot(FunctionPlotter):
    """
    An infinitely explorable plot window.
    """
    def calculate_xy(self):
        # Get limits
        x_min, x_max = self.ax.get_xlim()

        # Calculate
        x = np.linspace(x_min, x_max, self.resolution)
        y = [self.function(t) for t in x]
        return x,y

class ForwardAnimatingPlot(FunctionPlotter):
    """
    An animating plot window that draws from x=0 and forwards.
    """
    POINTS_PER_CALL = 8  # How many additional points to draw for each update() call
    x = []
    y = []
    def calculate_xy(self):
        for _ in range(self.POINTS_PER_CALL):
            # Add the point (t, function(t))
            t = len(self.x)/self.resolution
            self.x.append( t )
            self.y.append( self.function(t) )
        return self.x, self.y

class BidirectionalAnimatingPlot(FunctionPlotter):
    """
    An animated plot window that expands in both directions.
    Starts at x=0.

    NOTE    Extremely unperformant.
            Since Python's built in lists do not allow for
            insertion of element at the beginning of the list
            with O(1) time complexity. This code gets slower
            and slower the more elements are present in x and
            y.
    """
    POINTS_PER_CALL = 8  # How many additional points to draw for each update() call
    x = []
    y = []
    def calculate_xy(self):
        for _ in range(self.POINTS_PER_CALL):
            # Add the points (t, function(t)) and (-t, function(-t))
            t = len(self.x)/self.resolution
            self.x.append( t )
            self.y.append( self.function(t) )
            self.x.insert(0, -t)
            self.y.insert(0, self.function(-t))
        return self.x, self.y

def main():
    # Define function to be drawn
    function = lambda t : 3 * pi * exp( -(5*sin(2*pi*t)) )  

    # Create plots
    inf_plot = InfinitePlot(function, borders=((-1,1), (0,1400)))
    forward_anim_plot = ForwardAnimatingPlot(function, borders=((0,4), (0,1400)), resolution=300)
    bi_anim_plot = BidirectionalAnimatingPlot(function, borders=((-4,4), (0,1400)), resolution=300)

    # Draw/Interaction loop
    while True:
        inf_plot.update()
        forward_anim_plot.update()
        bi_anim_plot.update()
        plt.pause(REFRESH_RATE)

if __name__ == "__main__":
    main()