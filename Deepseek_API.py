import requests
import os
from bs4 import BeautifulSoup
from openai import OpenAI

m = 0
paka = 0

simple_prompt = '''Return ONLY Python code to solve the problem. No explanations, no comments.

Problem: {task}

Code:'''

api_keys_kirill_and_nikita = [
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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"
]

arr = ['298', '130', '461', '529', '349', '109', '401', '904', '793', '195', '65', '196', '449', '411', '89', '69', '206', '427', '387',
        '81', '997', '777', '950', '304', '462', '367', '390', '323', '291', '8', '590', '120', '71', '86', '150', '924', '961', '675',
        '938', '642', '813', '7', '96', '698', '522', '844', '159', '6', '762', '388', '380', '556', '14', '171', '941', '126', '597', '515',
        '498', '170', '99', '970', '92', '5', '347', '108', '192', '253', '628', '157', '260', '234', '215', '211', '282', '830', '51', '2',
        '430', '785', '442', '144', '328', '350', '151', '278', '172', '40', '765', '757', '357', '745', '361', '160', '859', '327', '45',
        '416', '639', '329', '578', '271', '42', '369', '276', '899', '843', '325', '516', '455', '681', '87', '38', '1', '243', '758', '908',
        '149', '48', '942', '213', '9', '214', '678', '694', '279', '30', '314', '163', '131', '858', '178', '209', '600', '535', '249',
        '501', '338', '290', '21', '54', '374', '43', '305', '422', '895', '836', '916', '189', '524', '818', '284', '32', '784', '464',
        '364', '26', '759', '564', '368', '520', '957', '869', '294', '955', '833', '815', '115', '819', '25', '966', '508', '331', '760',
        '320', '235', '643', '301', '581', '546', '496', '393', '715', '153', '125', '35', '156', '4', '264', '181', '790', '871', '579',
        '648', '905', '689', '791', '263', '424', '224', '97', '511', '188', '342', '894', '763', '317', '10', '395', '539', '23', '431',
        '634', '146', '28', '141', '100', '733', '936', '933', '906', '392', '684', '29', '145', '190', '384', '207', '944', '13', '50',
        '679', '472', '606', '134', '326', '773', '475', '60', '795', '114', '778', '996', '299', '142', '319', '297', '477', '831', '233',
        '312', '288', '46', '266', '250', '460', '324', '688', '340', '925', '975', '517', '756', '352', '653', '225', '275', '513', '466'
           , '574', '509', '311', '158', '691', '308', '876', '119', '523', '122', '332', '816', '62', '649', '711', '493', '967', '845',
        '376', '95', '262', '839', '124', '699', '84', '47', '697', '44', '510', '66', '18', '281', '481', '550', '742', '85', '228', '36',
        '61', '842', '848', '321', '892', '580', '283', '309', '296', '316', '173', '471', '370', '935', '270', '447', '59', '345', '102',
        '274', '24', '779', '820', '127', '817', '811', '289', '726', '129', '132', '683', '336', '88', '692', '82', '183', '75', '710',
        '582', '265', '897', '22', '700', '598', '703', '701', '208', '394', '629', '355', '93', '633', '147', '504', '682', '554', '258',
        '273', '3', '743', '439', '946', '846', '412', '754', '686', '136', '39', '482', '79', '984', '826', '295', '729', '780', '19',
        '792', '68', '525', '637', '245', '236', '11', '113', '330', '596', '118', '491', '457', '514', '34', '425', '441', '143', '671',
        '198', '499', '948', '680', '728', '165', '978', '348', '440', '267', '463', '269', '333', '98', '58', '200', '413', '712', '696',
        '216', '940', '52', '638', '521', '31', '803', '63', '135', '664', '479', '687', '542', '755', '518', '838', '375', '15', '766',
        '154', '128', '16', '385', '488', '872', '822', '199', '94', '140', '185', '695', '782', '218', '292', '354', '693', '465', '526',
        '519', '272', '64', '841', '764', '939', '20', '103', '531', '287', '903', '534', '947', '293', '945', '55', '676', '106', '670',
        '148', '72', '377', '33', '854', '495', '164', '544', '56', '685', '543', '907', '123', '605', '432', '231', '641']

key = api_keys_kirill_and_nikita[0]


def save_to_nikita_folder(content, n_str):
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

#++++++++
for n_str in range(110, 1001):
    print(n_str)

    if str(n_str) in arr:
        continue

    try:
        m += 1
        paka += 1

        url_user = f"https://acmp.ru/index.asp?main=task&id_task={n_str}"
        response = requests.get(url_user, timeout=10)
        response.encoding = 'windows-1251'
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        parent = soup.find('td', attrs={"colspan": "3", "background": "/images/notepad2.gif"})

        if not parent:
            continue

        if paka >= 1:
            paka = 0
            current_index = api_keys_kirill_and_nikita.index(key)
            next_index = (current_index + 1) % len(api_keys_kirill_and_nikita)
            key = api_keys_kirill_and_nikita[next_index]

        tasks = parse_russian_text(str(parent))

        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[{"role": "user", "content": simple_prompt.format(task=tasks)}],
            timeout=30
        )

        solution = completion.choices[0].message.content
        solution_new = extract_python_code(solution)
        save_to_nikita_folder(solution_new, n_str)

        print(f"Задача {n_str}")
        print(f"Всего: {m}")
        print("=" * 50)

    except Exception as e:
        print(f"Ошибка в задаче {n_str}: {e}")
        continue
