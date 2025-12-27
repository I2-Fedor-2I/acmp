import requests
import json
import ast
import os

from astunparse import unparse
from bs4 import BeautifulSoup

arr = ['1', '2', '3', '4', '5', '6', '8', '9', '10', '13', '14', '15', '21', '22', '23', '25', '33', '35', '43', '46', '48', '52', '61', '62', '63', '66', '68', '79', '81', '86', '92', '106', '108', '119', '124', '131', '147', '148', '149', '233', '263', '264', '272', '284', '293', '297', '312', '324', '327', '349', '387', '457', '493', '499', '504', '511', '514', '529', '534', '542', '550', '579', '597', '633', '637', '643', '675', '685', '688', '692', '694', '697', '700', '754', '773', '935']
def suhoj(response):
    response_data = response.json()
    if "response" in response_data:
        response_content = response_data["response"]
        if isinstance(response_content, str):
            parsed_response = json.loads(response_content)
            if "content" in parsed_response:
                return parsed_response["content"]
            else:
                return parsed_response["response"]["content"]
        else:
            if "content" in response_content:
                return response_content["content"]
            else:
                return response_content["response"]["content"]
    else:
        return response_data["content"]
def get_code(string):
    module = ast.parse(string)

    code_lines = []
    for node in ast.walk(module):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            code_line = unparse(node).strip() + '\n'
            code_lines.append(code_line)
        elif isinstance(node, ast.Assign):
            code_line = unparse(node).strip() + '\n'
            code_lines.append(code_line)
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            code_line = unparse(node).strip() + '\n'
            code_lines.append(code_line)
        elif isinstance(node, ast.Expr):
            # Выражения: например вызовы функций без присваивания
            code_line = unparse(node).strip() + '\n'
            code_lines.append(code_line)
        # Можно добавить и другие типы узлов по необходимости

    return ''.join(code_lines)
def save_to_nikita_folder(content):
    folder_path = "C:/NikitaHatikiN"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{n_str}.txt"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return file_path
def parse_russian_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим все теги в порядке их появления в документе
    all_tags = soup.find_all(['h1', 'h2', 'p'])

    russian_texts = []

    for tag in all_tags:
        text = tag.get_text().strip()

        # Проверяем, что текст содержит русские буквы и не пустой
        if text and any(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in text.lower()):
            # Пропускаем последнюю надпись "Отправить решение"
            if 'Отправить решение' and 'Примеры' not in text:
                russian_texts.append(text)

    return ' '.join(russian_texts)


for n_str in range(101, 202):
    if str(n_str) in arr:
        pass
    else:
        url_user = f"https://acmp.ru/index.asp?main=task&id_task={n_str}"


        response = requests.get(url_user)
        response.encoding = 'windows-1251'  #'cp1251'
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        parent = soup.find('td', attrs={"colspan": "3", "background": "/images/notepad2.gif"})

        tasks = parse_russian_text(str(parent))


        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        pro_promt_content = 'Your output must follow this JSON structure: {"response": {"content": "the task solution exclusively"}}   The key "response" should contain a dictionary with only one key: "content". The value of the key "content" is a string representing the answer to the problem.'
        pro_promt_task = (f'''Solve the following problem. The problem can be from any field: programming, mathematics, algorithms, chess, etc.

Problem text:
{tasks}

Solution requirements:

If the problem requires code - write working Python code

If the problem is mathematical - provide solution with formulas

If the problem is algorithmic - describe the algorithm and implementation

Always show the final answer

Explain the logic of the solution

Start solving''')


        pro_promt_json = (f'''
        "json_structure": "{pro_promt_content}",
          "task": "{pro_promt_task}",
          "role": "You are an AI agent that solves tasks",
          "response_rules": [
            "Return only pure Python code",
            "No explanations, no comments, only code",
            "Ensure the code is executable"
          ],
          "programming_language": "Python"''')

        data = {
            "model": "deepseek-coder:33b",
            "prompt": f'{pro_promt_json}',
            "format": "json",
            "stream": False
        }

        response = requests.post(url, headers=headers, json=data)

        res = suhoj(response)
        clean = get_code(res)
        save_to_nikita_folder(clean)


