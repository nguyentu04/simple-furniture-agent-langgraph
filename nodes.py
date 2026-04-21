from state import AgentState


def analyze_intent(state: AgentState):
    user_text = state["user_input"].lower()

    if "refund" in user_text or "hoàn tiền" in user_text:
        return {"intent": "refund"}

    elif "sofa" in user_text or "chair" in user_text or "table" in user_text or "bàn" in user_text or "giường" in user_text:
        return {"intent": "product_search"}

    elif "payment" in user_text or "thanh toán" in user_text:
        return {"intent": "payment_support"}

    else:
        return {"intent": "general"}


def respond_general(state: AgentState):
    return {
        "tool_result": "User is asking a general question. No external tool is needed."
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

    else:
        final_text = "Xin lỗi, tôi chưa hiểu yêu cầu của bạn."

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

    return "respond_general"