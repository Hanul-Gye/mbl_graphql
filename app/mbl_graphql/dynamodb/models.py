from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, NumberAttribute, BooleanAttribute, ListAttribute
from decouple import config

class PushupCount(MapAttribute):
    set1 = UnicodeAttribute()
    set2 = UnicodeAttribute()
    set3 = UnicodeAttribute()
    set4 = UnicodeAttribute()
    set5 = UnicodeAttribute()

class DayDetail(MapAttribute):
    PushupCounts = MapAttribute(of=PushupCount)
    CompletionDate = UnicodeAttribute(null=True)

class Days(MapAttribute):
    Day1 = MapAttribute(of=DayDetail)
    Day2 = MapAttribute(of=DayDetail)
    Day3 = MapAttribute(of=DayDetail)

class PushupDay(Model):
    """
    PynamoDB model definition for pushups
    """
    class Meta:
        table_name = "pushups"
        region = config('AWS_DEFAULT_REGION')
    week = UnicodeAttribute(hash_key=True)
    days = MapAttribute(of=Days)
