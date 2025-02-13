from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from transformers import pipeline
import pandas as pd
import uvicorn
from pathlib import Path

app = FastAPI()

cocktail_df = pd.read_csv("cocktails.csv")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.from_texts(cocktail_df["ingredients"].tolist(), embedding_model)

generator = pipeline("text-generation", model="gpt2", pad_token_id=50256, max_new_tokens=100)
llm = HuggingFacePipeline(pipeline=generator)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_db.as_retriever())

user_preferences = {}


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = Path("static/index.html")
    if index_path.exists():
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    else:
        raise HTTPException(status_code=404, detail="HTML file not found")


@app.post("/chat/")
def chat_endpoint(request: ChatRequest):
    try:
        user_id = request.user_id
        message = request.message.lower()

        if "i like" in message:
            ingredient = message.split("like")[-1].strip()
            if user_id not in user_preferences:
                user_preferences[user_id] = []
            user_preferences[user_id].append(ingredient)
            return {"response": f"Got it! I saved your preference: {ingredient}"}

        if "my favourite ingredients" in message:
            if user_id in user_preferences and user_preferences[user_id]:
                preferences = ', '.join(user_preferences[user_id])
                return {"response": f"Your favourite ingredients are: {preferences}"}
            else:
                return {"response": "You haven't shared any favourite ingredients yet."}

        if "cocktails containing" in message:
            ingredient = message.split("cocktails containing")[-1].strip()

            filter_type = None
            if "non-alcoholic" in message:
                filter_type = "Non alcoholic"
            elif "alcoholic" in message:
                filter_type = "Alcoholic"

            filtered_cocktails = cocktail_df[cocktail_df['ingredients'].str.contains(ingredient, case=False, na=False)]

            if filter_type:
                filtered_cocktails = filtered_cocktails[
                    filtered_cocktails['category'].str.contains(filter_type, case=False, na=False)]

            if not filtered_cocktails.empty:
                cocktail_list = []
                for index, row in filtered_cocktails.head(5).iterrows():
                    cocktail_list.append(f"{row['name']} – {row['ingredients']}")
                return {"response": "\n".join(cocktail_list)}
            else:
                return {"response": f"Sorry, I couldn't find any cocktails containing {ingredient}."}

        if "recommend" in message:
            if user_id in user_preferences and user_preferences[user_id]:
                preferences = user_preferences[user_id]

                filtered_cocktails = cocktail_df[
                    cocktail_df['ingredients'].str.contains('|'.join(preferences), case=False, na=False)]

                if not filtered_cocktails.empty:
                    cocktail_list = []
                    for index, row in filtered_cocktails.head(5).iterrows():
                        cocktail_list.append(f"{row['name']} – {row['ingredients']}")
                    return {"response": "\n".join(cocktail_list)}
                else:
                    return {"response": "Sorry, I couldn't find any recommendations based on your preferences."}
            else:
                return {"response": "You haven't shared your favourite ingredients yet."}

        response = qa_chain.invoke(message)
        return {"response": response.get('result', 'Sorry, I couldn\'t find an answer to your question.')}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
