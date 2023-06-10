# OMG - OddMailGuard

> tldr : A web service that assigns an oddness score to emails.

**OMG** aka **OddMailGuard** is a dedicated web service designed to verify the oddness of emails. To use the service, simply transfer an email to the displayed address and include the given ID at the start of the email subject. The analysis will be take arround 30 seconds, providing you with an overall oddness score, as well as more specific oddness details, such as for the body, subject, sender and more.

 ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

# 🌐 Services

OMG uses [Google Safe Browsing API](https://developers.google.com/safe-browsing/v4) to detect malicious links. It also uses [OpenAI's Chat Completion API](https://platform.openai.com/docs/guides/gpt/completions-api) with the gpt-3.5-turbo model to assign an oddness value (ranging from 0 to 100) to the email body and subject. To ensure data protection, all potential links and emails are replaced with placeholders, to avoid data leakage (since OpenAi store everything).

# ⬇️ Installation

1. Clone the repo
```sh
git clone https://github.com/YungBricoCoop/omg
cd omg
```
2. Install backend dependencies
```sh
cd backend
pip install -r requirements.txt
```
3. Install frontend dependencies
```sh
cd frontend
npm i
```


# 🔧 Config
Before running the code you might need to configure the environment. For the backend, create a `.env` file in the root directory and update the following keys:

```ini
MAIL_SERVER="server.com"
MAIL_USERNAME="username@server.com"
MAIL_PASSWORD="strong_password"
MAIL_IMAP_PORT=993
MAIL_SMTP_PORT=465
ID_LENGTH=8
SAFE_BROWSING_API_KEY="https://developers.google.com/safe-browsing/v4"
OPENAI_API_KEY="https://platform.openai.com/account/api-keys"
```

# 🚀 Run

## Backend
Use **uvicorn** for development, and **gunicorn** for production.

Dev :  `uvicorn app:app --reload`

Prod :  `gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app`

## Frontend

For development, you can host the frontend using `npm run dev`. 

For production, build the frontend using `npm run build` and host it on a production server.

##  📝 To Do

- [ ] Enhance attachment oddness scanning

## 🤝Contributing

Im open to contributions! If you'd like to contribute, please create a pull request and I'll review it as soon as I can.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.