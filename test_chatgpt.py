import api_backend
import time

print("[+] Starting ChatGPT remote browser...")
api_backend.start_chat_gpt()

# Wait a few seconds to ensure Chrome starts properly
time.sleep(5)

# Test 1: Ask ChatGPT a simple question
question1 = "What is GPT-4?"
print(f"[+] Asking ChatGPT: {question1}")
response1 = api_backend.make_gpt_request(question1)
print(f"[ChatGPT Response]: {response1}\n")

# Test 2: Ask another question
question2 = "Who created OpenAI?"
print(f"[+] Asking ChatGPT: {question2}")
response2 = api_backend.make_gpt_request(question2)
print(f"[ChatGPT Response]: {response2}\n")

# Test 3: Ask a third question
question3 = "What is the capital of France?"
print(f"[+] Asking ChatGPT: {question3}")
response3 = api_backend.make_gpt_request(question3)
print(f"[ChatGPT Response]: {response3}\n")

# Stop ChatGPT session
print("[+] Stopping ChatGPT remote browser...")
api_backend.stop_chat_gpt()

print("[✅] Test completed successfully!")
