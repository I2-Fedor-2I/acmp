import requests
import json
import os
from bs4 import BeautifulSoup

arr = []

def zaebota(response):
    """Ищет путь к решениб задачи в JSON"""
    response_data = response.json()
    if "response" in response_data:
        response_content = response_data["response"]
        if isinstance(response_content, str):
            try:
                parsed_response = json.loads(response_content)
                if "content" in parsed_response:
                    return parsed_response["content"]
                else:
                    return parsed_response["response"]["content"]
            except json.JSONDecodeError:
                return response_content
        else:
            if "content" in response_content:
                return response_content["content"]
            else:
                return response_content["response"]["content"]
    else:
        return response_data["content"]

def extract_python_code(text):
    """Извлекает Python код из текста, убирая объяснения"""
    if text.strip().startswith(('def ', 'class ', 'import ', 'from ', 'with ', 'if __name__')):
        return text

    if '```python' in text:
        start = text.find('```python') + 9
        end = text.find('```', start)
        if end != -1:
            return text[start:end].strip()

    elif '```' in text:
        start = text.find('```') + 3
        end = text.find('```', start)
        if end != -1:
            return text[start:end].strip()

    lines = text.split('\n')
    code_lines = []
    in_code = False

    for line in lines:
        if any(keyword in line for keyword in ['def ', 'import ', 'class ', 'print(', 'return ', ' = ']):
            in_code = True
        if in_code and line.strip() and not line.strip().startswith(('#', '"', "'")):
            code_lines.append(line)

    return '\n'.join(code_lines) if code_lines else text

def save_to_nikita_folder(content, n_str):
    """Сэйв контента в папке на диске С"""
    folder_path = "C:/NikitaHatikiN"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{n_str}.txt"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return file_path

def parse_russian_text(html_content):
    """Выбирает только условие заданий на сайте acmd.ru"""
    soup = BeautifulSoup(html_content, 'html.parser')

    all_tags = soup.find_all(['h1', 'h2', 'p'])
    russian_texts = []

    for tag in all_tags:
        text = tag.get_text().strip()
        if text and any(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in text.lower()):
            if 'Отправить решение' not in text and 'Примеры' not in text:
                russian_texts.append(text)

    return ' '.join(russian_texts)

#промт для ламы
simple_prompt = '''Return ONLY Python code to solve the problem. No explanations, no comments.

Problem: {task}

Code:'''

for n_str in range(101, 202):
    if str(n_str) in arr:
        continue

    try:
        url_user = f"https://acmp.ru/index.asp?main=task&id_task={n_str}"
        response = requests.get(url_user)
        response.encoding = 'windows-1251'
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        parent = soup.find('td', attrs={"colspan": "3", "background": "/images/notepad2.gif"})

        if not parent:
            continue

        tasks = parse_russian_text(str(parent))

        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}

        data = {
            "model": "deepseek-coder:33b",
            "prompt": simple_prompt.format(task=tasks),
            "stream": False
        }

        response = requests.post(url, headers=headers, json=data)
        res = zaebota(response)

        clean_code = extract_python_code(res)

        save_to_nikita_folder(clean_code, n_str)
        print(f"Задача {n_str} обработана успешно")

    except Exception as e:
        print(f"Ошибка в задаче {n_str}: {e}")
        continue