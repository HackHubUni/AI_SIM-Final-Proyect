import json
import google.generativeai as genai

# Configure API Key
GOOGLE_API_KEY = "AIzaSyDKZl8gFeDs6X0draN3nd3kV5Se0l1FCLg"
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key=GOOGLE_API_KEY)

# Example knowledge base JSON structure
knowledge_base = {
    "Company A": {
        "Revenue": "$1,000,000",
        "Profit": "$100,000",
        "Location": "New York"
    },
    "Company B": {
        "Revenue": "$800,000",
        "Profit": "$80,000",
        "Location": "California"
    },
    "Company C": {
        "Revenue": "$1,200,000",
        "Profit": "$150,000",
        "Location": "London"
    }
}


def load_knowledge_base(json_file):
    with open(json_file, "r") as file:
        knowledge_base = json.load(file)
    return knowledge_base

# Function to ask questions to the language model
def ask_question(model, question, knowledge_base):
    prompt = "Knowledge Base: "
    for entity, states in knowledge_base.items():
        prompt += f"\n{entity}:"
        for variable, result in states.items():
            prompt += f"\n  {variable}: {result}"
    
    prompt += f"\nQuestion: {question}"
    print(prompt)
    response = model.generate_content(prompt)
    return response.text

# Example question
question = "Which company had the highest revenue?"
answer = ask_question(model, question, knowledge_base)
print(f"Answer: {answer}")
