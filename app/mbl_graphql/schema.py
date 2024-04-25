import graphene
from graphene import ObjectType, String, Field, Int, Schema
from mbl_graphql.dynamodb.models import PushupDay
from pynamodb.exceptions import DoesNotExist

class PushupSetType(ObjectType):
    set1 = Int()
    set2 = Int()
    set3 = Int()
    set4 = Int()
    set5 = Int()

class PushupCountType(ObjectType):
    less_than_5 = Field(PushupSetType)
    six_to_ten = Field(PushupSetType)
    eleven_to_twenty = Field(PushupSetType)

class PushupDayType(ObjectType):
    week = Int()
    day = String()
    pushup_counts = Field(PushupCountType)
    completion_date = String()

class Query(ObjectType):
    pushup_day = Field(PushupDayType, week=Int(), day=String())

    def resolve_pushup_day(self, info, week, day):
        # Here you would query your DynamoDB table
        # For example, using boto3 directly or your PynamoDB model
        try:
            pushup_day = PushupDay.get(week, day)

            return PushupDayType(
                week=pushup_day.week,
                day=pushup_day.day,
                pushup_counts=PushupCountType(
                    less_than_5=PushupSetType(
                        set1=pushup_day.pushup_counts.less_than_5.set1,
                        set2=pushup_day.pushup_counts.less_than_5.set2,
                        set3=pushup_day.pushup_counts.less_than_5.set3,
                        set4=pushup_day.pushup_counts.less_than_5.set4,
                        set5=pushup_day.pushup_counts.less_than_5.set5,
                    ),
                    # six_to_ten=PushupSetType(
                    #     set1=pushup_day.pushup_counts.six_to_ten.set1,
                    #     ...
                    # ),
                ),
                completion_date=pushup_day.completion_date
            )
        except DoesNotExist:
            return None

# 스키마 정의는 모든 클래스 정의 뒤에 한 번만 진행
schema = Schema(query=Query)