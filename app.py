import imaplib
import email
from email.header import decode_header
import psycopg2
import schedule
import time

def check_email_and_update_db():
    mail_pass = "h883F5EPDuj6Tbs70dX3"
    username = "it.department.lkmb-rt@mail.ru"
    imap_server = "imap.mail.ru"

    imap = imaplib.IMAP4_SSL(imap_server)
    try:
        imap.login(username, mail_pass)
    except imaplib.IMAP4.error as e:
        print("Ошибка при входе:", e)
        return

    imap.select("INBOX")
    res, messages = imap.search(None, 'ALL')
    messages = messages[0].split()

    subjects = []

    def decode_mime_words(mime_words):
        # Декодируем заголовки с различными кодировками
        decoded_words = []
        for word, encoding in decode_header(mime_words):
            if isinstance(word, bytes):
                if encoding:
                    decoded_words.append(word.decode(encoding))
                else:
                    decoded_words.append(word.decode('utf-8', errors='replace'))  # Замена ошибок
            else:
                decoded_words.append(word)
        return ''.join(decoded_words)

    for num in messages:
        res, msg_data = imap.fetch(num, '(RFC822)')
        if res != 'OK':
            print(f"Ошибка получения письма с номером {num.decode('utf-8')}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_mime_words(msg["Subject"])

        subjects.append(subject)

    imap.logout()

    print("Список заголовков:", subjects)
    for title in subjects:
        if "id" in title.lower():
            id_number = title.split()[0]  # Получаем первое слово (ID)
            if "одобрен" in title.lower():
                status = "Одобрен"
            elif "отказ" in title.lower():
                status = "Отказ"
            else:
                continue  # Пропускаем, если статус не определён

            print(f"Обновление статуса для ID {id_number[2:]} на '{status}'")  # Логирование
            update_status_in_db(id_number[2:], status)

def update_status_in_db(id_number, status):
    host = "localhost"
    database = "mail_db"
    user = "postgres"
    password = "sda"

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # Обновление статуса в базе данных
        cursor.execute("UPDATE projects SET status = %s WHERE project_id = %s", (status, id_number))
        connection.commit()
        print(f"Статус для ID {id_number} обновлён на '{status}'")

    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

# Планируем выполнение функции каждую минуту
schedule.every(1).minutes.do(check_email_and_update_db)

# Бесконечный цикл для выполнения запланированных задач
while True:
    schedule.run_pending()
    time.sleep(1)
