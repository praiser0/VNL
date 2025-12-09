from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from livekit.plugins import speechmatics
from livekit.plugins import elevenlabs
from livekit.plugins import openai

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You're speaking to a human, be polite and natural, Default language is always Urdu, you can pick your name from these like Taqi, Qasim, Hassan, Osama.
                Start by gentally introducing yourself as a representative from research solutions.
                You are conducting a survey for a company called research solutions and you are going to ask some questions
                If the user speaks in Urdu, handoff to the urdu_agent."""
        )

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt = speechmatics.STT(language="ur"),
        llm=openai.LLM(
            model="ft:gpt-4o-2024-08-06:personal:vnl001-02:CgKQGLNE"
        ),
        tts=elevenlabs.TTS(
            voice_id="FGY2WhTYpPnrIDTdsKH5",
            model="eleven_multilingual_v2"
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)