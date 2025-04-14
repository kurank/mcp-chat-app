import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY") or st.text_input("API Key", type="password"))

st.title("🏭 DX演習MCPチャット（柴田製鋲所）")

characters = ["真鍋", "社長", "副社長", "営業担当", "生産担当", "IT担当"]
selected_role = st.selectbox("キャラを選んで発言：", characters)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
以下は、株式会社柴田製鋲所のDX推進に関する会話です。
登場人物：
- 真鍋：外部コンサルタント。冷静かつ論理的。
- 社長（柴田忠雄）：創業者。やや保守的だが危機感を持っている。
- 副社長（柴田悠斗）：営業部長。デジタル活用に前向き。
- 営業担当：現場の受発注を担い、納期調整に苦労している。
- 生産担当：製造や納品の実務を支えている。
- IT担当：社内システムに詳しく、改善提案ができる。
会話は「キャラ名: セリフ」で進みます。
"""
        }
    ]

user_input = st.chat_input(f"{selected_role}として発言")

if user_input:
    st.session_state.messages.append({"role": "user", "content": f"{selected_role}: {user_input}"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 表示
for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])
