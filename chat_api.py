from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), verbose=True)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


# 逐步迭代提问
def get_model_response(conversation_history, new_question, date_model='gpt-3.5-turbo'):
    # 将新问题添加到对话历史
    conversation_history.append({"role": "user", "content": new_question})

    # 使用OpenAI API获取模型回答
    response = client.chat.completions.create(
        model=date_model,  # 选择合适的引擎
        messages=conversation_history
    )

    # 从API响应中提取模型的回答
    model_response = response.choices[0].message.content

    # 将模型的回答添加到对话历史
    conversation_history.append({"role": "assistant", "content": model_response})

    return model_response
