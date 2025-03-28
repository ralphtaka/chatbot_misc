from langchain_openai import ChatOpenAI
import prompts_logic

class SimpleLogic:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    # 使用 LLM 進行情緒分析
    def analyze_emotion(self, user_history):
        emotion = prompts_logic.get_analyze_emotion_result(self.llm, user_history)
        if "無法判斷" in emotion:
            return "無法判斷"
        else:
            return emotion

    # 如果有情緒偵測則推歌
    def recommend_song(self, emotion):
        recommendation = prompts_logic.get_recommend_song_result(self.llm, emotion)
        if "找不到" in recommendation:
            return "找不到"
        else:
            return recommendation

    # 如果偵測不到情緒或者找不到對應的歌則閒聊
    def chatbot_response(self, user_input):
        chat_message = prompts_logic.get_chatbot_response_result(self.llm, user_input)
        return chat_message

    def assistant_logic(self, user_input, user_history):
        emotion = self.analyze_emotion(user_history)
        if "無法判斷" in emotion:
            return self.chatbot_response(user_input)
        else:
            recommendation = self.recommend_song(emotion)
            if "找不到" in recommendation:
                return self.chatbot_response(user_input)  # 呼叫chat功能
            else:
                return recommendation