import json
import os
import boto3
import requests
from google.cloud import storage
from google.oauth2 import service_account
import base64
import datetime

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    email = message.get("email")
    
    assignment_id = message.get("assignment_id")
    submission_id = message.get("submission_id")
    
    num_of_attempts = message.get("num_of_attempts")
    submission_date = message.get("submission_date")
    update_date = message.get("update_date")
    assignment_name = message.get("assignment_name")
    
    file_url = message.get("submission_url")
    
    dynamodb = boto3.resource('dynamodb')
    dynamodb_table = dynamodb.Table(os.environ['DYNAMO_DB_TBALE'])
    
    api = os.environ['MAILGUN_API']
    api_key = os.environ['MAILGUN_KEY']
    bucket_name = os.environ['BUCKET_NAME']
    
    # storage_client = storage.Client().from_service_account_json('JSON filepath')
    service_key = os.environ['SERVICE_KEY']
    decode_service_key = base64.b64decode(service_key).decode('utf-8')
    creds_dict = json.loads(decode_service_key)
    credentials = service_account.Credentials.from_service_account_info(creds_dict)      
    storage_client = storage.Client(credentials=credentials)
    
    try:
        # Download the file
        response = requests.get(file_url)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        
        # Check if the content-type is application/zip
        if response.headers.get('Content-Type') != 'application/zip':
            raise ValueError("Downloaded file is not a ZIP file")
        
        # Save the file temporarily
        local_filename = '/tmp/myrepo-1.0.0.zip'
        with open(local_filename, 'wb') as f:
            f.write(response.content)
            
        # Upload to Google Cloud Storage
        destination_blob_name = f'{email}/{submission_id}/{num_of_attempts}/submission.zip'
        
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_filename)
        
        
        print(json.dumps({'statusCode': 200,'body': 'File downloaded and uploaded successfully'}))
        
        message = (
            f"Your assignment was received.<br>"
            f"Submission details:<br>"
            f"Assignment name: {assignment_name}<br>"
            f"Number of attempts: {num_of_attempts}<br>"
            f"<html><body>"
            f"<p>Your submission is saved at</p>"
            f"<p>{destination_blob_name}</p>"
            f"</body></html>"
        )

        requests.post(
            "https://api.mailgun.net/v3/csye6225sw.me/messages",
            auth=(api, api_key),
            data={"from": "Submission Notification <CSYE6225INFO@csye6225sw.me>",
                "to": [f'{email}'],
                "subject": 'Assignment Submission Notification',
                "html": message})
        
        
        email_info = {
            'submission_id': f'{submission_id}',
            'email': f'{email}',
            'timestamp': f'{update_date}',
            'submission_status': 'Success',
            'status': 'Deliver'
        }

        dynamodb_table.put_item(Item=email_info)
        
    except Exception as e:
        print(json.dumps({'statusCode': 500, 'body': str(e)}))
        
        message_fail = (
            f"Your assignment submission was failed.<br>"
            f"Submission details:<br>"
            f"Assignment name: {assignment_name}<br>"
            f"Number of attempts: {num_of_attempts}<br>"
            f"<html><body>"
            f"You may provide a wrong URL<br>"
            f"</body></html>"
        )
        
        requests.post(
		"https://api.mailgun.net/v3/csye6225sw.me/messages",
		auth=(api, api_key),
		data={"from": "Submission Failed Notification <CSYE6225INFO@csye6225sw.me>",
			"to": [f'{email}'],
			"subject": "Submission Failed",
			"html": message_fail})
        
        email_info = {
            'submission_id': f'{submission_id}',
            'email': f'{email}',
            'timestamp': f'{update_date}',
            'submission_status': 'Failed',
            'status': 'Deliver'
        }
        
        dynamodb_table.put_item(Item=email_info)
        

    