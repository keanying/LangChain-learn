import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType

os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['OPENAI_BASE_URL'] = 'https://api.91ai.me/v1'
os.environ['LANGSMITH_API_KEY'] = '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'
os.environ['OPENAI_API_KEY'] = 'sk-zmTlAse1jQo2r04WBeC616Ed62A64bC38190F50f8c8eDc0f'
os.environ["SERPAPI_API_KEY"] = 'eeb9669dba516b9173fc5791802c46e7720119745194a1cf27650971c38619e3'

# 加载 OpenAI 模型
llm = OpenAI(temperature=0, max_tokens=2048)

# 加载 serpapi 工具
tools = load_tools(["serpapi"])

# 如果搜索完想再计算一下可以这么写
# tools = load_tools(['serpapi', 'llm-math'], llm=llm)

# 如果搜索完想再让他再用python的print做点简单的计算，可以这样写
# tools=load_tools(["serpapi","python_repl"])

# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 运行 agent
agent.run("今天的日期和今天北京的天气")
