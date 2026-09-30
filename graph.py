from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents import manager_agent, generate_answer
from rag import retrieve


# ============================================================
# STATE
# ============================================================
class AgentState(TypedDict):
    question: str
    category: str
    answer: str
    context: str
    sources: list


# ============================================================
# MANAGER NODE
# ============================================================
def manager_node(state, chunks, metadata, index):
    question = state["question"]
    category = manager_agent(question)

    department_map = {
        "HR": "hr",
        "TECHNICAL": "technical",
        "PROJECT": "projects",
        "GENERAL": None,
    }
    department = department_map[category]

    results = retrieve(
        question, chunks, metadata, index, department=department, top_k=5
    )

    context_parts = []
    sources = []

    for result in results:
        metadata_item = result["metadata"]
        context_parts.append(
            f"""
Source: {metadata_item['source']}
Page: {metadata_item['page']}
Department: {metadata_item['department']}
Content: {result['text']}
"""
        )
        sources.append(metadata_item)

    context = "\n".join(context_parts)

    return {
        "category": category,
        "context": context,
        "sources": sources,
    }


# ============================================================
# ANSWER NODE
# ============================================================
def answer_node(state):
    category = state["category"]

    agent_name_map = {
        "HR": "HR specialist agent",
        "TECHNICAL": "Technical specialist agent",
        "PROJECT": "Project specialist agent",
        "GENERAL": "General company knowledge agent",
    }
    agent_name = agent_name_map[category]

    answer = generate_answer(state["question"], state["context"], agent_name)

    return {"answer": answer}


# ============================================================
# BUILD GRAPH
# ============================================================
def create_graph(chunks, metadata, index):
    graph = StateGraph(AgentState)

    # --------------------------------------------------------
    # Wrapper node
    # --------------------------------------------------------
    def manager_wrapper(state):
        return manager_node(state, chunks, metadata, index)

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------
    graph.add_node("manager", manager_wrapper)
    graph.add_node("answer", answer_node)

    # --------------------------------------------------------
    # Edges
    # --------------------------------------------------------
    graph.add_edge(START, "manager")
    graph.add_edge("manager", "answer")
    graph.add_edge("answer", END)

    return graph.compile()
