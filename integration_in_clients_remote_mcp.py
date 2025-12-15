import asyncio
import os

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

from models import get_lc_o_ali_model_client, ALI_TONGYI_API_KEY_OS_VAR_NAME

load_dotenv()
api_key=os.getenv(ALI_TONGYI_API_KEY_OS_VAR_NAME)
#print('api_key', api_key)
async def main():
    # 客户端集成多个mcp服务
    client = MultiServerMCPClient(
        {
            "Stock": {
                "url": "http://localhost:8000/mcp",
                "transport": "sse",
            },
            "MCP_WebSearch": {
                "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse",
                "transport": "sse",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            }
        }
    )

    tools = await client.get_tools()
    for index, tool in enumerate(tools):
        print(f"第{index + 1}个工具：", tool)

    llm = get_lc_o_ali_model_client()

    print(f"=================准备实际的业务工作=================")

    agent = create_agent(
        llm,
        tools
    )

    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "分析一下600795这个怎么样"}]}
    # )
    # print("分析结果为:", math_response)

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "泸州泸县的景点有哪些"}]}
    )
    print("分析结果为:", math_response)

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())