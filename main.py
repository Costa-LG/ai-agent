from collections.abc import Callable
import sys
import os
from openai import OpenAI
from prompts import system_prompt
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionToolMessageParam
from openai.types.completion_usage import CompletionUsage
from call_function import available_functions, call_function
import argparse

def load_api_key() -> str:
    load_dotenv()
    api_key:str|None = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("failed to load api_key")
    return api_key

def format_use(prompt: str, usage: CompletionUsage|None, response: str|None) -> str:
    if not usage or not response:
        raise RuntimeError("failed to access free model")

    input_information: str = f"User prompt: {prompt}\n"

    prompt_tokens:int = usage.prompt_tokens
    completion_tokens:int = usage.completion_tokens
    usage_information:str = f"Prompt tokens: {prompt_tokens}\nResponse tokens: {completion_tokens}\n"

    response_information = f"Response: {response}\n"
    return input_information + usage_information + response_information

def load_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()

def chat() -> Callable:
    count:int = 0

    def inner_func(messages, client, args):
        nonlocal count
        count += 1
        if count >= 20:
            raise Exception("max tries reached")

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                if result_message["content"] is None:
                    raise Exception("empty content returned")
                messages.append(ChatCompletionToolMessageParam(role="tool", tool_call_id=tool_call.id, content=result_message["content"]))
        else:
            if args.verbose:
                messages.append(ChatCompletionSystemMessageParam(role="system", content=format_use(args.user_prompt, response.usage, message.content)))
            else:
                messages.append(ChatCompletionSystemMessageParam(role="system", content=message.content))
            return messages
        return inner_func(messages, client, args)
    return inner_func

def main():
    try:
        args = load_parser()

        api_key = load_api_key()
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        messages:list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=args.user_prompt),
        ]

        conversation = chat()
        messages = conversation(messages, client, args)
        print(f"Final response:\n{messages[-1]["content"]}")
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()

