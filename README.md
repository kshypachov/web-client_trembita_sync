# Проєкт Взаємодії з Трембітою

Цей проєкт входить в набір прикладів взаємодії з API шлюзу безпечного обміну системи Трембіта (ШБО), що демонструють технічні особливості розробки вебсервісів та вебклієнтів, сумісних з системою Трембіта. Даний проєкт описує створення сумісного REST-клієнта на мові програмування Python з використанням фреймворку Flask для здійснення викликів REST API через ШБО.\
Приклад описує отримання з умовної бази даних (реєстру) відомості про інформаційні об’єкти (у прикладі об’єктом є користувач) та управління їх статусом, у тому числі відправку запитів на пошук, отримання, створення, редагування та видалення об’єктів через REST API.\
Додатково розглянуто функції API ШБО для завантаження архівів з підписаними електронними повідомленнями-запитами, повідомленнями-відповідями у вигляді ASiC-контейнерів, а також генерацію ключів і сертифікатів для взаємної автентифікації між REST-клієнтом та ШБО.

## Зміст

- [Вимоги](#Вимоги)
- [Встановлення](#Встановлення)
- [Конфігурація](#конфігурація)
- [Використання](#використання)
  - [Завантаження ASiC файлу](#завантаження-asic-файлу)
  - [Генерація ключа і сертифіката](#генерація-ключа-і-сертифіката)
  - [Отримання інформації про користувача](#отримання-інформації-про-користувача)
  - [Редагування інформації про користувача](#редагування-інформації-про-користувача)
  - [Видалення користувача](#видалення-користувача)
  - [Додавання користувача](#додавання-користувача)
  - [Отримання метаданих файлів](#отримання-метаданих-файлів)
- [Логування](#логування)
- [Ліцензія](#ліцензія)

## Вимоги
- Python 3.10+
- Git (для клонування репозиторію)
- Ubuntu Server 24.04
  
## Встановлення

### Ручне встановлення та запуск

1. Клонуйте репозиторій:

    ```bash
    git clone https://github.com/kshypachov/web-client_trembita_sync.git
    ```

2. Перейдіть в директорію проєкту:

    ```bash
    cd web-client_trembita_sync
    ```

3. Встановіть залежності:

    ```bash
    pip install -r requirements.txt
    ```

4. Відредагуйте файл config.ini заповнивши вашими значеннями, згідно з прикладом конфігурації, наведеним у розділі нижче. 
5. Запустіть проєкт за допомогою команд
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run --host=0.0.0.0
    ```
6. Відкрийте в браузері посилання 
   ```bash
   http://<your_server_ip>:5000
   ```
### Встановлення як служби за допомогою скрипту
1. Завантажте та запустіть скрипт для клонування репозиторію, встановлення залежностей та налаштування сервісу:

    ```bash
    wget https://raw.githubusercontent.com/kshypachov/web-client_trembita_sync/master/deploy.sh
    chmod +x deploy.sh
    ./deploy.sh
    ```
2. Заповніть конфігураційний файл `config.ini` значеннями для вашого середовища. Приклад вмісту файлу наведено у розділі нижче.
3. Запустіть додаток командою:
    ```bash
   sudo systemctl start flask-app
   ```
4. Відкрийте в браузері посилання 
   ```bash
   http://<your_server_ip>:5000
   ```

## Конфігурація

Створіть файл конфігурації `config.ini` в корені проєкту з наступним вмістом:

```ini
[trembita]

# Протокол, який використовується для взаємодії з ШБО (https або http)
# Протокол https вимагає взаємної автентифікації клієнта з ШБО з використанням сертифікатів
protocol = https

# Хостнейм, FQDN або локальна IP-адреса ШБО
# можливі варіанти: 192.168.1.1, trembita.example.gov.ua
host = your_trembita_host

# Ідентифікатор мети обробки персональних даних для взаємодії з сервісами, що використовують Підсистему моніторингу доступу до персональних даних системи Трембіта (ПМДПД). Може бути не заданим (закоментувати параметр), якщо обмін відбувається без використання цього ПМДПД.
purpose_id = your_purpose_id

# Шлях до ssl ключів та сертифікатів для взаємодії з ШБО (директорія буде створена, якщо вона не існує)
cert_path = path/to/your/certificates

# Шлях для збереження ASiC файлів з завантаженими повідомленнями (директорія буде створена, якщо вона не існує)
asic_path = path/to/save/asic/files

 # Ім'я файлу сертифіката який буде згенеровано якщо не буде знайдено файл у cert_path
cert_file = cert_name.pem

 # Ім'я файлу ключа який буде згенеровано якщо не буде знайдено файл у cert_path
key_file = key.pem

 # Ім'я файлу сертификата Трембіти, котрий необхідний для роботи з системой Трембіта за протоколом https з взаемною аутентифікацією, має знаходитись у  cert_path
trembita_cert_file = trembita.pem  

# Повний ідентифікатор клієнтської підсистеми Трембіти, що використовується для надсилання повідомлень-запитів
[client]
# xRoadInstance (SEVDEIR чи SEVDEIR-TEST)
instance = SEVDEIR-TEST

# memberClass (GOV) 
memberClass = GOV

# memberCode - код ЄДРПОУ організації-клієнта
memberCode = your_client_member_code

# subsystemCode - код підсистеми ШБО організації-клієнта, що буде використовуватись для запитів
subsystemCode = your_client_subsystem_code

# Повний ідентифікатор сервісу Трембіти, на який надсилаються повідомлення-запити
[service]
# xRoadInstance (SEVDEIR чи SEVDEIR-TEST)
instance = SEVDEIR-TEST

# memberClass (GOV) 
memberClass = GOV

# memberCode - код ЄДРПОУ організації-постачальника
memberCode = your_service_member_code
 
# subsystemCode - код підсистеми ШБО організації-постачальника, на якій опубліковано сервіс
subsystemCode = your_service_subsystem_code

# serviceCode - код сервісу, що опублікований на ШБО організації-постачальника
serviceCode = your_service_code

# serviceVersion - версія сервісу, якщо є (зазвичай сервіс не має версії). Якщо сервіс не має версії - не задавати значення
serviceVersion = your_service_version

[logging]
# Шлях до файлу логування
filename = path/to/client.log

# filemode визначає режим, в якому буде відкритий файл логування.
# 'a' - дописувати до існуючого файлу
# 'w' - перезаписувати файл кожен раз при старті програми
filemode = a

# format визначає формат повідомлень логування.
# %(asctime)s - час створення запису
# %(name)s - ім'я логгера
# %(levelname)s - рівень логування
# %(message)s - текст повідомлення
# %(pathname)s - шлях до файлу, звідки було зроблено виклик
# %(lineno)d - номер рядка у файлі, звідки було зроблено виклик
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s

# dateformat визначає формат дати в повідомленнях логування.
# Можливі формати можуть бути такими, як:
# %Y-%m-%d %H:%M:%S - 2023-06-25 14:45:00
# %d-%m-%Y %H:%M:%S - 25-06-2023 14:45:00
dateformat = %Y-%m-%d %H:%M:%S

# level визначає рівень логування. Найбільш детальний це DEBUG, за замовчуванням INFO
# DEBUG - докладна інформація, корисна для відлагодження роботи, логується вміст запитів та відповідей
# INFO - загальна інформація про стан виконання програми
# WARNING - попередження про можливі проблеми
# ERROR - помилки, які завадили нормальному виконанню
# CRITICAL - критичні помилки, що призводять до завершення програми
level = DEBUG
```

## Використання

### Завантаження ASiC файлу

Для завантаження ASiC файлу використовуйте функцію `download_asic_from_trembita`:

```python
from your_module import download_asic_from_trembita, Config

config = Config('config.ini')
download_asic_from_trembita('path/to/save/asic/files', 'query_id', config)
```

### Генерація ключа і сертифіката

Для генерації ключа і сертифіката використовуйте функцію `generate_key_cert`:

```python
from your_module import generate_key_cert

generate_key_cert('key.pem', 'cert.pem', 'path/to/save/keys')
```

Після того, як сертифікат буде згенеровано на стороні вебклієнта, його потрібно імпортувати на шлюз Трембіти згідно відповідних інструкцій. Також, для успішної взаємної автентифікації необхідно завантажити внутрішній сертифікат шлюзу Трембіти в ту саму директорію, та назвати файл `trembita.pem`.

### Надсилання запиту до сервісу отримання інформації про користувача

Для отримання інформації про користувача використовуйте функцію `get_person_from_service`:

```python
from your_module import get_person_from_service, Config

config = Config('config.ini')
person_info = get_person_from_service('parameter', 'value', config)
print(person_info)
```

У прикладі доступні такі параметри для пошуку користувача:
name, surname, patronym, dateOfBirth, gender, rnokpp, passportNumber, unzr

### Надсилання запиту до сервісу редагування інформації про користувача

Для редагування інформації про користувача використовуйте функцію `edit_person_in_service`:

```python
from your_module import edit_person_in_service, Config

config = Config('config.ini')
response = edit_person_in_service({'field': 'value'}, config)
print(response)
```

У прикладі ідентифікація об’єкта відбувається за полем `unzr`, що має передаватися серед параметрів. Приклад запиту на оновлення номеру паспорта користувача:
```python
response = edit_person_in_service({'unzr': '20010203-00011', 'passportNumber': '123456789'}, config)
```

### Надсилання запиту до сервісу видалення користувача

Для видалення користувача використовуйте функцію `service_delete_person`:

```python
from your_module import service_delete_person, Config

config = Config('config.ini')
response = service_delete_person({'unzr': 'user_id'}, config)
print(response)
```

### Надсилання запиту до сервісу додавання користувача

Для додавання користувача використовуйте функцію `service_add_person`:

```python
from your_module import service_add_person, Config

config = Config('config.ini')
response = service_add_person({'field': 'value'}, config)
print(response)
```

Першим аргументом функції service_add_person має бути об’єкт типу dict, що містить атрибути новостворюваного користувача. Перелік доступних атрибутів перелічено у підрозділі про отримання інформації про користувача. Приклад запиту:

```python
response = service_add_person({'name': 'Ярослав', 'surname': 'Мудрий', 'patronym': 'Володимирович', 'dateOfBirth': '978-02-20', 'gender': 'male', 'rnokpp': '0000000000', 'passportNumber': '123456789', 'unzr': '09780220-00019'}, config)
```

### Отримання метаданих файлів

Приклад передбачає відображення списку завантажених файлів з повідомленнями. Для отримання метаданих файлів в директорії використовуйте функцію `get_files_with_metadata`:

```python
from your_module import get_files_with_metadata

files_metadata = get_files_with_metadata('path/to/directory')
print(files_metadata)
```

## Логування

Логування налаштовано з використанням параметрів, вказаних у секції [logging] файлу `config.ini`. Всі логи зберігаються у файлі, вказаному в конфігурації.

## Ліцензія

Цей проєкт ліцензований під ліцензією GPL v3. Дивіться файл [LICENSE](LICENSE) для деталей.
```
