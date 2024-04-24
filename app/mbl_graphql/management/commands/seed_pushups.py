import json
from django.core.management.base import BaseCommand
from dynamodb.models import PushupDay

class Command(BaseCommand):
    help = 'Seeds the database with initial pushup data from a JSON file'

    def handle(self, *args, **options):
        try:
            with open('dynamodb/seeds/initial_pushups_data.json', 'r') as file:
                data = json.load(file)
            for item in data:
                pushup_day = PushupDay()
                pushup_day.week = item['Week']
                pushup_day.days = Days(**item['Days'])
                pushup_day.save()

            self.stdout.write(self.style.SUCCESS('Successfully seeded pushup data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding pushup data: {str(e)}'))
