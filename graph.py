from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import (
    analyze_intent,
    respond_general,
    search_product,
    process_refund,
    handle_payment,
    handle_unknown_request,
    finalize_response,
    route_by_intent,
)


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("analyze_intent", analyze_intent)
    builder.add_node("respond_general", respond_general)
    builder.add_node("search_product", search_product)
    builder.add_node("process_refund", process_refund)
    builder.add_node("handle_payment", handle_payment)
    builder.add_node("handle_unknown_request", handle_unknown_request)
    builder.add_node("finalize_response", finalize_response)

    builder.add_edge(START, "analyze_intent")

    builder.add_conditional_edges(
        "analyze_intent",
        route_by_intent,
        {
            "respond_general": "respond_general",
            "search_product": "search_product",
            "process_refund": "process_refund",
            "handle_payment": "handle_payment",
            "handle_unknown_request": "handle_unknown_request",
        },
    )

    builder.add_edge("respond_general", "finalize_response")
    builder.add_edge("search_product", "finalize_response")
    builder.add_edge("process_refund", "finalize_response")
    builder.add_edge("handle_payment", "finalize_response")
    builder.add_edge("handle_unknown_request", "finalize_response")
    builder.add_edge("finalize_response", END)

    return builder.compile()