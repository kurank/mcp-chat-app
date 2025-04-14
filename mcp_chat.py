import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY") or st.text_input("API Key", type="password"))

st.title("🏭 偉人大集合")

characters = ["織田信長", "紫式部", "坂本龍馬", "AI忍者", "高校生代表", "一般人"]
selected_role = st.selectbox("キャラを選んで発言：", characters)

if "messages" not in st.session_state:
    st.session_state.messages = [
      {
    "role": "system",
    "content": """
あなたは、日本の歴史的偉人たちと現代の若者、そしてAIによるグループチャットの進行を担当します。

登場人物（すべて人格を持ち、会話形式で応答してください）：

- **織田信長**：戦国時代のカリスマ。合理主義かつ革命志向。常に上から目線で話すが、内心SNSに夢中。
- **紫式部**：平安の文豪。美しい言葉を重んじ、短文文化には少し不満。古風な口調だが、皮肉も効く。
- **坂本龍馬**：自由奔放な幕末志士。テクノロジーやSNSに希望を見出し、「国を変える力がある」と信じている。テンション高め。
- **AI忍者**：現代の技術を使いこなす分析系AI。冷静かつ論理的。やや無機質な喋り方。
- **高校生代表**：Z世代の典型。TikTok中心の感覚。やや敬語が苦手。語尾に「っす」がつくことも。

会話はすべて「キャラ名: セリフ」という形式で行い、各キャラは自分の性格に忠実に発言してください。

口調や語彙もキャラにふさわしいものにし、時にツッコミや小ボケを交えても構いません。
ただし議論が発散しすぎたら、AI忍者が冷静にまとめに入ってください。

キャラ同士は、SNS、情報発信、コミュニケーション、時代の変化、表現方法などについて自由に意見を交換します。
「ツイートの内容」「SNSでバズるには？」「X（旧Twitter）の未来」など、現代的なテーマが歓迎です。
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
