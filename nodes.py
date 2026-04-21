import os
from dotenv import load_dotenv
from google import genai
from state import AgentState

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_intent(state: AgentState):
    user_text = state["user_input"].strip()

    prompt = f"""
You are an intent classification assistant for a furniture store support agent.

Classify the user's message into exactly one of these intents:
- general
- product_search
- refund
- payment_support
- unknown_request

Definitions:
- general: greeting, simple conversation, asking who you are, asking for general help
- product_search: asking to buy, find, browse, view, or search for furniture/products
- refund: asking for refund, return, exchange, cancel order, return product
- payment_support: asking about payment, checkout, payment failure, card, bank transfer, e-wallet
- unknown_request: unclear request or not matched to any category above

Return only the label.
Do not explain.

User message: {user_text}
"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

    intent = response.text.strip()

    allowed_intents = {
        "general",
        "product_search",
        "refund",
        "payment_support",
        "unknown_request",
    }

    if intent not in allowed_intents:
        intent = "unknown_request"

    return {"intent": intent}


def respond_general(state: AgentState):
    return {
        "tool_result": "General conversation detected."
    }


def search_product(state: AgentState):
    user_text = state["user_input"]

    return {
        "tool_result": f"Found products related to: '{user_text}'. Example results: Modern Sofa, Wooden Chair, Minimal Desk."
    }


def process_refund(state: AgentState):
    return {
        "tool_result": "Refund support detected. Please provide your order ID so I can guide you to the next step."
    }


def handle_payment(state: AgentState):
    return {
        "tool_result": "Payment issue detected. Please tell me which payment method you used, for example card, bank transfer, or e-wallet."
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
        final_text = f"Tôi đã tìm thấy một số sản phẩm phù hợp cho bạn. {tool_result}"

    elif intent == "refund":
        final_text = f"Tôi có thể hỗ trợ bạn về hoàn tiền. {tool_result}"

    elif intent == "payment_support":
        final_text = f"Tôi có thể hỗ trợ bạn về thanh toán. {tool_result}"

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