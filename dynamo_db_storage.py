import uuid
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
parlays_table = dynamodb.Table("Parlays")


# Save a new parlay
def save_parlay(parlay_data):
    parlay_id = str(uuid.uuid4())
    item = {
        "user_id": parlay_data["user_id"],
        "parlay_id": parlay_id,
        "wager": parlay_data["wager"],
        "legs": parlay_data["legs"],
        "status": "pending",
    }
    parlays_table.put_item(Item=item)
    return parlay_id


# Get all parlays for a user
def get_parlays_by_user(user_id):
    response = parlays_table.query(KeyConditionExpression=Key("user_id").eq(user_id))
    return response.get("Items", [])


# Update the status of a parlay
def update_parlay_status(user_id, parlay_id, status):
    parlays_table.update_item(
        Key={"user_id": user_id, "parlay_id": parlay_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": status},
    )


# Delete a parlay
def delete_parlay(user_id, parlay_id):
    parlays_table.delete_item(Key={"user_id": user_id, "parlay_id": parlay_id})
