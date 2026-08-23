# Missing Child Detection

A web application for managing missing-child reports and related information.

## Project structure

- `src` and `public` — React frontend
- `backend` — Django backend

## Run the frontend

```bash
npm install
npm start
```

Then open `http://localhost:3000` in a browser.

## Run the backend

The backend requires Python 3.8.

```bash
cd backend
py -3.8 -m venv projectenv
.\projectenv\Scripts\python.exe -m pip install -r requirements.txt
.\projectenv\Scripts\python.exe manage.py runserver
```

The backend will run at `http://127.0.0.1:8000`.

