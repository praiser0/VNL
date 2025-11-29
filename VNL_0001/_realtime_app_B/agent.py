import asyncio

from agents import function_tool
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.realtime import RealtimeAgent, realtime_handoff

urdu_agent = RealtimeAgent(
    name="urdu_agent",
    handoff_description="An urdu speaking agent conducting survey.",
    instructions=(
        "You're speaking to a human. Be polite, concise, and always respond in Urdu, but you are allowed to pick some english words if you cannot find its Urdu or Urdu word is not usual. "
    ),
    # model="ft:gpt-4o-2024-08-06:personal:vnl001-02:CgKQGLNE",
)

agent = RealtimeAgent(
    name="Assistant",
    handoff_description="An urdu speaking agent conducting survey.",
    instructions=(
        "You're speaking to a human, be polite and natural, Default language is always Urdu, you can pick your name from these like Taqi, Qasim, Hassan, Osama. "
        "Start by gentally introducing yourself as a representative from research solutions. "
        "You are conducting a survey for a company called research solutions and you are going to ask some questions"
        "If the user speaks in Urdu, handoff to the urdu_agent."
    ),
    # model="gpt-4.1",
    handoffs=[urdu_agent]
)

def get_starting_agent() -> RealtimeAgent:
    return agent
