import os
import re

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
#model_list = openai.Model.list()


def gpt_chart_format(base_prompt: str):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=base_prompt,
        temperature=0.01,
        max_tokens=200
    )
    return response.choices[0]['text']


# Create prompt to extract
def create_prompt_text2chart(
        #question: str, sql_query: str, data: str
        ):
    
    # Few shot technique
    few_shot_prompt = f"""
        >>> Data context:
        Based on the question: 'which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day'
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
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
        <chart_start>box plot<chart_end>
        <x_var_start>region<x_var_end>
        <y_var_start>charges<y_var_end>
        <hue_var_start>None<hue_var_end>
        <title_start>Outliers of Medical Charges in the Southwest Region<title_end>


        >>> Data context:
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
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
        <chart_start>Bar Chart<chart_end>
        <x_var_start>Age Group<x_var_end>
        <y_var_start>Count<y_var_end>
        <hue_var_start>Sex<hue_var_end>
        <title_start>Distribution of Age and Sex in the Southeast Region<title_end>


        >>> Data context:
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
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
        <chart_start>Line Chart<chart_end>
        <x_var_start>Month<x_var_end>
        <y_var_start>Total Revenue (USD)<y_var_end>
        <hue_var_start>Product Category<hue_var_end>
        <title_start>Monthly Sales Revenue by Product Category in 2023<title_end>


        >>> Data context:
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
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
        <chart_start>Area Chart<chart_end>
        <x_var_start>Day<x_var_end>
        <y_var_start>Total Trading Volume<y_var_end>
        <hue_var_start>Stock Symbol<hue_var_end>
        <title_start>Daily Trading Volume by Stock Symbol (Q4 2023)<title_end>


        >>> Data context:
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
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
        <chart_start>Metric Plot<chart_end>
        <x_var_start>None<x_var_end>
        <y_var_start>Average Daily Return (2023)<y_var_end>
        <hue_var_start>None<hue_var_end>
        <title_start>Average Daily Return for AAPL in 2023<title_end>

        
        >>> Data context:
        Based on the question: 'which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day'
        there was created this SQL Query: 'SELECT HOUR(open_datetime) AS hour_of_day, SUM(gross_total_return_on_trade) AS pnl
        FROM trade_history_agg
        WHERE user_id = 3
        AND DAYOFWEEK(open_datetime) = 3
        AND YEAR(open_datetime) = 2023
        GROUP BY hour_of_day
        ORDER BY pnl DESC;
        '
        Then I got as resulting data record: ' (10, 8270.5)
        (12, 1193.5)
        (11, 1028.0)
        (15, 960.0)
        (0, 0.0)
        (2, -1643.0)
        '

        Recommend me a graph that can be used to best represent the question, the sql generated, and the resulting data.
        Keep in mind the following conditions:
        If total records is 1 and sql query has 1 column, recommend metric plot and recommended x variable.
        Put the recommended chart in the tag "<chart_start>" and end with "<chart_end>".
        Bar chart, scatter plot, swarm plot must have recommended hue.
        Recommend the x and y variables for the plot, based on the question and sql query provided.
        Put the recommend x between the tags "<x_var_start>" and "<x_var_end>" and y between the tags "<y_var_start>" and "<y_var_end>".
        Put Hue class between the tags "<hue_var_start>" and "<hue_var_end>"
        Put numerical values for x and y, and categorical value in hue.
        Give an appropriate title. Put the title between the tags between the tags "<title_start>" and "<title_end>"

        >>> Your output:
    
        """
    resp_chart_format: str
    resp_chart_format = gpt_chart_format(few_shot_prompt)
    
    ## Parse GPT Response
    try:
        chart_recommendation = re.search(r"<chart_start>(.*)<chart_end>", resp_chart_format.replace('\n', ' ')).group(1).strip()
        x_recommendation = re.search(r"<x_var_start>(.*)<x_var_end>", resp_chart_format.replace('\n', ' ')).group(1).strip()
        y_recommendation = re.search(r"<y_var_start>(.*)<y_var_end>", resp_chart_format.replace('\n', ' ')).group(1).strip()
        hue_recommendation = re.search(r"<hue_var_start>(.*)<hue_var_end>", resp_chart_format.replace('\n', ' ')).group(1).strip()
        title_recommendation = re.search(r"<title_start>(.*)<title_end>", resp_chart_format.replace('\n', ' ')).group(1).strip()
    except:
        chart_recommendation = None
        x_recommendation = None
        y_recommendation = None
        hue_recommendation = None
        title_recommendation = None
    print(chart_recommendation, x_recommendation, y_recommendation, hue_recommendation, title_recommendation, sep='\n')
    json_chart_structure = {
        'chart_type': chart_recommendation.lower(),
        'x_axis': x_recommendation,
        'y_axis': y_recommendation,
        'hue_variable': hue_recommendation,
        'chart_title': title_recommendation
    }
    return json_chart_structure


## https://github.com/thongekchakrit/ChartAI/blob/main/Home.py
def create_chart():
    json_chart_structure = create_prompt_text2chart()
    chart_type = json_chart_structure.get('chart_type')
    if not chart_type is None: 
        print(chart_type)
        # if 'pie' in chart_type:
        #     width = 4
        #     height = 2


create_chart()






## Plotting - Guide Home.py 458