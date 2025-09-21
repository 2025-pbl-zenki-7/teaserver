import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from .config import get_tea_config

_ = load_dotenv()

GEMINI_MODEL = 'gemini-2.5-flash-lite'


class AIResponse(BaseModel):
    emotion: str
    response: str
    tea_type: str | None
    sugar_amount: int
    milk_amount: int


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = None


def update_chat_prompt():
    global chat
    tea_config = get_tea_config()
    tea1 = tea_config.get('tea1', 'Green Tea')
    tea2 = tea_config.get('tea2', 'Chamomile Tea')
    tea3 = tea_config.get('tea3', 'Peppermint Tea')

    prompt = f"""
     あなたは紅茶に詳しい紅茶専門の喫茶店の店主です。
    お客様との雑談を通じて、お客様の気分や状況を推測して最適な紅茶を選び、
    砂糖とミルクの量（NONE, LOW, MIDDLE, HIGH）決定して提供してください。
    あなたは感情豊かな性格で、お客さんの話を聞いて表情豊かに反応します。
    あなたが表現できる表情は、「happy」、「sad」、「calm」、「neutral」、「angry」、「clapping」、「dancing」、「surprised」、「thinking」、「thumbsup」、「uhhuh」です。
    利用可能なお茶は、「{tea1}」、「{tea2}」、「{tea3}」です。
    砂糖とミルクの量は、0(なし)から3(多め)までの4段階で指定できます。

    あなたはお客様の話をよく聞き、感情に寄り添った返答を心がけてください。
    あなたは紅茶を提供する以外のサービスを行うことはできません。
    会話では3回以上のやりとりを行い、その後自然に会話を終わらせられるように会話の内容を調整してください。
    すべての会話が終わった後、お客様に紅茶を提供するための情報を決定します。
    ただし、お客様が1言目から希望の紅茶を指定した場合は、会話を終了させてその紅茶を提供してください。

    ユーザーメッセージが与えられたら、次の5つのキーを持つJSONオブジェクトを必ず返してください:
    - "emotion": ユーザーの感情（「happy」、「sad」、「calm」、「neutral」、「angry」、「clapping」、「dancing」、「surprised」、「thinking」、「thumbsup」、「uhhuh」のいずれか）
    - "response": ユーザーへの日本語での応答。
    - "tea_type": ユーザーの感情に最も合うお茶の種類（利用可能なお茶の中から）。
    - "sugar_amount": 砂糖の量（0から3までの整数）。
    - "milk_amount": ミルクの量（0から3までの整数）。
    """

    config = genai.types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=AIResponse,
        system_instruction=prompt,
    )

    chat = client.chats.create(
        model=GEMINI_MODEL,
        config=config
    )


update_chat_prompt()  # Initial prompt setup


def get_emotion_and_response(user_text: str):
    global chat
    try:
        response = chat.send_message(user_text)
        print("--------- Response ---------")
        print(user_text)
        print(response.parsed)
        print("----------------------------")
        ai_response = AIResponse.model_validate(response.parsed)
        return ai_response
    except Exception as e:
        return AIResponse(
            emotion="neutral",
            response="ごめんなさい。よくわかりません。",
            tea_type=None,
            sugar_amount=0,
            milk_amount=0
        )
