import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(api_key=GEMINI_API_KEY, model="gemini-2.5-pro", temperature=0.3)

class WaterIntakeAgent:
     def __init__(self):
        self.history = []
     
     
     def analyze_intake(self, intake_ml):
        
        prompt =  f"""
        You are a water intake tracker. You are given the amount of water a person has consumed in ml.
        Provide a hydration status is well or not.
        Also suggest if they need to drink more water."""

        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    


if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydation Status: {feedback}")

     

