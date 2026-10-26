from .tools.registry import TOOLS
from .tools.executor import execute_tool
from .client import create_llm_client

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
