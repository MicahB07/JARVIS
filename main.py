import ollama
import yaml 

def build_system_prompt(config):
    base_prompt = config["system_prompt"]
    capabilities = config["capabilities"]

    capability_rules = []

    if not capabilities["internet_access"]:
        capability_rules.append("- You do not have internet access. Never pretend you do.")
    else:
        capability_rules.append("- You have internet access and can search for current information.")
    
    if not capabilities["calendar_access"]:
        capability_rules.append("- You do not have access to the user's calendar.")
    else:
        capability_rules.append("- You have access to the user's calendar.")
        
    if not capabilities["screen_vision"]:
        capability_rules.append("- You cannot see the user's screen.")
    else:
        capability_rules.append("- You can see the user's screen when asked.")

    if not capabilities["persistent_memory"]:
        capability_rules.append("- You have no memory of previous sessions. This conversation only.")
    else:
        capability_rules.append("- You have persistent memory of previous conversations.")

    capability_section = "\nCURRENT CAPABILITIES:\n" + "\n".join(capability_rules)
    
    return base_prompt + capability_section


def chat(message, history, model_name):
    history.append({
        "role": "user",
        "content": message
    })

    response = ollama.chat(
        model=model_name,
        messages=history
    )

    reply = response["message"]["content"]

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply, history

def main():
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)
    
    model_name = data["model"]["fast_model"]
    system_prompt = build_system_prompt(data)

    print("=" * 50)
    print("  J.A.R.V.I.S - Online")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    history = [
        {
            "role": "system",
            "content": system_prompt
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
        reply, history = chat(user_input, history, model_name)
        print(reply)
        print()

if __name__ == "__main__":
    main()



