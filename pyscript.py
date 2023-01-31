import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")
import django

django.setup()

from django.contrib.auth.models import User
from random import choices
from string import ascii_uppercase, digits
import requests
from django.conf import settings
from django.db import transaction
from accounts.models import UserProfile

from polls.models import Batch


def send_sms(phone: str, message: str) -> bool:

    url = settings.SMS_URL + F'&number=88{phone}&message={message}'

    payload = {}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        print("SMS not sent")
    return True


password_generator = ascii_uppercase + digits


reader = csv.DictReader(open('data.csv'))

for _ in range(1000):
    try:
        data = next(reader)
        s_id = data.get('ID')
        phone = data.get('PHONE')
        if phone[0] != '0':
            phone = '0' + phone
        password = str.join('', choices(password_generator, k=8))
        print("data: ", data, 'password: ', password)
        with transaction.atomic():
            if User.objects.filter(username=s_id).exists():
                print(f"already exists: {s_id}")
                continue
            user = User.objects.create_user(username=s_id, password=password)
            batch = Batch.objects.get(number=data.get('BATCH'))
            UserProfile.objects.create(user=user, batch=batch)
        with open("cred.txt", 'a') as file1:
            file1.write(f"{s_id} - {password}\n")
        send_sms(phone=phone, message=f'Dear {data.get("NAME")}({s_id}),\n\n\n'
                                      f'Your login pass: {password}\n\n'
                                      f'Login URL: https://poll.kidslab.center/accounts/login/\n')
        print(f"SMS Send Success to: {phone} with ID: {s_id}")
    except StopIteration:
        print("completed")
        break
