from django.core.management.base import BaseCommand
from dynamodb.models import PushupDay

class Command(BaseCommand):
    help = 'Creates the DynamoDB table for pushups if it does not exist'

    def handle(self, *args, **options):
        if not PushupDay.exists():
            # 테이블 생성
            PushupDay.create_table(
                read_capacity_units=1,
                write_capacity_units=1,
                wait=True
            )
            self.stdout.write(self.style.SUCCESS('Pushup table created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Pushup table already exists.'))
