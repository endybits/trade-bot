import os

import openai
from openai.error import InvalidRequestError

from app.utils.prompts import few_shot_code_to_chart_template, few_shot_code_to_chart_template_alternative
from app.utils.upload_chart import uploadFileToS3

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
    file_dict = {'filename': None, 'path': None} # This dict will be full in the AI-generated code.
    try:
        few_shot_template = few_shot_code_to_chart_template(
                                user_question,
                                sql_query,
                                db_data
                            )
        python_code = create_chart_base_code(few_shot_template)
        print("\n\n")
        print(python_code)
        exec(python_code)
        if file_dict['filename'] and file_dict['path']:
            print(file_dict)
            chart_url = uploadFileToS3(path=file_dict['path'], filename=file_dict['filename'])
            return chart_url
    except InvalidRequestError as e:
        print("CALLING ALTERNATIVE PROMPT TEMPLATE")
        few_shot_template = few_shot_code_to_chart_template_alternative(
                                user_question,
                                sql_query,
                                db_data
                            )
        python_code = create_chart_base_code(few_shot_template)
        print("\n\n")
        print(python_code)
        exec(python_code)
    

#make_chart()