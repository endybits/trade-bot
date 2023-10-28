import sys
y = 12
output = """
x = 10
#y = 11
print(x + y)
"""
exec(output)
#eval(output)

import matplotlib.pyplot as plt

# Data from the SQL query result
data = {
    'hour_of_day': [10, 12, 11, 15, 0, 2],
    'pnl': [8270.5, 1193.5, 1028.0, 960.0, 0.0, -1643.0]
}

# Create a bar chart to visualize the best hour of the day to trade on Tuesday in 2023
plt.figure(figsize=(8, 6))
plt.bar(data['hour_of_day'], data['pnl'], color='blue')
plt.xlabel('Hour of Day')
plt.ylabel('PNL')
plt.title('Best Hour of the Day to Trade on Tuesday in 2023')
plt.show()