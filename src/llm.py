from langchain_openai import ChatOpenAI

def get_llm(model_name: str, base_url: str, api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name, 
        base_url=base_url,
        api_key=api_key,
        extra_body={"enable_thinking": False}
    )