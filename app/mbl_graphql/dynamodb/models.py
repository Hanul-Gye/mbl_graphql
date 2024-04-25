from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, NumberAttribute
from decouple import config

class PushupSet(MapAttribute):
    set1 = NumberAttribute(attr_name='set1')
    set2 = NumberAttribute(attr_name='set2')
    set3 = NumberAttribute(attr_name='set3')
    set4 = NumberAttribute(attr_name='set4')
    set5 = NumberAttribute(attr_name='set5')

class PushupCount(MapAttribute):
    less_than_5 = PushupSet(attr_name='lessThan5')
    six_to_ten = PushupSet(attr_name='sixToTen')
    eleven_to_twenty = PushupSet(attr_name='elevenToTwenty')

class PushupDay(Model):
    class Meta:
        table_name = "pushups"
        region = config('AWS_DEFAULT_REGION')
        host = config('DYNAMODB_ENDPOINT')
    week = NumberAttribute(hash_key=True)
    day = UnicodeAttribute(range_key=True)
    pushup_counts = PushupCount(attr_name='pushupCounts')
    completion_date = UnicodeAttribute(null=True, attr_name='completionDate')
