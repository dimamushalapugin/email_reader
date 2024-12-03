import imaplib
import email
from email.header import decode_header


mail_pass = "h883F5EPDuj6Tbs70dX3"
username = "it.department.lkmb-rt@mail.ru"
imap_server = "imap.mail.ru"


imap = imaplib.IMAP4_SSL(imap_server)
try:
    imap.login(username, mail_pass)
except imaplib.IMAP4.error as e:
    print("Ошибка при входе:", e)

imap.select("INBOX")
# print(imap.select("INBOX"))

res, msg = imap.fetch(b'1', '(RFC822)') ## b'32739 - номер сообщения, самые первые сообщения с конца
msg = email.message_from_bytes(msg[0][1])
# print(msg)
letter_date = email.utils.parsedate_tz(msg["Date"]) # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
letter_id = msg["Message-ID"] #айди письма
letter_from = msg["Return-path"] # e-mail отправителя

subject = msg["Subject"]
subject = subject.encode('unicode-escape').decode('utf-8')
# print(subject)

# print(type(letter_date), type(letter_id), letter_id, type(letter_from))

try:
    subject = decode_header(msg["Subject"])[0][0].decode('utf-8')  # декодирование заголовка, с ним как раз проблема
    print(subject)
except:
    print("ошибка декодирования заголовка")
    response = imap.fetch(b'0', "(BODY[HEADER.FIELDS (Subject)])")
    subject = response[1][0][1].decode('utf-8')
    decoded_subject = email.header.make_header(email.header.decode_header(subject))
    print(decoded_subject)


# Функция для извлечения текста из тела письма
def get_body(msg):
    if msg.is_multipart():
        # Если сообщение состоит из нескольких частей
        for part in msg.walk():
            # Ищем текстовые части
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        # Если сообщение не является многокомпонентным
        return msg.get_payload(decode=True).decode(msg.get_content_charset())

# Чтение тела письма
body = get_body(msg)
print(body)

imap.logout()

# posgtresql 
# password = "sda"
# port = 5432
# user = "postgres" no name
# host = "localhost" no name
# dbname = "postgres" no name

        

