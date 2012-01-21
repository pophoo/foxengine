# -*-coding:utf-8 -*-

def candlestick(ax, quotes, width=0.2, colorup='red', colordown='blue',
                alpha=1.0):

    """
    根据matplotlib.finance.candlestick修改

    quotes is a sequence of (time, open, close, high, low, ...) sequences.
    As long as the first 5 elements are these values,
    the record can be as long as you want (eg it may store volume).

    time must be in float days format - see date2num

    Plot the time, open, close, high, low as a vertical line ranging
    from low to high.  Use a rectangular bar to represent the
    open-close span.  If close >= open, use colorup to color the bar,
    otherwise use colordown

    ax          : an Axes instance to plot to
    width       : fraction of a day for the rectangle width
    colorup     : the color of the rectangle where close >= open
    colordown   : the color of the rectangle where close <  open
    alpha       : the rectangle alpha level

    return value is lines, patches where lines is a list of lines
    added and patches is a list of the rectangle patches added

    """

    OFFSET = width/2.0

    lines = []
    patches = []
    for q in quotes:
        t, open, close, high, low = q[:5]

        if close>=open :
            color = colorup
            lower = open
            height = close-open
        else           :
            color = colordown
            lower = close
            height = open-close

        vline = Line2D(
            xdata=(t, t), ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True,
            )

        rect = Rectangle(
            xy    = (t-OFFSET, lower),
            width = width,
            height = height,
            facecolor = color,
            edgecolor = color,
            )
        rect.set_alpha(alpha)


        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches

