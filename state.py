from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    tool_result: Optional[str]
    final_response: Optional[str]
