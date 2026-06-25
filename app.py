import streamlit as st
from textblob import TextBlob
from datetime import datetime
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# RESPONSE DATA
# -----------------------------
positive_responses = [
    "That's wonderful to hear! Keep celebrating your achievements.",
    "I'm glad you're feeling positive today.",
    "Your positive energy is inspiring. Keep it up!",
    "You seem to be doing well. Keep focusing on what makes you happy."
]

neutral_responses = [
    "Thank you for sharing your feelings.",
    "It's okay to have an average day.",
    "Every day doesn't need to be perfect.",
    "Take things one step at a time."
]

negative_responses = [
    "I'm sorry you're going through a difficult time.",
    "Your feelings are important and deserve attention.",
    "Remember that tough moments don't last forever.",
    "It's okay to ask for support when you need it."
]

motivational_quotes = [
    "Believe you can and you're halfway there.",
    "Small progress is still progress.",
    "Every challenge helps you grow.",
    "You are stronger than you think.",
    "Take one step at a time and keep moving forward."
]

relaxation_tips = [
    "Practice deep breathing for 2 minutes.",
    "Take a short walk outside.",
    "Listen to calming music.",
    "Drink water and stretch your body.",
    "Write down three things you're grateful for.",
    "Spend 5 minutes practicing mindfulness.",
    "Close your eyes and focus on your breathing.",
    "Take a short break from screens."
]

# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Positive"

    elif polarity < -0.2:
        return "Negative"

    else:
        return "Neutral"

# -----------------------------
# RESPONSE GENERATOR
# -----------------------------
def generate_response(mood):

    if mood == "Positive":
        response = random.choice(positive_responses)

    elif mood == "Negative":
        response = random.choice(negative_responses)

    else:
        response = random.choice(neutral_responses)

    tip = random.choice(relaxation_tips)
    quote = random.choice(motivational_quotes)

    return response, tip, quote

# -----------------------------
# SAVE CHAT HISTORY
# -----------------------------
def save_chat(user_message, mood):

    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now()} | Mood: {mood} | Message: {user_message}\n"
        )

# -----------------------------
# CRISIS DETECTION
# -----------------------------
def detect_crisis(text):

    crisis_keywords = [
        "suicide",
        "kill myself",
        "want to die",
        "end my life",
        "self harm",
        "hurt myself",
        "can't live anymore"
    ]

    text = text.lower()

    for keyword in crisis_keywords:
        if keyword in text:
            return True

    return False

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 Mental Health Companion Chatbot")

st.markdown("""
Welcome! This chatbot provides emotional support, motivation,
and relaxation suggestions based on your feelings.
""")

st.warning(
    "⚠️ This chatbot is not a substitute for professional mental health care."
)

# -----------------------------
# SESSION MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY OLD CHATS
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("How are you feeling today?")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Crisis Detection
    if detect_crisis(user_input):

        bot_response = """
🚨 **Important**

It sounds like you may be going through a very difficult time.

Please contact:
- A trusted friend or family member
- A counselor or mental health professional
- Local emergency services if you are in immediate danger

You deserve support and help.
"""

    else:

        mood = analyze_sentiment(user_input)

        response, tip, quote = generate_response(mood)

        save_chat(user_input, mood)

        bot_response = f"""
### 📊 Mood Detected: {mood}

💬 **Supportive Response**

{response}

🌱 **Relaxation Tip**

{tip}

✨ **Motivational Quote**

"{quote}"
"""

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    with st.chat_message("assistant"):
        st.markdown(bot_response)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.header("📈 Daily Wellness Tips")

    st.success("😴 Sleep 7–8 hours")
    st.success("💧 Stay hydrated")
    st.success("🏃 Exercise regularly")
    st.success("🧘 Practice mindfulness")
    st.success("📚 Take study breaks")
    st.success("🤝 Talk to someone you trust")

    st.divider()

    st.subheader("Project Features")

    st.write("✅ Sentiment Analysis")
    st.write("✅ Mood Detection")
    st.write("✅ Empathetic Responses")
    st.write("✅ Relaxation Tips")
    st.write("✅ Motivational Quotes")
    st.write("✅ Crisis Detection")
    st.write("✅ Chat History Logging")

    st.divider()

    st.subheader("Developer Info")

    st.write("Mental Health Companion")
    st.write("Built using Python, Streamlit & TextBlob")
