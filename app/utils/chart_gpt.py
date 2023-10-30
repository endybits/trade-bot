import os

import openai

from app.utils.prompts import few_shot_code_to_chart_template

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_generate_chart_code(base_prompt: str):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=base_prompt,
        temperature=0.01,
        max_tokens=1000
    )
    return response.choices[0]['text']


def create_chart_base_code( prompt: str):
    #print(prompt)
    python_code_str = gpt_generate_chart_code(prompt)
    return python_code_str

## TODO Dynamical data
def make_chart(user_question: str, sql_query: str, db_data: str):
    few_shot_template = few_shot_code_to_chart_template(
                            user_question,
                            sql_query,
                            db_data
                        )
    python_code = create_chart_base_code(few_shot_template)
    print(python_code)
    exec(python_code)

#make_chart()