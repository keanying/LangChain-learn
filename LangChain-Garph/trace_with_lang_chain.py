import os
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['OPENAI_BASE_URL'] = 'https://api.91ai.me/v1'
os.environ['LANGSMITH_API_KEY'] = 'lsv2_pt_65486ff7f8f3488b86fba4d4108dfec8_c86'
os.environ['OPENAI_API_KEY'] = 'sk-zmTlAse1jQo2r04WBeC616Ed62A64b'
os.environ["SERPAPI_API_KEY"] = 'eeb9669dba516b9173fc5791802c46e772011974'

@tool
def search(query: str):
    """Call to surf the web."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


tools = [search]
tool_node = ToolNode(tools)
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"


def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge("__start__", "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", 'agent')
app = workflow.compile()
final_state = app.invoke({"messages": [HumanMessage(content="旧金山的天气怎么样?")]},
                         config={"configurable": {"thread_id": 42}})
print(final_state["messages"][-1].content)
