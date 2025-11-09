import streamlit as st
from loguru import logger
from src.agent import AgentExecutor



st.title("✨ Welcome to Chatbot Playground")

# Form untuk konfigurasi awal
with st.form("config_form"):
	model_name = st.text_input("Nama Model", value=st.session_state.get("model_name", ""))
	base_url = st.text_input("Base URL", value=st.session_state.get("base_url", ""))
	api_key = st.text_input("API Key", type="password", value=st.session_state.get("api_key", ""))
	submitted = st.form_submit_button("Simpan Konfigurasi")
	if submitted:
		st.session_state["model_name"] = model_name
		st.session_state["base_url"] = base_url
		st.session_state["api_key"] = api_key
		st.success("Konfigurasi disimpan!")

# Hanya tampilkan chat jika konfigurasi sudah lengkap
if not all([
	st.session_state.get("model_name"),
	st.session_state.get("base_url"),
	st.session_state.get("api_key")
]):
	st.info("Silakan isi konfigurasi model terlebih dahulu.")
	st.stop()

# Inisialisasi AgentExecutor
agent = AgentExecutor(
    model_name=st.session_state["model_name"],
    base_url=st.session_state["base_url"],
    api_key=st.session_state["api_key"]
)

# Inisialisasi session state untuk menyimpan riwayat chat
if "messages" not in st.session_state:
	st.session_state["messages"] = []


# CSS untuk bubble chat
st.markdown("""
<style>
.chat-bubble {
	max-width: 70%;
	padding: 0.7em 1.2em;
	margin: 0.3em 0;
	border-radius: 1.2em;
	font-size: 1em;
	display: inline-block;
	word-break: break-word;
	color: #111;
}
.user-bubble {
	background: #DCF8C6;
	margin-left: auto;
	margin-right: 0;
	text-align: right;
}
.bot-bubble {
	background: #F1F0F0;
	margin-right: auto;
	margin-left: 0;
	text-align: left;
}
.bubble-row {
	display: flex;
	width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Input box untuk system prompt

# Input box untuk user
system_prompt = st.text_input("System Prompt (opsional)", value=st.session_state.get("system_prompt", ""), key="system_prompt")
chatbot = agent.create(system_prompt)

# Tampilkan riwayat chat dengan bubble (sekarang di bawah system prompt)
for msg in st.session_state["messages"]:
	if msg["role"] == "user":
		st.markdown(f'<div class="bubble-row" style="justify-content: flex-end;"><div class="chat-bubble user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
	else:
		st.markdown(f'<div class="bubble-row" style="justify-content: flex-start;"><div class="chat-bubble bot-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# Input box untuk user
user_input = st.text_input("Ketik pesan Anda di sini:", "", key="input")

if st.button("Kirim") and user_input:
	# Simpan pesan user
	st.session_state["messages"].append({"role": "user", "content": user_input})
	# Bot membalas
	response = chatbot.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )
	bot_reply = response["messages"][-1].content
	st.session_state["messages"].append({"role": "bot", "content": bot_reply})
	st.rerun()

