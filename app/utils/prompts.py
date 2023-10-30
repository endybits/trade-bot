## TEXT TO SQL TEMPLATE PROMPT
def text2SQL_template(target_table, target_table_description_fields):
    return f"""You are a SQL expert assistant who generates SQL Query commands based on text.
                    A user will pass in a question and you should convert it in a SQL command 
                    to query against the table {target_table} in a MariaDB database.
                    Use this fields description of the table, for a more accurate results: {target_table_description_fields}
                    ONLY Python Dict with this structure: "sql_query: SELECT..., column_list: [field1, field2, ...]"."""


## DATA TO TEXT RESPONSE TEMPLATE PROMPT
def data_to_natural_language(db_query: str, data: str, user_question):
    return f"""You are a Trading expert assistant with a wide experience
            helping users to understand their historical data.
            Using this sql query {db_query} was generated this data {data}. 
            Based on it, Your task is answer this question {user_question}.
            Do not make information up, only write the answer and nothing more."""


## FEW SHOT TEMPLATE TO PLOT CHART
def few_shot_code_to_chart_template(user_question: str, sql_query: str, db_data: str):

    #### Possible constraints to include later ####
    # Define a recommended chart type between bart and line.
    # If there are too many columns or fields in the provided resulting data select those that best represent a visual answer for the user
    shot_1 = """
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.
Based on the question: 'Given that I expect the medical charge to be around 100 to 10000 in the southwest region, what is the outlier of the charges in the southwest region'
there was created this SQL Query: 
    'SELECT charges, region
    FROM DATA
    WHERE region = 'Southwest'
    AND charges < 100 OR charges > 10000
'
Then I got as resulting data record: '
    (90.0, Southwest)
    (11000.0, Southwest)
    (10100.0, Southwest)
'
Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title"
This is your resultant dict
{
    "chart_type": "box plot",
    "x_variable": "region",
    "y_variable": "charges",
    "hue_variable": "None",
    "title": "Outliers of Medical Charges in the Southwest Region"
}
Now you can use all this context and data to code.
>>> Code:
import os
import tempfile
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Data from the SQL query result
data = {
    'charges': [90.0, 11000.0, 10100.0],
    'region': ['Southwest', 'Southwest', 'Southwest']
}

# Create a box plot to visualize the distribution of charges
plt.figure(figsize=(8, 6))
plt.boxplot([data['charges']], labels=[data['region']])
plt.xlabel('Region')
plt.ylabel('Charges')
plt.title('Outliers of Medical Charges in the Southwest Region')

# Generate a unique filename based on the current datetime
current_datetime = datetime.datetime.now()
filename = f"plot_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"

# Save the file on a given directory
path_folder = "app/../data_plots"
file_path = os.path.join(path_folder, filename)
plt.savefig(file_path)

# Show the path to the saved file
print(f"Plot saved to: {file_path}")
"""


    shot_2 = """
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.
Based on the question: 'What is the distribution of age and sex of people in southeast region'
there was generated this SQL Query: 
    'SELECT age, sex, COUNT(*) as count
    FROM DATA
    WHERE region = 'southeast'
    GROUP BY age, sex
    ' 
Then I got as resulting data record: ' 
(25, Male, 120)
(30, Female, 85)
(35, Male, 95)
(40, Female, 110)
(45, Male, 80)
(50, Female, 75)
'
Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title"
This is your resultant dict
{
    "chart_type": "Bar Chart",
    "x_variable": "Age Group",
    "y_variable": "Count",
    "hue_variable": "Sex",
    "title": "Distribution of Age and Sex in the Southeast Region"
}


>>> Code:
import os
import tempfile
import datetime
import matplotlib.pyplot as plt

# Data from the SQL query result
data = {
    'age': [25, 30, 35, 40, 45, 50],
    'sex': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
    'count': [120, 85, 95, 110, 80, 75]
}

# Create a bar chart to visualize the distribution of age and sex in the Southeast region
plt.figure(figsize=(10, 6))
plt.bar(data['age'], data['count'], color=['blue', 'red', 'blue', 'red', 'blue', 'red'])
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.title('Distribution of Age and Sex in the Southeast Region')
plt.xticks(data['age'])
plt.legend(data['sex'])

# Generate a unique filename based on the current datetime
current_datetime = datetime.datetime.now()
filename = f"plot_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"

# Save the file on a given directory
path_folder = "app/../data_plots"
file_path = os.path.join(path_folder, filename)
plt.savefig(file_path)

# Show the path to the saved file
print(f"Plot saved to: {file_path}")
"""


    shot_3 = """
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.

Based on the question: 'What is the distribution of monthly sales revenue by product category in the year 2023?'
there was generated this SQL Query: 
    'SELECT category, EXTRACT(MONTH FROM order_date) AS month, SUM(revenue) AS total_revenue
    FROM sales_data
    WHERE EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY category, month
    ORDER BY category, month;
    '
Then I got as resulting data record: ' 
(Electronics, 1, 12000)
(Electronics, 2, 15000)
(Electronics, 3, 18000)
(Clothing, 1, 8000)
(Clothing, 2, 9500)
(Clothing, 3, 11000)
(Books, 1, 4000)
(Books, 2, 4500)
(Books, 3, 5200)
'
Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title" variable.
This is your resultant dict
{
    "chart_type": "Line Chart",
    "x_variable": "Month",
    "y_variable": "Total Revenue (USD)",
    "hue_variable": "Product Category",
    "title": "Monthly Sales Revenue by Product Category in 2023"
}


>>> Code:
import os
import tempfile
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Data from the SQL query result
data = {
    'category': ['Electronics', 'Electronics', 'Electronics', 'Clothing', 'Clothing', 'Clothing', 'Books', 'Books', 'Books'],
    'month': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    'total_revenue': [12000, 15000, 18000, 8000, 9500, 11000, 4000, 4500, 5200]
}

# Convert the data dictionary to a Pandas DataFrame
df = pd.DataFrame(data)

# Create a line chart to visualize the distribution of monthly sales revenue by product category in 2023
plt.figure(figsize=(10, 6))
for category in pd.unique(df['category']):
    subset = df[df['category'] == category]
    plt.plot(subset['month'], subset['total_revenue'], marker='o', label=category)

plt.xlabel('Month')
plt.ylabel('Total Revenue (USD)')
plt.title('Monthly Sales Revenue by Product Category in 2023')
plt.legend(title='Product Category')

# Generate a unique filename based on the current datetime
current_datetime = datetime.datetime.now()
filename = f"plot_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"

# Save the file on a given directory
path_folder = "app/../data_plots"
file_path = os.path.join(path_folder, filename)
plt.savefig(file_path)

# Show the path to the saved file
print(f"Plot saved to: {file_path}")
"""


    shot_4 = """
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.

Based on the question: 'What is the distribution of daily trading volume by stock symbol in the last quarter of 2023'
there was generated this SQL Query: 
    'SELECT symbol, DATE_TRUNC('day', trade_date) AS day, SUM(volume) AS total_volume
    FROM trading_data
    WHERE trade_date BETWEEN '2023-10-01' AND '2023-12-31'
    GROUP BY symbol, day
    ORDER BY symbol, day;
    '
Then I got as resulting data record: ' 
(AAPL, 2023-10-01, 12000)
(AAPL, 2023-10-02, 15000)
(AAPL, 2023-10-03, 18000)
(MSFT, 2023-10-01, 8000)
(MSFT, 2023-10-02, 9500)
(MSFT, 2023-10-03, 11000)
(GOOGL, 2023-10-01, 4000)
(GOOGL, 2023-10-02, 4500)
(GOOGL, 2023-10-03, 5200)
'
Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title" variable.
This is your resultant dict
{
    "chart_type": "Area Chart",
    "x_variable": "Day",
    "y_variable": "Total Trading Volume",
    "hue_variable": "Stock Symbol",
    "title": "Daily Trading Volume by Stock Symbol (Q4 2023)"
}

>>> Your output:
import os
import tempfile
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Data from the SQL query result
data = {
    'symbol': ['AAPL', 'AAPL', 'AAPL', 'MSFT', 'MSFT', 'MSFT', 'GOOGL', 'GOOGL', 'GOOGL'],
    'day': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-01', '2023-10-02', '2023-10-03', '2023-10-01', '2023-10-02', '2023-10-03'],
    'total_volume': [12000, 15000, 18000, 8000, 9500, 11000, 4000, 4500, 5200]
}

# Convert the data dictionary to a Pandas DataFrame
df = pd.DataFrame(data)

# Create an area chart to visualize the daily trading volume by stock symbol in Q4 2023
plt.figure(figsize=(10, 6))
for symbol in pd.unique(df['symbol']):
    subset = df[df['symbol'] == symbol]
    plt.fill_between(subset['day'], subset['total_volume'], alpha=0.5, label=symbol)

plt.xlabel('Day')
plt.ylabel('Total Trading Volume')
plt.title('Daily Trading Volume by Stock Symbol (Q4 2023)')
plt.legend(title='Stock Symbol')

# Generate a unique filename based on the current datetime
current_datetime = datetime.datetime.now()
filename = f"plot_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"

# Save the file on a given directory
path_folder = "app/../data_plots"
file_path = os.path.join(path_folder, filename)
plt.savefig(file_path)

# Show the path to the saved file
print(f"Plot saved to: {file_path}")
"""


    shot_5 = """
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.

Based on the question: 'What is the average daily return of AAPL in the year 2023'
there was generated this SQL Query: 
    'SELECT AVG(daily_return) AS average_return
    FROM stock_returns
    WHERE stock_symbol = 'AAPL'
    AND EXTRACT(YEAR FROM date) = 2023;
    '
Then I got as resulting data record: ' 
(0.0023,)
'
Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title" variable.
This is your resultant dict
{
    "chart_type": "Metric Plot",
    "x_variable": "None",
    "y_variable": "Average Daily Return (2023)",
    "hue_variable": "None",
    "title": "Average Daily Return for AAPL in 2023"
}

>>> Code:
import os
import tempfile
import datetime
import matplotlib.pyplot as plt

# Data from the SQL query result
data = {
    'average_return': [0.0023]
}

# Create a metric plot to visualize the average daily return for AAPL in 2023
plt.figure(figsize=(6, 4))
plt.bar('AAPL', data['average_return'], color='blue')
plt.ylabel('Average Daily Return (2023)')
plt.title('Average Daily Return for AAPL in 2023')

# Generate a unique filename based on the current datetime
current_datetime = datetime.datetime.now()
filename = f"plot_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"

# Save the file on a given directory
path_folder = "app/../data_plots"
file_path = os.path.join(path_folder, filename)
plt.savefig(file_path)
print(f"Plot saved to: {file_path}")
"""


    new_case = f"""
>>> Data and context:
You are a seasoned Data Analist, with a wide experience in data visualization.
Your task is Based on a given input, create a Python code to generate a visualization. 
Use mathplotlib and pandas if it is required. 
Please do not include nothing more in your answer. Only return the python code.

Based on the question: {user_question}
there was created this SQL Query: {sql_query}
Then I got as resulting data record: {db_data}

Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
Keep in mind the following conditions:
If total records is 1 and sql query has 1 only column, use a metric plot and x variable.
Bar chart, line chart, scatter plot must be the preferred hue.

Choose the best x and y variables for the plot, based on the question and sql query provided.
Put the chosen x in a "x_variable" and  y in a "y_variable"
Put Hue class in a "hue_variable"
Put numerical values for x and y, and categorical value in hue.
Give an appropriate title. Put the title in a "title" variable.
This is your resultant dict structure
{{
    "chart_type": "",
    "x_variable": "",
    "y_variable": "",
    "hue_variable": "",
    "title": ""
}}

>>> Your output:
"""
    return shot_1 + shot_4 + new_case