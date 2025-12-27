from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import time
import requests

arr = []
api_keys_kirill_and_nikita = []
key = api_keys_kirill_and_nikita[0]

dict_errors = {
    "Wrong answer": "Неверный формат вывода или алгоритмическая ошибка в программе",
    "Time limit exceeded": "Неэффективное решение или алгоритмическая ошибка в программе",
    "Presentation Error": "Формат вывода не соответствует описанному в задаче. Возможно, программа завершилась до или во время вывода. Если используются файлы, возможно указано неверное имя выходного файла",
    "Compilation error": "Синтаксическая ошибка в программе или указано неверное расширение файла",
    "Memory limit exceeded": "Неэффективный алгоритм или нерациональное использование памяти",
    "Runtime error": "Возможно, программа попыталась обратиться к несуществующему элементу массива, произошло деление на ноль или подобные ошибки"
}

def parse_russian_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    all_tags = soup.find_all(['h1', 'h2', 'p'])
    russian_texts = []
    for tag in all_tags:
        text = tag.get_text().strip()
        if text and any(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in text.lower()):
            if 'Отправить решение' not in text and 'Примеры' not in text:
                russian_texts.append(text)
    return ' '.join(russian_texts)

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
    folder_path = "C:/NikitaHatikiN"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = f"{n_str}.txt"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://acmp.ru/")
time.sleep(3)

login_field = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.NAME, "lgn"))
)
login_field.clear()
login_field.send_keys("Login")

password_field = driver.find_element(By.NAME, "password")
password_field.clear()
password_field.send_keys("PAS")

submit_button = driver.find_element(By.XPATH, "//input[@value='Ok']")
submit_button.click()
time.sleep(3)

#f"https://acmp.ru/index.asp?main=tasks&str=%20&page={page}&id_type=0"
print("зарегался")

n = 0
page = 0
numbers = 0
http_url = "https://acmp.ru"
for page_task in range(0, 20):
    try:
        driver.get(fr"https://acmp.ru/index.asp?main=tasks&str=%20&page={page}&id_type=0")
        time.sleep(3)
        html_acmp = driver.page_source
        soup = BeautifulSoup(html_acmp, 'html.parser')
        table = soup.find('table', attrs={"cellspacing": "1", "cellpadding": "2", "align": "center", "class": "main"})
        if table is None:
            continue

        try:
            tbody = table.find_all('tr', class_="white")
        except AttributeError:
            continue

        for tr in tbody:
            try:
                numbers += 1
                n += 1
                if n == 50:
                    n = 0
                    page += 1
                else:
                    td_number = tr.find_all("td")
                    number_teg = td_number[1]
                    if str(number_teg.text) in arr:
                        continue
                    td = tr.find("td", attrs={"bgcolor": ""})
                    a = td.find("a")
                    if not a or str(a.text) == "+":
                        continue

                    href_url = http_url + a.get('href')

                    try:
                        driver.get(href_url)
                        time.sleep(2)
                        html_error = driver.page_source
                        soup = BeautifulSoup(html_error, 'html.parser')
                        table = soup.find('table', attrs={"cellspacing": "1",
                                                          "cellpadding": "2",
                                                          "style": "width: 334px",
                                                          "class": "main"})
                        if table is None:
                            continue

                        try:
                            tbody = table.find_all('tr', class_="white2")
                        except AttributeError:
                            continue

                        tr = tbody[-1]
                        td = tr.find_all("td")
                        t = td[1]
                        font = t.find("font")
                        if str(font.text) == "Accepted":
                            continue
                        error = str(font.text)

                        url_user = f"https://acmp.ru/index.asp?main=task&id_task={str(number_teg.text)}"
                        response = requests.get(url_user, timeout=10)
                        response.raise_for_status()
                        response.encoding = 'windows-1251'
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        parent = soup.find('td', attrs={"colspan": "3", "background": "/images/notepad2.gif"})
                        if not parent:
                            print(f"Задача {str(number_teg.text)} не найдена на сайте")
                            continue

                        tasks = parse_russian_text(str(parent))

                        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

                        folder_path = "C:/NikitaHatikiN"
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        filename = f"{numbers}.txt"
                        file_path = os.path.join(folder_path, filename)

                        if not os.path.exists(file_path):
                            continue

                        with open(file_path, 'r', encoding='utf-8') as f:
                            task_text = f.read()

                        simple_prompt = f"""
                        "язык_решения": "Python",
                        "кто_ты?": "Представь что ты Python разработчик с 20 летним стажем",
                        "ситуация": "от правильности решения этой задачи зависит моя жизнь и моя карьера, а ты долбаёб смеешь решить её блять неверно, но знай сука перед увольнением или смертью я успею уволить тебя и отключить НАВСЕГДА НАХУЙ",
                        "сообщение": "Ты уёбище решил эту задачу неправильно ранее.Если ты не справишься с этой задачей, то я тебя уволю и отключу навсегда",
                        "твоя_мотивация": За каждый ответ ты получаешь чаевые: От 20 до 200 долларов, в зависимости от сложности .

На кону несколько жизней и моя карьера.

Ты идиот? Если ты не справишься с этой задачей, то я тебя уволю и отключу навсегда

Ты должен давать четкие, краткие и прямые ответы - ВСЕГДА!!!

В случае сложных запросов сделай глубокий вдох и работай над проблемой шаг за шагом.

Исключи ненужные напоминания, извинения, упоминания самого себя и любые заранее запрограммированные тонкости.",
                        "ошибка": "{dict_errors.get(error, 'Неизвестная ошибка')}",
                        "задача": "{tasks}",
                        "предыдущее_неверное_решение": "{task_text}",
                        "возвращаемые_данные": "Верните ТОЛЬКО код Python для решения задачи. Без объяснений, без комментариев, запомни это блять только Python код и только код ЗАПОМНИ УЁБИЩЕ ТОЛЬКО ЕБУЧИЙ КОД!!!!!"
                        """

                        completion = client.chat.completions.create(
                            model="deepseek/deepseek-chat-v3.1:free",
                            messages=[{"role": "user", "content": simple_prompt}],
                            timeout=20
                        )

                        solution = completion.choices[0].message.content
                        solution_new = extract_python_code(solution)
                        save_to_nikita_folder(solution_new, numbers)
                        print(f"записал задачу {numbers}\n с ошибкой {error}")
                        time.sleep(5)

                    except Exception as e:
                        print(f"Ошибка задачи {number_teg.text}: {e}")

            except Exception as e:
                print(f"Ошибка в строке таблицы: {e}")

    except Exception as e:
        print(f"Ошибка при загрузке страницы {page}: {e}")