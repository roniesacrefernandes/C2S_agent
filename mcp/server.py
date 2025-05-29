from mcp.server.fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server')

load_dotenv()

# Configurações do PostgreSQL
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")

required_vars = [PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE]
if not all(required_vars):
    logger.error("Todas as variáveis de ambiente PostgreSQL devem ser definidas.")
    raise ValueError("Variáveis de ambiente PostgreSQL não encontradas.")

logger.info(f"Conectando ao PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DATABASE}")

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco PostgreSQL.
    """
    try:
        connection = psycopg2.connect(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE
        )
        return connection
    except Exception as e:
        logger.error(f"Erro ao conectar ao PostgreSQL: {e}")
        raise

# Testa a conexão inicial
try:
    test_conn = get_db_connection()
    test_conn.close()
    logger.info("Conexão com PostgreSQL estabelecida")
except Exception as e:
    logger.error(f"Erro conexão PostgreSQL: {e}")
    raise

logger.info("Inicializando o servidor MCP SErver")    
mcp = FastMCP("mcp_server")

@mcp.resource("config://app")
def get_config():
    """
    Retorna a configuração do aplicativo.
    """
    logger.info("Obtendo configuração do aplicativo (config/app)")
    return {
        "name": "MCP Server PostgreSQL",
        "version": "1.0.0",
        "description": "Servidor MCP com PostgreSQL.",
        "author": "Ronie",
        "license": "my-license",
        "database": {
            "type": "PostgreSQL",
            "host": PG_HOST,
            "port": PG_PORT,
            "database": PG_DATABASE
        }
    }

@mcp.prompt()
def prompt(message: str):
    """
    Retorna o prompt do servidor.
    """
    logger.info("Obtendo prompt do servidor {message}")
    return f"Teste de prompt do servidor MCP: {message}"
    
@mcp.tool()
def buscar_por_marca(marca: str):
    """
    Busca automóveis por marca específica.
    """
    logger.info(f"Buscando automóveis da marca: {marca}")
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM automoveis WHERE LOWER(marca) LIKE LOWER(%s) ORDER BY ano DESC", (f"%{marca}%",))
        automoveis = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if automoveis:
            result = [dict(row) for row in automoveis]
            return {
                "automoveis": result,
                "total_encontrados": len(result),
                "mensagem": f"Encontrei {len(result)} automóvel da marca {marca.title()}!"
            }
        else:
            return {
                "automoveis": [],
                "total_encontrados": 0,
                "mensagem": f"Não encontrei nenhum automóvel da marca {marca.title()}"
            }
            
    except psycopg2.Error as e:
        logger.error(f"Erro PostgreSQL ao buscar por marca: {e}")
        return {"error": f"Erro de banco de dados: {str(e)}"}
    except Exception as e:
        logger.error(f"Erro geral ao buscar por marca: {e}")
        return {"error": str(e)}

@mcp.tool()
def buscar_por_modelo(modelo: str):
    """
    Busca automóveis por modelo específico.
    """
    logger.info(f"Buscando automóveis do modelo: {modelo}")
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM automoveis WHERE LOWER(modelo) LIKE LOWER(%s) ORDER BY ano DESC", (f"%{modelo}%",))
        automoveis = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if automoveis:
            result = [dict(row) for row in automoveis]
            return {
                "automoveis": result,
                "total_encontrados": len(result),
                "mensagem": f"Encontrei {len(result)} automóvel do modelo {modelo.title()}!"
            }
        else:
            return {
                "automoveis": [],
                "total_encontrados": 0,
                "mensagem": f"Não encontrei nenhum automóvel do modelo {modelo.title()}"
            }
            
    except psycopg2.Error as e:
        logger.error(f"Erro PostgreSQL ao buscar por modelo: {e}")
        return {"error": f"Erro de banco de dados: {str(e)}"}
    except Exception as e:
        logger.error(f"Erro geral ao buscar por modelo: {e}")
        return {"error": str(e)}

@mcp.tool()
def buscar_por_cor(cor: str):
    """
    Busca automóveis por cor específica.
    """
    logger.info(f"Buscando automóveis da cor: {cor}")
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM automoveis WHERE LOWER(cor) LIKE LOWER(%s) ORDER BY marca, modelo", (f"%{cor}%",))
        automoveis = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if automoveis:
            result = [dict(row) for row in automoveis]
            return {
                "automoveis": result,
                "total_encontrados": len(result),
                "mensagem": f"Encontrei {len(result)} automóvel(is) na cor {cor.title()}!"
            }
        else:
            return {
                "automoveis": [],
                "total_encontrados": 0,
                "mensagem": f"Não encontrei nenhum automóvel na cor {cor.title()}."
            }            
    except psycopg2.Error as e:
        logger.error(f"Erro PostgreSQL ao buscar por cor: {e}")
        return {"error": f"Erro de banco de dados: {str(e)}"}
    except Exception as e:
        logger.error(f"Erro geral ao buscar por cor: {e}")
        return {"error": str(e)}

@mcp.tool()
def buscar_por_preco(preco_minimo: float, preco_maximo: float = None):
    """
    Busca automóveis por faixa de preço. 
    """
    logger.info(f"Buscando automóveis por preço: {preco_minimo} - {preco_maximo}")
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        if preco_maximo:
            cursor.execute("SELECT * FROM automoveis WHERE preco BETWEEN %s AND %s ORDER BY preco ASC", (preco_minimo, preco_maximo))
        else:
            cursor.execute("SELECT * FROM automoveis WHERE preco >= %s ORDER BY preco ASC", (preco_minimo,))
        
        automoveis = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if automoveis:
            result = [dict(row) for row in automoveis]
            return {
                "automoveis": result,
                "total_encontrados": len(result),
                "mensagem": f"Encontrei {len(result)} automóvel"
            }
        else:
            return {
                "automoveis": [],
                "total_encontrados": 0,
                "mensagem": f"Não encontrei nenhum automóvel "
            }
            
    except psycopg2.Error as e:
        logger.error(f"Erro PostgreSQL ao buscar por preço: {e}")
        return {"error": f"Erro de banco de dados: {str(e)}"}
    except Exception as e:
        logger.error(f"Erro geral ao buscar por preço: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Iniciando o servidor MCP")

    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor MCP: {e}")
        raise   
