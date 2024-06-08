#
## Getting Started with backend

First, setup the environment:

```
Create environment outside the project root directory.
1. python3.10 -m venv healthbot
2. source path_to_healthbot/bin/activate
```

We use the OpenAI LLM and google search api. As a result you need to specify an `OPENAI_API_KEY`, `GOOGLE_CSE_ID` and `GOOGLE_API_KEY` in an .env file inside backend directory.

Example `backend/.env` file:

```
OPENAI_API_KEY=<openai_api_key>
GOOGLE_CSE_ID=<cse_id>
GOOGLE_API_KEY=<google_api_key>
```

Second, run the server:

```
python main.py
```

Open [http://localhost:8088/docs](http://localhost:8000/docs) with your browser to see the Swagger UI of the API.


## Getting Started with frontend
Go to frontend directory

First if not installed, install the dependencies:

```
npm install
```

Second, run the development server:

```
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.