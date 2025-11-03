from dotenv import load_dotenv
import streamlit as st
import asyncio
import os

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    RetryPromptPart,
    ModelMessagesTypeAdapter,
)

from rag_agent import agent, RAGDeps
from utils import get_chroma_client

load_dotenv()


async def get_agent_deps():
    return RAGDeps(
        chroma_client=get_chroma_client("./chroma_db"),
        collection_name="docs",
        embedding_model="all-MiniLM-L6-v2",
    )


def display_message_part(part):
    """
    Mostra uma parte da mensagem no Streamlit.
    """
    if part.part_kind == "user-prompt":
        with st.chat_message("user"):
            st.markdown(part.content)
    elif part.part_kind == "text":
        with st.chat_message("assistant"):
            st.markdown(part.content)


async def run_agent_once(user_input: str) -> str:
    """
    Roda o agente UMA vez (sem streaming).
    Se não conseguir falar com o modelo online, devolve uma msg de erro.
    """
    try:
        result = await agent.run(
            user_input,
            deps=st.session_state.agent_deps,
            message_history=st.session_state.messages,
        )
        # guarda histórico novo (inclui tool calls)
        st.session_state.messages.extend(result.new_messages())
        # o pydantic-ai devolve o texto em result.data
        return result.data
    except Exception as e:
        # aqui captura exatamente o erro que você estava vendo (APITimeoutError / ConnectTimeout)
        return (
            "⚠️ Não consegui falar com o modelo online agora. "
            "Verifique internet, firewall ou sua OPENAI_API_KEY.\n\n"
            f"Detalhes técnicos: `{type(e).__name__}: {e}`"
        )


async def main():
    st.title("IMUNIZACHAT")

    # estado
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_deps" not in st.session_state:
        st.session_state.agent_deps = await get_agent_deps()

    # mostra histórico já existente
    for msg in st.session_state.messages:
        if isinstance(msg, (ModelRequest, ModelResponse)):
            for part in msg.parts:
                display_message_part(part)

    # input do chat
    user_input = st.chat_input("O que você quer saber sobre vacinas?")

    if user_input:
        # mostra o que o usuário falou
        with st.chat_message("user"):
            st.markdown(user_input)

        # mostra placeholder do assistente
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("⏳ consultando o agente...")

            answer = await run_agent_once(user_input)

            # mostra resposta final
            placeholder.markdown(answer)


if __name__ == "__main__":
    asyncio.run(main())
