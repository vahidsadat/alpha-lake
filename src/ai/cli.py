from chat_service import process_message

def main():
    while True:

        input_prompt = input("Enter your question (or type 'exit' to quit): ")
        if input_prompt.lower() == 'exit':
            break
        response = process_message(input_prompt)

        print(response)

if __name__ == "__main__":
    main()