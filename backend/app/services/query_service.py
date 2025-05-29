from rag_query_function import query_rag
from mcp_query_function import query_mcp


# 利用model参数，让查询的时候用户可以选择查询方式
def query_by_question(question: str, model: str = "RAG"):
    if model == "RAG":
        return query_rag(question)
    else:
        return query_mcp(question)

if __name__ == "__main__":
    question = input("请输入您的问题：")
    model = input("请选择您的查询方式（RAG或MCP）：")
    answer = query_by_question(question, model)
    print(answer)