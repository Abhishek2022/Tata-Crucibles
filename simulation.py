import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

sns.set(color_codes=True)
sns.set(rc={'figure.figsize':(5,5)})

passengers_size = 200

# No. of paramters for each passenger
params_size = 4    
# Average speeds for each parameter
avg_speeds = [4.2, 3.1, 4.9, 6.5]
# Std deviation for each parameter
std_deviation = [1, 0.5, 0.7, 1.3]
# Final matrix containing passenger's info
passenger_data = []

for i in range (params_size):
    data_normal = norm.rvs(size=passengers_size, loc=avg_speeds[i], scale=std_deviation[i])
    passenger_data.append(data_normal)

ax = sns.distplot(data_normal, bins=100, kde=True, color='skyblue',hist_kws={"linewidth": 15,'alpha':1})
ax.set(xlabel='Normal Distribution', ylabel='Frequency')

# Displaying one of the parameters
plt.show()