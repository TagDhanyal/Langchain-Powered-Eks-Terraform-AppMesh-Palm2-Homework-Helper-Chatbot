# will make it its own micorservice for v2

import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'users'  # Replace with your actual table name
table = dynamodb.Table(table_name)

def fetch_all_users():
    response = table.scan()
    return response.get('Items', [])

# --- USER AUTHENTICATION ---
users = fetch_all_users()

usernames = [user.get("username") for user in users]
names = [user.get("name") for user in users]
hashed_passwords = [user.get("password") for user in users]