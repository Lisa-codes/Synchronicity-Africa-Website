import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import sqlite3

# Replace these with your actual credentials and details
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
shortcode = 'YOUR_SHORTCODE'
passkey = 'YOUR_PASSKEY'
phone_number = 'YOUR_PHONE_NUMBER'  # Donor's phone number in format 2547XXXXXXXX
callback_url = 'https://your_callback_url.com/callback'

def generate_token(consumer_key, consumer_secret):
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    access_token = json_response['access_token']
    return access_token

def store_donation(donor_name, phone_number, amount):
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO donations (donor_name, phone_number, amount, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (donor_name, phone_number, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def lipa_na_mpesa_online(access_token, shortcode, passkey, phone_number, callback_url):
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer {}".format(access_token)}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": encoded_string,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",  # Amount of donation
        "PartyA": phone_number,  # Donor's phone number in format 2547XXXXXXXX
        "PartyB": shortcode,
        "PhoneNumber": phone_number,  # Donor's phone number in format 2547XXXXXXXX
        "CallBackURL": callback_url,
        "AccountReference": "Donation",
        "TransactionDesc": "Donation"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    # Store donation details in the database
    if response.status_code == 200:
        store_donation("Donor Name", phone_number, 1)  # Replace "Donor Name" with actual donor name if available
    
    return response.text

# Generate the access token
access_token = generate_token(consumer_key, consumer_secret)

# Make the payment request
response = lipa_na_mpesa_online(access_token, shortcode, passkey, phone_number, callback_url)
print(response)
