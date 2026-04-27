import ollama

def chat(message, history):
    history.append({
        "role": "user",
        "content": message
    })

    response = ollama.chat(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=history
    )

    reply = response["message"]["content"]

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply, history

def main():
    print("=" * 50)
    print("  J.A.R.V.I.S - Online")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    history = [
        {
            "role": "system",
            "content": """You are JARVIS, a highly intelligent personal AI assistant. 
You are helpful, precise, and slightly formal but friendly.
You assist with tasks, answer questions, and remember context within our conversation.
Keep responses concise unless asked for detail."""
        }
    ]
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "quit":
            print("JARVIS: Goodbye.")
            break
            
        if not user_input:
            continue
            
        print("JARVIS: ", end="", flush=True)
        reply, history = chat(user_input, history)
        print(reply)
        print()

if __name__ == "__main__":
    main()