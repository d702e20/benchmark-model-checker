import pandas as pd
import matplotlib as plt
import seaborn as sns

sns.set_theme()
sns.set_context("poster")

# read csv file
raw = pd.read_csv('suite.csv-2023-06-26_14-14.csv', sep=',', skipinitialspace=True)

data = raw.groupby('name')

# plot the data
#plot = data.plot(kind='bar', x='name', y='time_s', title='Suite')

# show the plot
#plt.pyplot.show()

#sns.pairplot(raw, hue="name")

#sns.catplot(data=raw, x="name", y="time_s", hue="name", kind="bar", height=6, aspect=2)
sns.scatterplot(data=raw, x="threads", y="time_s", hue="name", legend=False, s=100)
plt.pyplot.show()

pass