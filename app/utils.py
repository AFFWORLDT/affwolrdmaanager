from passlib.context import CryptContext
from bson import json_util, ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import json
import string
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def gen_code(n: int = 6) -> str:
    seq = list(string.ascii_letters + string.digits)
    return "".join(random.choices(seq, k=n))


def verify(plain, hashed):
    return pwd_context.verify(plain, hashed)


def bsonToJson(id: ObjectId):
    tid = json.loads(json_util.dumps(id))
    return tid["$oid"]


def jsonToBson(id: str):
    return ObjectId(oid=id)


def send_email(reciever: str, subject: str, html: str):
    sender = "portal@affworld.in"
    sender_title = "Affworld Technologies"
    recipient = reciever

    msg = MIMEMultipart()
    msg.attach(MIMEText(html, "html"))
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = formataddr((str(Header(sender_title, "utf-8")), sender))
    msg["To"] = recipient

    server = smtplib.SMTP_SSL("smtp.zoho.in", 465)

    server.login("portal@affworld.in", "Rahul12@")
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
