from .chat_service import process_message
from .prompts import SYSTEM_PROMPT

def main():
    while True:
        messages = [
                    {"role": "system", "content" : SYSTEM_PROMPT}
                ]
        input_prompt = input("Enter your question (or type 'exit' to quit): ")
        if input_prompt.lower() == 'exit':
            break
        response = process_message(input_prompt,messages)

        print(response)

if __name__ == "__main__":
    main()