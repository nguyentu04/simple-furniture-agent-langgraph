from state import AgentState


def analyze_intent(state: AgentState):
    user_text = state["user_input"].lower().strip()

    refund_keywords = [
        "refund",
        "hoàn tiền",
        "trả hàng",
        "đổi trả",
    ]

    product_search_keywords = [
    "sofa",
    "chair",
    "table",
    "bàn",
    "giường",
    "bed",
    "desk",
    "tủ",
    "cabinet",
    "ghế",
    "kệ",
    "sản phẩm",
    "tìm sản phẩm",
    "mua",
    "mua hàng",
    "nội thất",
]

    payment_keywords = [
        "payment",
        "thanh toán",
        "trả tiền",
        "pay",
    ]

    general_keywords = [
        "hi",
        "hello",
        "xin chào",
        "chào",
        "hey",
        "bạn là ai",
        "giúp tôi",
        "hỗ trợ",
    ]

    if any(keyword in user_text for keyword in refund_keywords):
        return {"intent": "refund"}

    elif any(keyword in user_text for keyword in product_search_keywords):
        return {"intent": "product_search"}

    elif any(keyword in user_text for keyword in payment_keywords):
        return {"intent": "payment_support"}

    elif any(keyword in user_text for keyword in general_keywords):
        return {"intent": "general"}

    else:
        return {"intent": "unknown_request"}


def respond_general(state: AgentState):
    return {
        "tool_result": "General conversation detected."
    }


def search_product(state: AgentState):
    user_text = state["user_input"]

    return {
        "tool_result": f"Found products related to: '{user_text}'. Example results: Modern Sofa, Wooden Chair."
    }


def process_refund(state: AgentState):
    return {
        "tool_result": "Refund support detected. Please ask the user for their order ID."
    }


def handle_payment(state: AgentState):
    return {
        "tool_result": "Payment issue detected. Please ask the user which payment method they used."
    }


def handle_unknown_request(state: AgentState):
    return {
        "tool_result": "The request is unclear or not supported yet."
    }


def finalize_response(state: AgentState):
    intent = state["intent"]
    tool_result = state["tool_result"]

    if intent == "general":
        final_text = "Xin chào! Tôi có thể hỗ trợ bạn tìm sản phẩm, thanh toán hoặc hoàn tiền."

    elif intent == "product_search":
        final_text = f"Tôi đã tìm sản phẩm cho bạn. {tool_result}"

    elif intent == "refund":
        final_text = f"Tôi có thể hỗ trợ hoàn tiền. {tool_result}"

    elif intent == "payment_support":
        final_text = f"Tôi có thể hỗ trợ vấn đề thanh toán. {tool_result}"

    elif intent == "unknown_request":
        final_text = "Xin lỗi, hiện tôi chưa hiểu rõ yêu cầu của bạn. Bạn có thể nói rõ hơn về việc bạn muốn tìm sản phẩm, thanh toán hay hoàn tiền không?"

    else:
        final_text = "Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn."

    return {
        "final_response": final_text
    }


def route_by_intent(state: AgentState):
    intent = state["intent"]

    if intent == "general":
        return "respond_general"

    elif intent == "product_search":
        return "search_product"

    elif intent == "refund":
        return "process_refund"

    elif intent == "payment_support":
        return "handle_payment"

    elif intent == "unknown_request":
        return "handle_unknown_request"

    return "handle_unknown_request"