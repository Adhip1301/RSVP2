import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_ID = "13osQjkH6_IwNTJ1wGr8KAGk2b_29ntIejcDoKrQ82pk"  # Replace with your actual Sheet ID
sheet = client.open_by_key(SHEET_ID).sheet1  # First sheet

@app.route("/rsvp")
def rsvp():
    name = request.args.get("name")
    email = request.args.get("email")
    response = request.args.get("response")

    # Validate input
    if not name or not email or not response:
        return "Missing RSVP details!", 400  # Bad request if any field is missing

    # Get all existing responses
    existing_data = sheet.get_all_values()

    # Check if this email has already responded
    for row in existing_data:
        if len(row) >= 2 and row[1] == email:  # Assuming Email is in Column B
            return "You have already responded!", 400

    # Append new RSVP response
    sheet.append_row([name, email, response])
    return "RSVP recorded successfully!", 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Prevents double execution
