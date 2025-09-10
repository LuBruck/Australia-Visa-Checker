# Australia Visa Checker

This project aims to automatically monitor the status of Working Holiday Visa openings for Brazil on the official Australian government website.  
When the status changes (for example, when new spots open), the script sends an alert email to the registered recipients.

---

## Features

- Accesses the official Australian government website and checks the visa status for Brazil.
- Checks the last update date of the status.
- Automatically sends an email to the registered recipients when the status changes to open.

---

## How to Use

### 1. Prerequisites

- Python 3 installed
- Install the project dependencies:

```bash
pip install -r requirements.txt
```
### 2. Configure `.env` file

Create a `.env` file in the project root whith the following content

```file
EMAIL_SENDER=youremail@gmail.com
PSW_EMAIL=your_app_password
LIST_EMAIL_RECIVER=email1@gmail.com,email2@gmail.com
```

**Note:**
For Gmail accounts, you must generate an app password and use it in the ```PSW_EMAIL``` field.

### 3. Run the Script

In the terminal, execute:

```bash
python main.py
```

If there is a change in the visa status, the registered recipients will receive an alert email.


## Customization

- To add more recipients, simply separate the emails with a comma in the `LIST_EMAIL_RECIVER` field in the `.env` file.
- The script can be adapted to monitor other countries or visa types by adjusting the search logic in the code.

---

## Notes

- The script was developed for educational purposes and can be adapted as needed.
- Make sure your email is authorized to send messages via SMTP (Gmail requires an app password).