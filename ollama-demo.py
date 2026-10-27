from ollama import chat

response = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Explain kubernetes pod eviction"
        }
    ]
)
# FIXED: Using dot notation to access the text response
print(response.message.content)
