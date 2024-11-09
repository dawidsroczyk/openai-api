import os
import openai


# create description of a table
# so that it can be sent to openai model
def create_table_definition_prompt(df, table_name):

    prompt='''### sqlite SQL table, with it properties
    #
    # {}({})
    #
    '''.format(table_name, ','.join(str(col) for col in df.columns))

    return prompt


# handle user input
def user_query_input():
    
    user_input = input('Enter the info you want: ')
    return user_input


# combine user input with table description
def combine_prompts(df, table_name, query_prompt):
    definition = create_table_definition_prompt(df, table_name)
    query_init_string = f'### Write only a SQL query to answer: {query_prompt}\nSELECT'
    return definition+query_init_string


# send prompt to openai
def send_to_openai(prompt, client):

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['#', ';']
    )

    return response
