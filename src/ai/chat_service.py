from tools.registry import TOOLS
from tools.executor import execute_tool
from prompts import SYSTEM_PROMPT
from client import create_llm_client

import json

client = create_llm_client()

messages = [
            {"role": "system", "content" : SYSTEM_PROMPT}
        ]


def process_message(input_prompt:str):
    messages.append({"role": "user", "content": input_prompt})
    analize = client.chat.completions.create(
        model = "qwen3:4b-instruct",
        messages = messages,
        tools = TOOLS,
        tool_choice="required",
        temperature = 0
    )
    assistant_message = analize.choices[0].message
    messages.append(assistant_message)
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            function_name =tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            analysis_result = execute_tool(function_name, arguments).to_json(
                orient="records", date_format="iso"
            )
            messages.append(
                {"role": "tool",
                "tool_call_id": tool_call.id,
                "content": analysis_result}
            )
            final_response = client.chat.completions.create(
                model="qwen3:4b-instruct",
                messages=messages
            )
            final_message = final_response.choices[0].message

            messages.append(final_message)
        return final_response.choices[0].message.content       
    else:
        raise ValueError(f"No tool calls found in the assistant's message. {assistant_message.content}")
