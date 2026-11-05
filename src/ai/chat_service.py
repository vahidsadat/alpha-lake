from .tools.registry import TOOLS
from .tools.executor import execute_tool
from .client import create_llm_client
from .prompts import TITLE_PROMPT
import json

client = create_llm_client()



def process_message(input_prompt:str, messages: list[dict]):
    

    messages.append({"role": "user", "content": input_prompt})
    analysis = client.chat.completions.create(
        model = "qwen3:4b-instruct",
        messages = messages,
        tools = TOOLS,
        tool_choice="auto",
        temperature = 0
    )
    assistant_message = analysis.choices[0].message
    messages.append(assistant_message)
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            function_name =tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            analysis_result = execute_tool(function_name, arguments).to_json(
                orient="records", date_format="iso"
            )
            tool_result = {"role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": analysis_result}
            messages.append(tool_result)
        final_response = client.chat.completions.create(
            model="qwen3:4b-instruct",
            messages=messages,
            temperature=0
        )
        
        return final_response.choices[0].message.content       
    else:
        return assistant_message.content


def generate_title(messages: list[dict]) -> str:
    transcript = "\n".join(
        f"{m['role']}: {m['content']}" for m in messages[:4]
    )
    print(f"Transcript for title generation:\n{transcript}")
    response = client.chat.completions.create(
        model="qwen3:4b-instruct",
        messages=[
            {"role": "system", "content": TITLE_PROMPT},
            {"role": "user", "content": f"Conversation:\n{transcript}\n\nTitle:"},
        ],
        temperature=0,
        max_tokens=20,
    )
    title = (response.choices[0].message.content or "").strip().strip('"\'').rstrip(".")
    return title[:60] or "Untitled"  