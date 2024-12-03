import imaplib
import email
from email.header import decode_header
def main():
    mail_pass = "h883F5EPDuj6Tbs70dX3"
    username = "it.department.lkmb-rt@mail.ru"
    imap_server = "imap.mail.ru"

    imap = imaplib.IMAP4_SSL(imap_server)
    try:
        imap.login(username, mail_pass)
    except imaplib.IMAP4.error as e:
        print("Ошибка при входе:", e)

    imap.select("INBOX")

    # Получаем список всех писем
    res, messages = imap.search(None, 'ALL')
    messages = messages[0].split()

    # Выводим количество входящих писем
    print(f"Всего входящих писем: {len(messages)}")

    # Списки для хранения заголовков и тел писем
    subjects = []
    bodies = []

    # Функция для получения тела письма
    def get_body(msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(part.get_content_charset())
        else:
            return msg.get_payload(decode=True).decode(msg.get_content_charset())

    # Перебираем все письма
    for num in messages:
        res, msg_data = imap.fetch(num, '(RFC822)')
        if res != 'OK':
            print(f"Ошибка получения письма с номером {num.decode('utf-8')}")
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        
        # Получаем заголовок письма
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8')

        # Получаем тело письма
        body = get_body(msg)

        # Сохраняем заголовок и тело письма в списки
        subjects.append(subject)
        bodies.append(body)


    # Закрываем соединение
    imap.logout()

    # Выводим заголовки и тела всех писем
    print("\nЗаголовки всех писем:")
    for subject in subjects:
        pass
        # print(subject)

    # print("\nТела всех писем:")
    # for body in bodies:
    #     print(body)
# Проверка наличия "id" и вывод элемента с его индексом
    print("Список заголовков:", subjects)
    for index, title in enumerate(subjects):
        if "id" in title.lower():
            # Извлекаем номер ID и статус
            id_number = title.split()[0]  # Получаем первое слово (ID)
            status = "согласовано" if "согласовано" in title.lower() else "не согласовано"
            print(f"id {id_number[2:]} статус: {status}")


main()















# posgtresql 
# password = "sda"
# port = 5432
# user = "postgres" no name
# host = "localhost" no name
# dbname = "postgres" no name