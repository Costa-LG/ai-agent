import os
from openai import OpenAI
from prompts import system_prompt
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from openai.types.completion_usage import CompletionUsage
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


def main():
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
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if args.verbose:
        print(format_use(args.user_prompt, response.usage, response.choices[0].message.content))
    else:
        print(response.choices[0].message.content)
if __name__ == "__main__":
    main()
