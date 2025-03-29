from langchain_openai import ChatOpenAI

def get_llm_result_content(llm: ChatOpenAI, prompt: str) -> str:
    return llm.invoke(prompt).content

def get_analyze_emotion_result(llm: ChatOpenAI, user_history: str):
    prompt = f"分析使用者輸入的對話中的情緒，分成以下這五類：快樂,悲傷,憤怒,放鬆,興奮\n若無法判斷則回應「無法判斷」\n使用者說的話: {user_history}\n 情緒："
    return get_llm_result_content(llm, prompt)

def get_recommend_song_result(llm: ChatOpenAI, emotion: str):
    prompt = """你是一個DJ，請依照使用者輸入的情緒幫忙從以下的歌曲挑選推薦的歌曲，如果找不到適合的歌曲則回應「找不到」

            歌曲，藝人和其對應情緒：
            歌名:Happy;藝人:Pharrell William;情緒:快樂
            歌名:Someone Like You;藝人:Adele;情緒:悲傷
            歌名:Smells Like Teen Spirit;藝人:Nirvana;情緒:憤怒
            歌名:Weightless;藝人:Marconi Union;情緒:放鬆
            歌名:I Gotta Feeling;藝人:Black Eyed Peas;情緒:興奮

            """ + str(emotion)
    return get_llm_result_content(llm, prompt)

def get_chatbot_response_result(llm: ChatOpenAI, user_input: str):
    prompt = f"你是一個善於聆聽跟發問的Chatbot，現在希望你針對使用者說的話提出適當的回應跟問題。\n使用者說的話：{user_input}"
    return get_llm_result_content(llm, prompt)