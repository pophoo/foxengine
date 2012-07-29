

用于根据回测结果画图

1. 确定使用matplotlib, 简单而且文档齐全

2. K线有函数直接支持
matplotlib.finance.candlestick,candlestick2
只需要对它做小改动即可

例子:
http://matplotlib.sourceforge.net/examples/pylab_examples/finance_demo.html

其中plot_day_summary是ohlc线
candlestick,candlestick2均为K线
选择使用candlestick2
