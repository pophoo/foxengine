# -*-coding:utf-8 -*-

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.colors import colorConverter
from matplotlib.collections import LineCollection, PolyCollection

def candlestick(ax, quotes, width=0.2, colorup='red', colordown='cyan',
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
    uface_color = 'black'
    for q in quotes:
        t, open, close, high, low = q[:5]

        if close>=open :
            color = colorup
            face_color = uface_color
            lower = open
            height = close-open
        else           :
            color = colordown
            face_color = color
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
            facecolor = face_color,
            edgecolor = color,
            )
        rect.set_alpha(alpha)


        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches


def candlestick2(ax, opens, closes, highs, lows, width=1,
                 colorup='red', colordown='cyan',
                 #alpha=0.75,
                 alpha=1,
                ):
    """
    根据matplotlib.finance.candlestick2修改

    Represent the open, close as a bar line and high low range as a
    vertical line.


    ax          : an Axes instance to plot to
    width       : the bar width in points
    colorup     : the color of the lines where close >= open
    colordown   : the color of the lines where close <  open
    alpha       : bar transparency

    return value is lineCollection, barCollection
    """

    # note this code assumes if any value open, close, low, high is
    # missing they all are missing

    delta = width/2.
    barVerts = [ ( (i-delta, open), (i-delta, close), (i+delta, close), (i+delta, open) ) for i, open, close in zip(xrange(len(opens)), opens, closes) if open != -1 and close!=-1 ]

    rangeSegments = [ ((i, low), (i, high)) for i, low, high in zip(xrange(len(lows)), lows, highs) if low != -1 ]



    r,g,b = colorConverter.to_rgb(colorup)
    colorup = r,g,b,alpha
    r,g,b = colorConverter.to_rgb(colordown)
    colordown = r,g,b,alpha
    colord = { True :  colorup,
               False : colordown,
               }
    r,g,b = colorConverter.to_rgb('black')
    fcolorup = r,g,b,alpha
    fcolord = { True : fcolorup,
               False : colordown,
            }
    colors = [colord[open<close] for open, close in zip(opens, closes) if open!=-1 and close !=-1]
    fcolors = [fcolord[open<close] for open, close in zip(opens, closes) if open!=-1 and close !=-1]


    assert(len(barVerts)==len(rangeSegments))

    useAA = 0,  # use tuple here
    lw = 0.5,   # and here
    rangeCollection = LineCollection(rangeSegments,
                                     #colors       = ( (0,0,0,1), ),
                                     colors = colors,
                                     linewidths   = lw,
                                     antialiaseds = useAA,
                                     )


    barCollection = PolyCollection(barVerts,
                                   facecolors   = fcolors,
                                   #edgecolors   = ( (0,0,0,1), ),
                                   edgecolors   = colors,
                                   antialiaseds = useAA,
                                   linewidths   = lw,
                                   )

    minx, maxx = 0, len(rangeSegments)
    miny = min([low for low in lows if low !=-1])
    maxy = max([high for high in highs if high != -1])

    corners = (minx, miny), (maxx, maxy)
    ax.update_datalim(corners)
    ax.autoscale_view()

    # add these last
    ax.add_collection(rangeCollection)
    ax.add_collection(barCollection)
    rangeCollection.set(zorder=1)    
    barCollection.set(zorder=2) #bar要覆盖掉range,避免range的线条颜色在bar中显示
    return rangeCollection, barCollection
