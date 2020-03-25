import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

def draw_barplot(
    data: pd.DataFrame,
    x_column: str,
    figsize: tuple,
    title=None, 
    xlabel=None, 
    ylabel=None,
    horiz=False,
    sort_by_count=False,
    get_shares=False
    ) -> plt.plot:
    """
    A generalized method to draw a barplot
    """

    # Defining the figure margins
    plt.figure(figsize=figsize)

    # Aggregating
    data = data.groupby([x_column], as_index=False).size()

    # Converting to frame
    data = data.to_frame(name='count')

    if get_shares:
        data['count'] = data['count'] * 100 /np.sum(data['count'])

    if sort_by_count:
        if horiz:
            data.sort_values('count', inplace=True)
        else:
            data.sort_values('count', inplace=True, ascending=False)  

    # Plotting
    if horiz:
        plt.barh(y=data.index, width=data['count'])
    else:
        plt.bar(x=data.index, height=data['count'])

    if title is not None:
        plt.title(title)

    if xlabel is not None:    
        plt.xlabel(xlabel)

    if ylabel is not None:        
        plt.ylabel(ylabel)

    plt.show()
