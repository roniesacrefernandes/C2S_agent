import asyncio
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
#from langchain_openai import ChatOpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID")


if not GROQ_API_KEY:
    raise ValueError("A variável de ambiente 'GROQ_API_KEY' não está definida no arquivo .env")

llm = ChatGroq(
    groq_api_key= GROQ_API_KEY,
    model=  GROQ_MODEL_ID  
)

# llm = ChatOpenAI(
#     model=OPENAI_MODEL_ID,
#     temperature=0,
#     api_key=OPENAI_API_KEY    
# )

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
mcp_config_path = os.path.join(root_dir, "mcp", "server.py")

try:
    print("Iniciando conexão com o servidor MCP...")
    # Configurar parâmetros do servidor
    server_params = StdioServerParameters(
        command="python",
        args=[mcp_config_path],
    )
except Exception as e:
    print(f"AVISO: Não foi possível conectar ao MCP ou obter ferramentas: {e}")
    print("O agente continuará SEM ferramentas MCP.")


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)

            messages = [
            SystemMessage(
            content="Você é um agente automotivo especializado em ajudar usuários a encontrar informações sobre veículos, como marcas, modelos, anos, quilometragem e outros detalhes relevantes."
            )
            ] 
            print('Bem-vindo ao agente automotivo!')

            while True:
                user_input = await asyncio.to_thread(input, "\nVocê: ")

                if user_input.lower() in ["sair", "exit", "quit"]:
                    print("Saindo do agente automotivo.")
                    break

                messages.append(HumanMessage(content=user_input))
                
                try:
                    result = await agent.ainvoke({"messages": messages})

                    if isinstance(result, dict) and "messages" in result:
                        last_message = result["messages"][-1]
                    elif isinstance(result, dict) and "output" in result:
                        last_message = HumanMessage(content=result["output"]) 
                    else:
                        last_message = result 

                    messages.append(last_message)
                    
                    if hasattr(last_message, 'content') and last_message.content:
                        print(f"\nAgente: {last_message.content}")
                    else:
                        print("\nAgente: (Sem respostas)")
                        print(f"Detalhes da resposta: {last_message}") 

                except Exception as e:
                    print(f"\nErro ao processar solicitação: {e}")

                    if messages and isinstance(messages[-1], HumanMessage):
                        messages.pop()
                    print("Por favor, tente novamente.")
                
if __name__ == "__main__":
    asyncio.run(main())
