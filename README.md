# CS590 Modern Software Development  
## Docker Demo: FastAPI + Nginx + DukeGPT Chat

Run a **frontend + backend** app with Docker Compose:
- **Backend**: FastAPI (Python) with `/health`, `/api/hello`, `/api/echo`, and **`/api/chat` (using DukeGPT)**  
- **Frontend**: Static HTML + JS served by **Nginx**  
- **One command** to start both services

---

## Project Structure

    .
    ├── docker-compose.yml
    ├── .env                 # your API key & config (do NOT commit)
    ├── backend/
    │   ├── app/
    │   │   └── main.py
    │   ├── requirements.txt
    │   └── Dockerfile
    └── frontend/
        ├── bin/
        │   │   └── inject-env.sh
        ├── public/
        │   ├── index.html
        │   └── app.js
        └── Dockerfile

---

## Setup

1) Install Docker Desktop (or Docker Engine). Confirm `docker compose` works.

2) Create a file named **.env** in the project root (replace the API key):

        APP_NAME=CS590 Classroom Demo Chatbot (DukeGPT)
        LLM_API_URL=https://litellm.oit.duke.edu/v1
        LLM_TOKEN=REPLACE_ME
        MODEL_ID=GPT 4.1
        HOST=localhost
        CHAT_API_URL=http://${HOST}:4003
        CORS_ORIGINS=http://${HOST}:4083

   - This file is listed in the **.gitignore** so you don’t commit secrets.

3) Change the values as necessary to fit your solution:

   - Change the placeholder LLM API key from REPLACE_ME to yours
   - Change the HOST from localhost to your VCM hostname for deployment
   - Change the MODEL_ID to a different option (Mistral is free and run on Duke computers)
   - Change the LLM_API_URL if you prefer to use a non-Duke LLM that you have access to

4) Build & run:

        docker compose up --build

   Open:
   - **Frontend** → http://localhost:4083  
   - **API docs** → http://localhost:4003/docs

4) Stop everything:

        docker compose down

5) Useful commands:

        # see status
        docker compose ps

        # stream logs
        docker compose logs -f

        # restart just one service
        docker compose restart backend
        docker compose restart frontend

        # stop without removing containers
        docker compose stop

---

## How to Use (Frontend)

- **Health Check** → Press **Check** (calls `GET /health`)  
- **Hello** → Press **Say Hello** (calls `GET /api/hello?name=Student`)  
- **Echo** → Type a message, press **Send** (calls `POST /api/echo`)  
- **Chatbot** → Ask a question (calls `POST /api/chat`, replies from DukeGPT)

---

## Troubleshooting

- **Port in use** → edit host ports in `docker-compose.yml` (e.g., `4003:4000`, `4083:80`)  
- **No chatbot reply** → ensure `.env` has a valid `LITELLM_TOKEN`  
- **Backend not healthy** → check logs:

        docker compose logs backend

- **CORS error** → make sure `.env` has CORS_ORIGINS set to match the URL are using to run the website

---

## What You’ll Learn

- Build and run services in **containers**  
- Use **Docker Compose** to connect frontend & backend  
- Call Fast APIs from the browser  
- Keep secrets safe with **.env**

---
