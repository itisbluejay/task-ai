import streamlit as st

import time 


st.title("Motivasyon Destek Asistanı")

st.sidebar.subheader("Görev Ekle")

new_task = st.sidebar.text_input("Yeni görev yaz")

if st.sidebar.button("Görevi ekle"):
    if new_task.strip()  != "":
        st.session_state.tasks.append(new_task)
        st.sidebar.success("Görev eklendi")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.complated_tasks = []

if "selected_task" not in st.session_state:
    st.session_state.selected_task = None

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "pomodoro_start" not in st.session_state:
    st.session_state.pomodoro_start = None

if "pomodoro_duration" not in st.session_state:
    st.session_state.pomodoro_duration = None

st.sidebar.subheader("Pomodoro")

if st.session_state.tasks:
    selected_task = st.sidebar.selectbox(
        "Çalışılacak görev",
        st.session_state.tasks
    )

    minutes = st.sidebar.number_input(
        "Kaç dakika çalışacaksın?",
        min_value=5,
        max_value=60,
        step=5,
        value=25
    )

    if st.sidebar.button("Pomodoro Başlat"):
        st.session_state.active_task = selected_task
        st.session_state.pomodoro_start = time.time()
        st.session_state.pomodoro_duration = minutes * 60
        st.sidebar.success("Pomodoro başladı")

    if st.session_state.pomodoro_start is not None:
        elapsed = time.time() - st.session_state.pomodoro_start
        remaining = int(st.session_state.pomodoro_duration - elapsed)


        if remaining > 0:
            mins = remaining // 60
            secs = remaining % 60
            st.sidebar.info(f" Kalan süre: {mins:02d}:{secs:02d}")
            
            col1, col2 = st.sidebar.columns(2)

            with col1:
                if st.sidebar.button("Durdur"):
                    st.session_state.pomodoro_start = None
                    st.session_state.pomodoro_duration = None
                    st.sidebar.warning("Pomodoro durduruldu")
            with col2:
                if st.sidebar.button("Bitirdim"):
                    st.session_state.pomodoro_duration = None
                    st.session_state.pomodoro_duration = None
                    st.sidebar.success("Görev tamamlandı")
                    st.balloons()

            time.sleep(1)
            st.rerun()

        else:
            st.sidebar.success("Pomodoro tamamlandı!")
            st.session_state.pomodoro_start = None
            st.session_state.pomodoro_duration = None
            st.balloons()

            if st.button("Bitirdim"):
                st.session_state.completed_tasks.append(st.session_state.active_task)
                st.session_state.tasks.remove(st.session_state.active_task)
                st.session_state.active_task = None
                st.session_state.timer_running = False
else:
    st.sidebar.info("önce görev eklemelisin")


st.write(f" Puan: {st.session_state.coins}")

if st.sidebar.button("Pomodoro başlat"):

    if st.session_state.selected_task is None:
        st.sidebar.warning("Önce görev seç")
    else:
        st.sidebar.write(f" Çalışılıyor...: {st.session_state.selected_task}")

        progress = st.progress(0)
        total_seconds = minutes * 60

        for i in range(100):
            time.sleep(total_seconds / 100)
            progress.progress(i + 1)

        st.session_state.coins += minutes

        st.session_state.tasks.remove(st.session_state.selected_task)
        st.session_state.completed_task.append(st.session_state.selected_task)

        st.sidebar.success(f"Pomodoro tamamlandı! + {minutes} puan")








DONE_KEYWORDS = ["yaptım","bitti","tamamladım"]

EMOTIONS = {
    "yorgun": ["yoruldum", "bittim", "tükendim"],
    "isteksiz":["istemiyorum", "motivasyonum yok", "ertelemek"],
    "kaygılı": ["yetişmeyecek","korkuyorum","başaramam"]
}


SUPPORT_MESSAGES = {
    "yorgun": "Yorgun hissetmen çok normal. Şu an herşeyi bitirmek zorunda değilsin",
    "isteksiz": "Motivasyon beklemek yerine küçük bir adım atalım.",
    "kaygılı" : "Kaygı işi büyüttüğümüzde artar. Küçük parçalara bölelim.",
    "belirsiz": "Birlikte küçük bir adım bulalım."
 }


MINI_TASKS = {
    "yorgun": [
        "5 dakikalık bir zamanlayıcı kur",
        "Sadece bir sayfaya göz at"
    ],
    "isteksiz": [
        "Dersi aç ama çalışmak zorunda değilsin",
        "En kolay parçadan başla"
    ],
    "kaygılı": [
        "Görevi 3 küçük parçaya böl",
        "En kolay parçadan başla"
    ],
    "belirsiz": [
        "Sadece yapılacak 1 küçük şey yaz"
    ]
}

def detect_emotion(text):
    text = text.lower()
    for emotion, keys in EMOTIONS.items():
        for k in keys:
            if k in text:
                return emotion
    return "belirsiz"

def is_done(text):
    return any(k in text.lower() for k in DONE_KEYWORDS)

with st.form("chat form", clear_on_submit = True):
    user_input = st.text_input("Bir şey yaz:")
    submit= st.form_submit_button("Gönder")

if submit and user_input:

    st.session_state.messages.append({"role":"Sen","content": user_input}
    )
    
    if is_done(user_input):
        st.session_state.messages.append(
            {"role":"Asistan", "content": "Harika görevi tamamladın kendinle gurur duy"}
        
        )
        st.balloons()
        st.stop()
    
    emotion = detect_emotion(user_input)

    st.session_state.messages.append(
            {"role": "Asistan","content": SUPPORT_MESSAGES[emotion]}
        )

    for task in MINI_TASKS[emotion]:
        st.session_state.messages.append(
                {"role": "Asistan", "content": f"-> {task}"}
            )

st.markdown("---")
for msg in st.session_state.messages:
    st.write(f"**{msg['role']}** : {msg['content']} ")