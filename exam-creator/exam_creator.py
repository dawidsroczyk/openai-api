import time

# create dictionary where keys are
# question numbers and items
# are questions themselves
def create_student_view(test, num_questions):

    student_view = {1: ''}
    question_number = 1
    for line in test.split('\n'):
        if not line.startswith('   Correct Answer:'):
            student_view[question_number] += line + '\n'
        else:
            if question_number < num_questions:
                question_number += 1
                student_view[question_number] = ''
    return student_view


# create dictionary where keys are
# question numbers and items
# are answers to these questions
def extract_answers(test, num_questions):

    answers = {1: ''}
    question_number = 1
    for line in test.split('\n'):
        if line.startswith('   Correct Answer:'):
            answers[question_number] += line + '\n'
            if question_number < num_questions:
                question_number += 1
                answers[question_number] = ''
    return answers


# print questions to user
# and ask user to input answers
def take(student_view):
    student_answers = {}
    for question, question_view in student_view.items():
        print(question_view)
        time.sleep(0.1)
        answer = input('Enter your answer: ')
        student_answers[question] = answer
    return student_answers


# compare correct answers with student answers
# and grade the test
def grade(correct_answer_dict, student_answers):
    correct_answers = 0
    for question, answer in student_answers.items():
        if answer.upper() == correct_answer_dict[question][19].upper():
            correct_answers += 1
    grade = 100 * correct_answers / len(correct_answer_dict)
    
    if grade < 60:
        passed = 'NO PASS'
    else:
        passed = 'PASS!'
    
    return f'{correct_answers}/{len(correct_answer_dict)} correct! You got {grade} grade, {passed}'


class ExamCreator:

    def __init__(self):
        self.topic = ''
        self.num_questions = 0
        self.num_possible_answers = 0
        self.client = None
    

    # create prompt passed to openai api
    def create_test_prompt(self):

        prompt=f'Create a multiple choice quiz on the topic of {self.topic} consisting of {self.num_questions} questions. '\
            + f'Each question should have {self.num_possible_answers} options. '\
            + f'Also include the correct answer for each question using the starting string \'Correct Answer: \'. ' \
            + f'Do not add any unnecessary comments.'

        return prompt
    

    # call openai with prompt
    def call_openai(self, prompt):

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response


    # prompt openai, extract questions and answers
    def create_exam(self):

        prompt = self.create_test_prompt()
        response = self.call_openai(prompt)
        student_view = create_student_view(response.choices[0].message.content, self.num_questions)
        answers = extract_answers(response.choices[0].message.content, self.num_questions)

        return student_view, answers

