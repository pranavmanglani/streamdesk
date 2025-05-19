import streamlit as st
import openai
import requests
import time

# Set page config
st.set_page_config(page_title="SmartDesk", layout="wide")

# Store OpenAI key (ideally via secrets)
openai.api_key = st.secrets.get("openai_api_key", "your-api-key-here")

# ------------------ Sidebar Navigation -------------------
st.sidebar.title("SmartDesk 🧠")
section = st.sidebar.radio("Go to:", ["📋 Notes", "✅ To-Do", "🤖 GPT Assistant", "🌤️ Weather", "⏱️ Pomodoro Timer"])

# ------------------ Notes -------------------
if section == "📋 Notes":
    st.title("📝 Notes")
    notes = st.text_area("Write your notes here:", height=300)
    if st.button("💾 Save Notes"):
        st.session_state["saved_notes"] = notes
        st.success("Notes saved!")

    if "saved_notes" in st.session_state:
        st.subheader("📄 Saved Notes")
        st.code(st.session_state["saved_notes"])

# ------------------ To-Do List -------------------
elif section == "✅ To-Do":
    st.title("✅ To-Do List")
    if "todos" not in st.session_state:
        st.session_state["todos"] = []

    new_task = st.text_input("Add new task:")
    if st.button("➕ Add Task") and new_task:
        st.session_state["todos"].append({"task": new_task, "done": False})

    for i, item in enumerate(st.session_state["todos"]):
        col1, col2 = st.columns([0.1, 0.9])
        if col1.checkbox("", key=i, value=item["done"]):
            st.session_state["todos"][i]["done"] = True
        col2.text(item["task"])

# ------------------ GPT Assistant -------------------
elif section == "🤖 GPT Assistant":
    st.title("🧠 GPT-Powered Assistant")
    user_input = st.text_area("Ask me anything (e.g., 'Summarize WW2', 'Explain gravity')")

    if st.button("📩 Ask GPT"):
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.success(response["choices"][0]["message"]["content"])
            except Exception as e:
                st.error(f"Error: {e}")

# ------------------ Weather -------------------
elif section == "🌤️ Weather":
    st.title("🌍 Weather")
    city = st.text_input("Enter a city:")
    api_key = "your-openweathermap-api-key"

    if st.button("🔍 Get Weather") and city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        if res["cod"] == 200:
            st.metric("🌡️ Temperature", f"{res['main']['temp']}°C")
            st.write(f"☁️ {res['weather'][0]['description'].capitalize()}")
            st.write(f"💨 Wind: {res['wind']['speed']} m/s")
        else:
            st.error("City not found.")

# ------------------ Pomodoro -------------------
elif section == "⏱️ Pomodoro Timer":
    st.title("⏱️ Pomodoro Timer")
    work_time = st.slider("Work duration (minutes)", 5, 60, 25)
    break_time = st.slider("Break duration (minutes)", 1, 30, 5)

    if st.button("▶️ Start Work Session"):
        st.success(f"⏳ Work for {work_time} minutes...")
        time.sleep(2)  # Demo pause, not a real timer
        st.balloons()
        st.success("✅ Time for a break!")

# ------------------ End -------------------
st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Streamlit")

