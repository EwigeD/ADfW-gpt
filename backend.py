from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key,
                       openai_api_base = "https://api.aigc369.com/v1")
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]

# print(get_chat_response("牛顿提出过哪些知名的定律？", memory, openai_api_key))
# print(get_chat_response("我上一个问题问的是？", memory, openai_api_key))