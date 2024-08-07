import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_bootstrap import Bootstrap
import utils
import os
import logging

# Зчитування параметрів додатку з конфігураційного файлу
conf = utils.Config('config.ini')

# Налаштування логування
try:
    utils.configure_logging(conf)
    logger = logging.getLogger(__name__)
    logger.info("Логування налаштовано успішно.")
except Exception as e:
    print(f"Помилка налаштування логування: {e}")
    sys.exit(1)

logger.debug("Початок ініціалізації додатку")

crt_directory = conf.cert_path
asic_directory = conf.asic_path
key = conf.key_file
cert = conf.cert_file

# Створення директорій
utils.create_dir_if_not_exist(crt_directory)
utils.create_dir_if_not_exist(asic_directory)

private_key_full_path = os.path.join(crt_directory, key)
certificate_full_path = os.path.join(crt_directory, cert)

if not os.path.exists(private_key_full_path) or not os.path.exists(certificate_full_path):
    logger.info(f"Не знайдено ключ: {key} або сертифікат {cert} у директорії {crt_directory}")
    utils.generate_key_cert(key, cert, crt_directory)


# Ініціалізація додатку
app = Flask(__name__)
Bootstrap(app)
logger.info("Додаток Flask ініціалізовано.")


# Опис функціоналу обробки HTTP запитів
@app.route('/', methods=['GET', 'POST'])
def search_user():
    logger.debug(f"Отримано {'POST' if request.method == 'POST' else 'GET'} запит на маршрут '/'.")
    if request.method == 'POST': # Прийшов запит з даними від форми (на пошук за одним з параметрів), обробляємо
        search_field = request.form.get('search_field')
        search_value = request.form.get('search_value')

        logger.debug(f"Отримано параметри пошуку: {search_field} : {search_value} ")

        try:
            data = utils.get_person_from_service(search_field, search_value, conf)
        except Exception as e:
            logger.error(f"Виникла помилка: {str(e)}")
            return render_template('error.html', error_message=e,  current_page='index')
        return render_template('list_person.html', data=data,  current_page='index')

    return render_template('search_form.html',  current_page='index') # Прийшов GET запит, просто віддаємо вебсторінку


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    logger.debug(f"Отримано {'POST' if request.method == 'POST' else 'GET'} запит на маршрут '/create'.")
    if request.method == 'POST': # Прийшов запит з даними від форми (на створення об'єкта користувача), обробляємо
        try:
            form_data = request.get_json()
            logger.debug(f"Отримано запит на створення з параметрами: {form_data}")
            response = utils.service_add_person(form_data, conf)
            resp = jsonify(message=response.body), response.status_code
            return resp
        except Exception as e:
            logger.debug(f"Виникла помилка: {str(e)}")
            resp = jsonify(message=f'Помилка при створенні об’єкта користувача: {str(e)}'), 422
            return resp

    return render_template('create_person.html',  current_page='create') # Прийшов GET запит, просто віддаємо вебсторінку


@app.route('/edit', methods = ['POST'])
def edit_user():
    logger.debug("Отримано POST запит на маршрут '/edit'.")
    data = request.get_json()
    logger.debug(f"Отримано дані для редагування: {data}")
    try:
        http_resp = utils.edit_person_in_service(data, conf)
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        resp = jsonify(message=f"Виникла помилка при обробці запиту на редагування: error: {str(e)}"), 500
        return resp
    return jsonify(message=http_resp.body), http_resp.status_code


@app.route('/delete', methods = ['POST'])
def delete_person():
    logger.debug("Отримано POST запит на маршрут '/delete'.")
    data = request.get_json()
    logger.debug(f"Отримано запит на видалення: {data}")
    try:
        http_resp = utils.service_delete_person(data, conf)
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        resp = jsonify(message=f"Виникла помилка при обробці запиту на видалення: error: {str(e)}"), 500
        return resp
    return jsonify(message= http_resp.body), http_resp.status_code

@app.route('/files')
def list_files():
    logger.debug("Отримано GET запит на маршрут '/files'.")
    try:
        files = []
        for filename in os.listdir(asic_directory):
            filepath = os.path.join(asic_directory, filename)
            if os.path.isfile(filepath):
                creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
                files.append({
                    'name': filename,
                    'creation_time': creation_time.strftime('%Y-%m-%d %H:%M:%S')
                })

        # Sort files by creation time (descending order)
        files = sorted(files, key=lambda x: x['creation_time'], reverse=True)
        logger.debug("Список файлів отримано успішно.")

        return render_template('list_files_run_away.html', files=files, current_page='files')
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        return render_template('error.html', error_message=e, current_page='files')


@app.route('/download/<filename>')
def download_file(filename):
    logger.debug(f"Отримано GET запит на маршрут '/download/{filename}'.")
    ASIC_DIR = os.path.join(os.getcwd(), asic_directory)
    safe_filename = os.path.basename(filename)  # Валідація шляху файлової системи
    try:
        return send_from_directory(ASIC_DIR, safe_filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        return render_template('error.html', error_message=e, current_page='files')


@app.route('/download_cert/<filename>')
def download_cert(filename):
    logger.debug(f"Отримано GET запит на маршрут '/download_cert/{filename}'.")
    CERT_DIR = os.path.join(os.getcwd(), crt_directory)
    safe_filename = os.path.basename(filename)  # Обезопашиваем путь
    try:
        return send_from_directory(CERT_DIR, safe_filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        return render_template('error.html', error_message=e, current_page='certs')

@app.route('/certs')
def list_certs():
    logger.debug("Отримано GET запит на маршрут '/certs'.")
    try:
        files = []
        for filename in os.listdir(crt_directory):
            filepath = os.path.join(crt_directory, filename)
            if os.path.isfile(filepath):
                creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
                files.append({
                    'name': filename,
                    'creation_time': creation_time.strftime('%Y-%m-%d %H:%M:%S')
                })

        # Sort files by creation time (descending order)
        files = sorted(files, key=lambda x: x['creation_time'], reverse=True)
        logger.debug("Список сертифікатів отримано успішно.")

        return render_template('list_certs.html', files=files, current_page='certs')
    except Exception as e:
        logger.error(f"Виникла помилка: {str(e)}")
        return render_template('error.html', error_message=e, current_page='certs')

# Запуск додатку
if __name__ == '__main__':
    #sys.stdout.reconfigure(encoding='utf-8')
    logger.info("Запуск додатку Flask.")
    app.run(debug=True)
    logger.info("Додаток Flask зупинено.")
