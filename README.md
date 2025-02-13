
# Adviser

This project is a simple FastAPI-based chatbot application that allows users to interact with a cocktail recipe database. The chatbot can suggest cocktails based on user preferences, ingredients, and categories (alcoholic or non-alcoholic). Additionally, it can provide recommendations based on previously saved favorite ingredients.

## Features:
- **Save favorite ingredients**: Users can share ingredients they like, and the bot will remember them.
- **Ask for cocktails containing ingredients**: Users can ask for cocktails containing specific ingredients, and filter by alcohol type.
- **Get cocktail recommendations**: Based on previously saved favorite ingredients, the bot will recommend cocktails.
- **General questions**: The bot can also answer general questions about cocktails using a language model.


## Get dataset 

To download the dataset, run the following bash command:

```bash
#!/bin/bash
curl -L -o cocktails.zip https://www.kaggle.com/api/v1/datasets/download/aadyasingh55/cocktails
```

After downloading, move the `cocktails.zip` file to your project folder and unzip it:

```bash
unzip cocktails.zip -d .  # This will extract the contents into the current directory
```

### Set up a Virtual Environment
Create a virtual environment for the project:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On macOS/Linux:

```bash
source .venv/bin/activate
```

- On Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies:
To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### How to Run the Server:
To start the server, use Uvicorn:

```bash
uvicorn main:app --reload
```

The server will be accessible at `http://127.0.0.1:8000`.

### How to Use the Chatbot:
The chatbot provides several commands you can use to interact with it. Here are the main options:

#### 1. **Save Favorite Ingredient**:
You can tell the bot your favorite ingredients by saying something like:
```
I like lime
```
This will save the ingredient to your preferences. You can share multiple ingredients over time.

#### 2. **View My Favorite Ingredients**:
If you want to see the ingredients you've shared with the bot, simply say:
```
My favourite ingredients
```
The bot will list the ingredients you've saved.

#### 3. **Find Cocktails Containing an Ingredient**:
You can ask for cocktails containing a specific ingredient. with llm
```
What cocktails contain juice?
```
or with info from dataset
```
What are the 5 cocktails containing lemon?
```

#### 4. **Get Cocktail Recommendations**:
You can ask the bot to recommend cocktails based on your saved preferences:
```
Recommend me a cocktail
```

#### 5. **General Cocktail Questions**:
You can ask general questions about cocktails:
```
What is a Margarita?
```
This will use a language model to provide an answer.

### API Endpoints:

#### 1. **Root Endpoint** (`GET /`):
The root endpoint serves the HTML interface for the chatbot.

#### 2. **Chat Endpoint** (`POST /chat/`):
You can send a `POST` request to `/chat/` with a JSON body containing the `user_id` and the `message`. For example:

```json
{
  "user_id": "user123",
  "message": "What cocktails contain juice?"
}
```

### Example Request to `/chat/`:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user123",
  "message": "What are the cocktails containing juice?"
}'
```

### Example Response:

```json
{
  "response":"Avalon – ['Vodka', 'Pisang Ambon', 'Apple juice', 'Lemon juice', 'Lemonade']\nApello – ['Orange juice', 'Grapefruit juice', 'Apple juice', 'Maraschino cherry']\nAfterglow – ['Grenadine', 'Orange juice', 'Pineapple juice']\nBora Bora – ['Pineapple juice', 'Passion fruit juice', 'Lemon juice', 'Grenadine']\nBarracuda – ['Rum', 'Galliano', 'Pineapple Juice', 'Lime Juice', 'Prosecco'] "
}
```

---

### Folder Structure:

```
Adviser/
│
├── main.py                  # FastAPI application
├── cocktails.csv            # Cocktail data (name, ingredients, category, etc.)
├── static/
│   └── index.html           # HTML interface for the chatbot
├── requirements.txt         # List of required dependencies
└── README.md                # This file
```

---

## Development Notes:

- **Data Source**: The data comes from a `cocktails.csv` file, which contains information about cocktail names, ingredients, and categories (e.g., alcoholic or non-alcoholic).
- **Vector Store**: The chatbot uses FAISS (Facebook AI Similarity Search) for fast similarity search and HuggingFace embeddings to process ingredient-based queries.
- **Language Model**: The chatbot uses GPT-2 (via HuggingFace transformers) for answering general cocktail questions.

