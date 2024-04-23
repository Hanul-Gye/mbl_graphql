import graphene
import boto3
from boto3.dynamodb.conditions import Key

class PushupCountType(graphene.ObjectType):
    set1 = graphene.String()
    set2 = graphene.String()
    set3 = graphene.String()
    set4 = graphene.String()
    set5 = graphene.String()

class PushupRangeType(graphene.ObjectType):
    less_than_5 = graphene.Field(PushupCountType)
    six_to_ten = graphene.Field(PushupCountType)
    eleven_to_twenty = graphene.Field(PushupCountType)

class PushupType(graphene.ObjectType):
    week = graphene.String()
    day = graphene.String()
    pushup_counts = graphene.Field(PushupRangeType)
    completion_date = graphene.String()

class Query(graphene.ObjectType):
    pushups = graphene.List(PushupType, week=graphene.String(), day=graphene.String())

    def resolve_pushups(self, info, week=None, day=None):
        # DynamoDB에 연결
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000')
        table = dynamodb.Table('pushups')

        # DynamoDB에서 아이템 조회
        response = table.query(
            KeyConditionExpression=Key('Week').eq(week) & Key('Day').eq(day)
        )
        items = response.get('Items', [])
        
        # DynamoDB 아이템을 GraphQL 타입으로 변환
        results = []
        for item in items:
            pushup_counts = item.get('PushupCounts', {})
            less_than_5 = pushup_counts.get('<5', {})
            less_than_5_data = {k: v['S'] for k, v in less_than_5.items()} if isinstance(less_than_5, dict) else {}

            results.append(PushupType(
                week=item.get('Week', {}).get('S', ''),
                day=item.get('Day', {}).get('S', ''),
                pushup_counts=PushupRangeType(
                    less_than_5=PushupCountType(**less_than_5_data),
                    # 같은 방식으로 six_to_ten과 eleven_to_twenty를 처리하세요
                ),
                completion_date=item.get('CompletionDate', {}).get('NULL', 'False')
            ))
        return results


# 스키마 정의는 모든 클래스 정의 뒤에 한 번만 진행
schema = graphene.Schema(query=Query)