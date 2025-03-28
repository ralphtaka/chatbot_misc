from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, Optional
import prompts_logic

class LLMState(TypedDict):
    user_input: Optional[str]
    emotion: Optional[str]
    response: Optional[str]
    user_history: Optional[str]

def clear_state(state: LLMState):
    state["user_input"] = None
    state["emotion"] = None
    state["response"] = None
    state["user_history"] = None

def decide_next_step(state: LLMState):
    """決定下一步要執行的節點"""
    return "song_recommendation" if state["emotion"] is not None else "chatbot_response"

def loop_to_chatbot(state:LLMState):
    return "chatbot_response" if state["response"] == "找不到" else "END"

class LanggraphLogic:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        # 建立 LangGraph
        workflow = StateGraph(LLMState)
        workflow.add_node("emotion_analysis", self.analyze_emotion)
        workflow.add_node("song_recommendation", self.recommend_song)
        workflow.add_node("chatbot_response", self.chatbot_response)
        workflow.set_entry_point("emotion_analysis")
        workflow.add_conditional_edges("emotion_analysis", decide_next_step)
        workflow.add_conditional_edges("song_recommendation", loop_to_chatbot)

        # Compile
        self.executor = workflow.compile()

    def analyze_emotion(self, state: LLMState):
        """分析使用者的情緒"""
        user_history = state["user_history"]
        emotion = prompts_logic.get_analyze_emotion_result(self.llm, user_history)

        if "無法判斷" in emotion:
            return {"emotion": None}  # 繼續對話
        else:
            return {"emotion": emotion}

    def recommend_song(self, state: LLMState):
        """根據情緒推薦歌曲"""
        emotion = state["emotion"]
        recommendation = prompts_logic.get_recommend_song_result(self.llm, emotion)

        if "找不到" in recommendation:
            return {"response": "找不到"}
        else:
            # clear all the items from state
            clear_state(state)
            return {"response": recommendation}

    def chatbot_response(self, state: LLMState):
        """與使用者閒聊"""
        user_input = state["user_input"]
        chat_message = prompts_logic.get_chatbot_response_result(self.llm, user_input)
        return {"response": chat_message}

    def assistant_logic(self, user_input: str, user_history: str):
        # 執行 LangGraph 流程
        response_state = self.executor.invoke({"user_input": user_input, "user_history": user_history})
        return response_state["response"]
