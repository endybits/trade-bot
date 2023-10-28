import os
import re

import openai

from app.utils.prompts import get_few_shot_chart, get_few_shot_code_chart

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

def gpt_generate_chart_code(base_prompt: str):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=base_prompt,
        temperature=0.01,
        max_tokens=1000
    )
    return response.choices[0]['text']


# Create prompt to extract
def create_prompt_text2chart(
        #question: str, sql_query: str, data: str
        ):
    
    # Few shot technique
    few_shot_prompt = get_few_shot_chart()
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


#create_chart()
## Plotting - Guide Home.py 458



def create_chart_base_code( prompt: str):
    print(prompt)
    python_code_str = gpt_generate_chart_code(prompt)
    return python_code_str


python_code = create_chart_base_code(get_few_shot_code_chart())
print(python_code)