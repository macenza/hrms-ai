import requests

url = "http://127.0.0.1:8000/assistant/chat"
payload = {
    "user_id": 9999,
    "role": "manager",
    "conversation_id": "test-conv-id",
    "message": "Hello"
}

# First, try to create conversation to make sure it exists
requests.post("http://127.0.0.1:8000/assistant/conversation/new", json={
    "user_id": 9999,
    "role": "manager"
})

# Note: The new endpoint returns a conversation_id. Let's get it.
res = requests.post("http://127.0.0.1:8000/assistant/conversation/new", json={
    "user_id": 9999,
    "role": "manager"
})
conv_id = res.json()["conversation_id"]

payload["conversation_id"] = conv_id

response = requests.post(url, json=payload)
print("STATUS CODE:", response.status_code)
print("RESPONSE:", response.json())
