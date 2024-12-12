import logging
import requests
import json
import os
from decouple import config
from requests.auth import HTTPBasicAuth
from icecream import ic
import csv
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(level=logging.INFO)


import requests

def retrieve_secrets():
    """Retrieve secrets from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-west-1"
    )
    try:
        get_secret_value_response_halo = client.get_secret_value(
            SecretId='halo_oauth_token'
        )
        secrets_halo = json.loads(get_secret_value_response_halo['SecretString'])
        
        return secrets_halo['access_token']
    except BotoCoreError as e:
        logging.error(f"BotoCoreError retrieving secrets: {e}")
        raise Exception(status_code=500, detail="Failed to retrieve secrets from AWS Secrets Manager")
    except ClientError as e:
        logging.error(f"ClientError retrieving secrets: {e}")
        raise Exception(status_code=500, detail="Failed to retrieve secrets from AWS Secrets Manager")

def change_ticket_to_unbillable(ticket_id):
    secrets = retrieve_secrets()
    token = secrets['access_token']
    url = "https://synergy.halopsa.com/api/Tickets"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = [{
        "id": ticket_id,
        "isbillable": False
    }]

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        logging.info("Successfully updated ticket")
    else:
        logging.error(f"Failed to update ticket: {response.text}")

def change_tickets_from_csv(csv_file_path):
    token = retrieve_secrets()

    url = "https://synergy.halopsa.com/api/Tickets"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # Skip the header row
        for row in csv_reader:
            ticket_id = row[0]  # Accessing the first column
            # logging.info(f"Updating ticket {ticket_id}")

            payload = [{
                "id": ticket_id,
                "isbillable": False
            }]

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 201:
                logging.info(f"Successfully updated ticket {ticket_id}")
            else:
                logging.error(f"Failed to update ticket {ticket_id}: {response.text}")


if __name__ == "__main__":
    csv_file_path = './crgh_finance.csv'
    change_tickets_from_csv(csv_file_path)

