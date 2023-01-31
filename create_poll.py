import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")
import django

django.setup()

from django.contrib.auth.models import User

from polls.models import Batch, Poll, Choice

batches = Batch.objects.filter(number__in=[1, 2, 3])
owner = User.objects.get(username='admin')

polls = {
}

for batch in batches:
    if batch.number == 1:
        poll = Poll.objects.create(owner=owner, text='Who will be the president', batch=batch)
        polls['1'] = poll
    elif batch.number == 2:
        poll = Poll.objects.create(owner=owner, text='Who will be the Secretary', batch=batch)
        polls['2'] = poll
    elif batch.number == 3:
        poll = Poll.objects.create(owner=owner, text='Who will be the Organizing Secretary', batch=batch)
        polls['3'] = poll


reader = csv.DictReader(open('data.csv'))


for _ in range(1000):
    try:
        data = next(reader)
        name = data.get('NAME')
        batch_no = data.get('BATCH')
        username = '0' + data.get('ID')
        poll = polls.get(batch_no)
        Choice.objects.create(poll=poll, choice_text=name)
    except StopIteration:
        print("completed")
        break
