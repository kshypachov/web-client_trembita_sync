# Посібник з встановлення REST клієнта вручну

## Опис 
Цей посібник допоможе пройти процесс встановлення REST клієнта вручну. Для почтаку потрібно мати чисту систему Ubuntu, 
всі необхідні пакети та репозиторії будуть підключені пізніше.

## Загальні вимоги
- Python 3.10+
- Git (для клонування репозиторію)
- Ubuntu Server 24.04

## Встановлення REST клієнта вручну

Для ручного встановлення виконайте наступні кроки:

### 1. Встановлення залежностей
Для початку потрібно встановити всі необхідні пакети. Виконайте наступні команди для встановлення Python 3.10 і супутніх інструментів:

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv
```

- Примітка: Якщо версія Python нижче 3.10, клієнт працювати не буде.

### 2. Клонування репозиторію
```bash
git clone https://github.com/kshypachov/web-client_trembita_sync.git
cd web-client_trembita_sync
```

### 3. Створення та активація віртуального оточення
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Встановлення пакетів залежностей Python
```bash
pip install -r requirements.txt
```

### 5. Конфігурування клієнту 

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
### 6. Налаштування та запуск сервісу як systemd-сервіс

Перевірте за допомогою команди `pwd` що ви знаходитесь у директорії `web-client_trembita_sync`. 
Створіть systemd unit-файл для запуску сервісу:

```bash
sudo bash -c "cat > /etc/systemd/system/flask-app.service" << EOL
[Unit]
Description=Flask Application
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL
```

#### Перезапуск systemd та запуск клієнта

1.	Перезавантажте конфігурацію systemd:
```bash
sudo systemctl daemon-reload
```

2.	Запустіть клієнт:
```bash
sudo systemctl start flask-app
```

3. Додайте клієнт до автозапуску:
```bash
sudo systemctl enable flask-app
```

4.	Перевірте статус клієнта:
```bash
sudo systemctl status flask-app
```

Кліент працює на порту 5000, комунікація з клієнтом відбувається за допомогою веб браузера.