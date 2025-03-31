import os
import json
import gspread
from flask import Flask, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Load Google Sheets API credentials from environment variable
credentials_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
client = gspread.authorize(creds)

# Google Sheet ID (replace with your actual Google Sheet ID)
SHEET_ID = "13osQjkH6_IwNTJ1wGr8KAGk2b_29ntIejcDoKrQ82pk"
sheet = client.open_by_key(SHEET_ID).sheet1  # First sheet

@app.route("/rsvp", methods=["GET"])
def rsvp():
    name = request.args.get("name")
    email = request.args.get("email")
    response = request.args.get("response")

    if not name or not email or not response:
        return jsonify({"error": "Missing parameters"}), 400

    # Check if the email already exists
    existing_records = sheet.get_all_records()
    for row in existing_records:
        if row["Email"] == email:
            return jsonify({"message": "Response already recorded"}), 200

    # Append new RSVP response to Google Sheets
    sheet.append_row([name, email, response])
    
    return jsonify({"message": "RSVP recorded successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
