import matplotlib.pyplot as plt


def bar_graph(df):
    df.groupby('labels').labels.count().plot.bar(ylim=0)
    plt.show()
