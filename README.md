# 🚗 Servidor MCP Automóveis

Servidor MCP (Model Context Protocol) para gerenciar e analisar dados de automóveis com PostgreSQL, incluindo ferramentas avançadas de análise estatística, geração de gráficos e processamento de imagens.

## 🔧 Funcionalidades

### Busca e Consulta
- ✅ Listar todos os automóveis
- 🔍 Buscar por marca, modelo, ano, cor

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- Dependências Python (veja `requirements.txt`)

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd mcp-automoveis
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
Crie um arquivo `.env`:
```env
PG_USER=seu_usuario
PG_PASSWORD=sua_senha
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=automoveis_db
```

4. **Configure o banco PostgreSQL**
```sql
-- Crie a banco automoveis_db

CREATE DATABASE automoveis_db;

-- Insira dados executando o script python faker_data.py 
```
```bash
python faker_data.py
```

## ▶️ Como Executar

### Iniciar o Servidor MCP
```bash
python mcp_server.py
```
## 🛠️ Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `buscar_por_marca` | Busca por marca específica |
| `buscar_por_modelo` | Busca por modelo |
| `buscar_por_ano` | Busca por faixa de anos |
| `buscar_por_cor` | Busca por cor |
| `buscar_por_preco` | Busca por faixa de preço |

## 📊 Exemplos de Uso

### Buscar por marca
```python
await client.call_tool("buscar_por_marca", {"marca": "Toyota"})
```

## 📦 Dependências

```txt
fastmcp
psycopg2-binary
python-dotenv
pandas
numpy
matplotlib
seaborn
Pillow
```
## 🤝 Contribuição
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido por:** Ronie  
**Versão:** 1.0.0