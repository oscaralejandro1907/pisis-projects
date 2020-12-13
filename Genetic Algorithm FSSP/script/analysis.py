import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#df = pd.read_csv("results_large2.csv",skiprows=0,skip_blank_lines=True)

#bplot=sns.boxplot(x='nxm', y = 'GAP', data=df)

results = pd.read_csv("results.csv",skiprows=0,skip_blank_lines=True)

#splot=sns.scatterplot(x='GAP', y = 'ExecutionTime', hue='Group',data=results)

b=sns.boxplot(x='Group', y = 'GAP', data=results)

plt.show()