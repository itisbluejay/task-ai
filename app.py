import streamlit as st
import time 
import random


DONE_KEYWORDS = ["yaptım","bitti","tamamladım"]



SUPPORT_MESSAGES = {
    "yorgun": ["Yorgun hissetmen çok normal. Şu an herşeyi bitirmek zorunda değilsin"],
    "isteksiz": ["Motivasyon beklemek yerine küçük bir adım atalım.",
                "Bugün zor bir gün. Sadece 5 dakikanı bu işe ayırsan bile harika bir başlangıç yapmış olursun" ],
    "kaygılı" : ["Kaygı işi büyüttüğümüzde artar. Küçük parçalara bölelim.","Stres yapman çok normal. Hadi omuzlarındaki yükü hafifleticek bir adım bulalım "],
    "belirsiz": ["Birlikte küçük bir adım bulalım."]
    
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


new_task = st.sidebar.text_input("Yeni görev yaz")

if st.sidebar.button("Görevi ekle"):
    if new_task.strip()  != "":
        st.session_state.tasks.append(new_task)
        st.sidebar.success("Görev eklendi")


if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

if "selected_task" not in st.session_state:
    st.session_state.selected_task = None

if "active_task" not in st.session_state:
    st.session_state.active_task = None

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "pomodoro_start_time" not in st.session_state:
    st.session_state.pomodoro_start_time = None

if "pomodoro_duration" not in st.session_state:
    st.session_state.pomodoro_duration = None

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = []

    st.session_state.messages.append({"role": "Asistan", "content":"Merhaba! Ben Motivasyon Destek Asistanın.Bugün sana nasıl yardımcı olabilirim? Lütfen hedeflerini, duygu durumunu veya sorunlarını benimle paylaş ki sana en uygun çalışma planını oluşturabileyim"})

if "pomodoro_duration" not in st.session_state:
    st.session_state.pomodoro_duration = None

if "last_probabilities" not in st.session_state:
    st.session_state.last_probabilities ={"belirsiz": 1.0, "yorgun": 0.0,"isteksiz": 0.0, "kaygılı": 0.0}

selected_task = None

st.title("Motivasyon Destek Asistanı")
st.write(f"🪙 **Puan** {st.session_state.coins}")

st.sidebar.subheader("Görev Ekle")





st.sidebar.subheader("Pomodoro")
pomodoro_info_placeholder = st.sidebar.empty()

if st.session_state.tasks and st.session_state.pomodoro_start_time is None:
    selected_task = st.sidebar.selectbox(
        "Çalışılacak görev",
        st.session_state.tasks,
        key = "selected_task_pomodoro"
    )

    minutes = st.sidebar.number_input(
        "Kaç dakika çalışacaksın?",
        min_value=5,
        max_value=60,
        step=5,
        value=25,
        key = "pomodoro_minutes"
    )

    task_difficulty = st.sidebar.slider(
        "Görevin zorluk seviyesi(1: Kolay, 5: Çok zor)",
        min_value =1,
        max_value = 5,
        value = 3,
        key = "task_difficulty"

    )

    

elif st.session_state.pomodoro_start_time is not None:

    st.sidebar.success(f" {st.session_state.active_task} çalışılıyor lütfen odaklan.")
    elapsed = time.time() - st.session_state.pomodoro_start_time
    remaining = st.session_state.pomodoro_duration - elapsed

    #odaklanma perdesi görüntüsü için
    if remaining > 0:
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        st.markdown("---")
        st.header("POMODORO MODU AKTİF")
        st.subheader(f"Şu an **{st.session_state.active_task}** görevine odaklan.Geri sayım devam ediyor.")
        
        st.markdown(
        f"""
        <div style ='
            background-color: #FF4B4B; /* Streamlit Kırmızı Tonu */
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            border: 5px solid #FF8C00; /* Çerçeve ekleme */
            box-shadow: 0 4px  12px rgba(0, 0, 0, 0.2); /* Gölge efekti */
            margin-top: 20 px;
        '>
            <h1 style='front-size: 6em; margin: 0;'>{mins:02d}:{secs:02d}</h1>
            <p style='font-size: 1.5em; margin-top: 10px;' >DİKKATİNI DAGITMA </p>
            <p style='font -size: 1em; margin top: 10px;' >Yapay zeka asistanı, odaklanman için geçici olarak devre dışı bırakıldı.</p>
        </div>
        """,
        unsafe_allow_html=True
        )


        pomodoro_info_placeholder.info(f" ⌛ **{st.session_state.active_task}** için kalan süre: **{mins:02d}:{secs:02d}**")
            
        col1, col2 = st.sidebar.columns(2)

        with col1:
            if st.button("Durdur", key ="pause_button"):
                st.session_state.pomodoro_start_time = None
                st.session_state.active_task = None
                st.sidebar.warning("Pomodoro durduruldu")
                st.rerun()

        with col2:
            if st.button("Bitirdim" , key= "finish_button_achive"):
                st.session_state.pomodoro_start_time = 0
                
                earned_coins = st.session_state.pomodoro_duration // 60

                st.session_state.coins += earned_coins

                if st.session_state.active_task in st.session_state.tasks:
                    st.session_state.tasks.remove(st.session_state.active_task)

                
                st.session_state.active_task = None
                st.session_state.pomodoro_start_time = None
                st.sidebar.success(f" Görev tamamlandı! + {earned_coins} puan kazandın.")
                st.balloons()
                st.rerun()

        time.sleep(1)
        st.rerun()
    else:
        earned_coins = st.session_state.pomodoro_duration // 60

        st.session_state.coins += earned_coins
        st.session_state.completed_tasks.append(st.session_state.active_task)
        if st.session_state.active_task in st.session_state.tasks:
            st.session_state.tasks.remove(st.session_state.active_task)
        st.session_state.completed_tasks.append(st.session_state.active_task)
        st.session_state.pomodoro_start_time = None
        st.session_state.active_task = None

        pomodoro_info_placeholder.success(f"🕑 Süre doldu! **+{earned_coins} puan** kazandın.")
        st.balloons()
        st.rerun()
        
        
else:
    st.sidebar.info("önce görev eklemelisin")

st.subheader("Görev Durumu")
col_tasks, col_completed = st.columns(2)

with col_tasks:
    st.markdown("#### Yapılacaklar")
    if st.session_state.tasks:
        for task in st.session_state.tasks:
            if task == st.session_state.active_task:
                st.warning(f"** 🦩 {task}** (Çalışılıyor)")
            else:
                st.info(f"⚪ {task}")
    else:
        st.markdown("> *Şu anda yapılacak göreviniz yok. Harika!*")

with col_completed:
    st.markdown("#### Tamamlananlar")
    if st.session_state.completed_tasks:
        for task in st.session_state.completed_tasks:
            st.success(f"✅{task}")

    else:
        st.markdown(">*Henüz tamamlanmış göreviniz yok.*")










def detect_emotion(text):
    text = text.lower()

    scores = {
        "yorgun": 0,
        "isteksiz": 0,
        "kaygılı": 0,
        "belirsiz": 0
    }

    keywords = {
        "yorgun" : ["yorgun", "uykum var","yoruldum", "bıktım","enerjim yok"],
        "isteksiz":["istemiyorum","başlayamıyorum", "sıkıcı","sıkıldım","halim yok"],
        "kaygılı":["kaygı","korkuyorum","yetişmeyecek","endişe","stres","baskı"],
        "belirsiz":["bilmiyorum","ne yapacağım","kararsızım","kafam karışık"]
          }
    
    HEDEF_KELIMELER = ["ders çalışmak","iş","ödev","kitap","çalışmalıyım","kod yazmak","başlamalıyım","yapmalıyım"]

    for emotion, keys in keywords.items():
        # Bu döngü mevcut haliyle kalsın.
        for key in keys:
            if key in text:
                scores[emotion] += 1

    if any(key in text for key in HEDEF_KELIMELER):
        scores["kaygılı"] += 0.5 
        
    total_score = sum(scores.values())


    if total_score == 0:
        return {"belirsiz": 1.0,"yorgun":0.0,"isteksiz": 0.0,"kaygılı": 0.0}
    
    probabilities = {
        emotion: score / total_score
        for emotion, score in scores.items()
    }

    return probabilities

    




def predict_optimal_duration(probabilities, total_tasks):
    KAYGI_KATSAYISI = 0.5  #kaygı 1 isa 10 dk kısaltma yapar
    YORGUNLUK_KATSAYISI = 0.4  # Yorgunluk 1 ise 7.5 dk kısaltma yapar

    TASK_LOAD_BONUS = min(total_tasks, 5) * 60

    kaygi_cezasi = probabilities.get("kaygılı", 0) * KAYGI_KATSAYISI * 600
    yorgunluk_cezasi = probabilities.get("yorgun", 0) * YORGUNLUK_KATSAYISI * 450

    base_duration_sec = 25 * 60

    predicted_duration_sec = base_duration_sec + TASK_LOAD_BONUS - kaygi_cezasi - yorgunluk_cezasi
    
    predicted_duration_sec = max(600, min(2400, predicted_duration_sec))

    return predicted_duration_sec     

if st.sidebar.button("Pomodoro Başlat" , key= "start_pomodoro_button"):
    st.session_state.active_task = selected_task

    user_selected_min = st.session_state.get("pomodoro_minutes", 25)
    user_selected_sec = user_selected_min * 60
    
    current_probabilities= st.session_state.get('last_probabilities', {"belirsiz": 1.0, "yorgun": 0.0, "isteksiz": 0.0, "kaygılı": 0.0})

    kaygi_etkisi = current_probabilities.get("kaygılı", 0) * 300 # Max 5 dk azaltır
    yorgunluk_etkisi = current_probabilities.get("yorgun", 0) * 300 # Max 5 dk azaltır

    final_duration = user_selected_sec - kaygi_etkisi - yorgunluk_etkisi
    final_duration = max(300, final_duration)


    

    st.session_state.pomodoro_start_time = time.time()
    st.session_state.pomodoro_duration = final_duration

    predicted_minutes = int(round(final_duration / 60))


    st.sidebar.success(f" Hedef : {predicted_minutes}dk olarak ayarlandı.Başarılar")

    st.rerun()




with st.container(height=350):
    for msg in st.session_state.messages:
        if msg['role'] == "Sen":
            # Doğru girinti ve etiketleme
            st.markdown(f"**  👤 Sen** : {msg['content']} ", unsafe_allow_html= True)
        else:
            # Doğru girinti ve etiketleme
            st.markdown(f"**  🤖 {msg['role']}** : {msg['content']}", unsafe_allow_html=True )

# Otomatik kaydırma mantığı (Container'dan dışarıda, doğru yer)
if st.session_state.messages:
    st.markdown("<div id='end_of_chat'></div>", unsafe_allow_html=True) 
    st.markdown(
        """
        <script>
            var element = document.getElementById("end_of_chat");
            element.scrollIntoView({behavior: "smooth"});
        </script>
        """,
        unsafe_allow_html=True
    )


# 2. YAZMA FORMU (Yine dışarıda, doğru yer)
with st.form("chat form", clear_on_submit = True):
    # DİKKAT: Doğru girinti seviyesinde!
    user_input = st.text_input("Bir şey yaz:")
    submit= st.form_submit_button("Gönder")


# 3. YZ MANTIĞI VE is_done FONKSİYONU (Formdan hemen sonra, doğru yer)
def is_done(text):
    return any(k in text.lower() for k in DONE_KEYWORDS)


if submit and user_input:

    st.session_state.messages.append({"role":"Sen","content": user_input})
    gorev_tamamlandi = False

    # GÖREV TAMAMLANDI MANTIĞI
    if is_done(user_input):

        if st.session_state.active_task:
            tamamlanan_gorev = st.session_state.active_task
            if tamamlanan_gorev in st.session_state.tasks:
                st.session_state.tasks.remove(tamamlanan_gorev)
            st.session_state.completed_tasks.append(tamamlanan_gorev)

            kazanilan_puan = 10
            st.session_state.coins += kazanilan_puan

            last_probabilities = st.session_state.get("last_probabilities", {"belirsiz": 1.0})
            baskin_duygu = max(last_probabilities, key=last_probabilities)

            tebrik_sozleri ={
                "yorgun":f"İnanılmazsın! Gözlerinden yorgunluğun hissedilirken bile **{tamamlanan_gorev}** artık bitti ve omuzlarından bir yük kalktı.",
                "kaygılı":f"O kadar endişeye rağmen harika bir iş çıkardın **{tamamlanan_gorev}** artık bitti ",
                "isteksiz":f"İşte bu! Hiç canın istemiyordu ama görevini tamamladın.Tebrik ederim",
                "belirsiz":f"harika! Bir adımı daha başarıyla tamamladın."

            }

            ozel_tebrik = tebrik_sozleri.get(baskin_duygu, "Harika bir iş çıkardın!")

            st.session_state.messages.append(
                {"role":"Asistan","content": f"🎯 **GÖREV TAMAMLANDI!** \n\n{ozel_tebrik} \n\n Hesabına **{kazanilan_puan} puan** ekledim. Yeni bir hedefe geçmeye hazır mısın?"}
            )



            st.session_state.active_task = None
            st.session_state.pomodoro_start_time = None

            
            st.balloons()
            st.rerun()
            gorev_tamamlandi = True
        
        
    if gorev_tamamlandi:
        pass

    # YZ ANALİZ MANTIĞI
    if not gorev_tamamlandi:

        cevap = "Anladım. Şu anki durumuna uygun bir öneri hazırlıyorum."

        # Detect emotion fonksiyonunuzun uygulamanın üst kısımlarında tanımlı olması gerekiyor.
        probabilities = detect_emotion(user_input) 

        emotion = max(probabilities, key=probabilities.get)
        st.session_state['last_probabilities'] = probabilities

        baskin_duygu_skor = int(probabilities[emotion] * 100)

        CHITCHAT_REFLEX = {
            "selam": "Selam! Seni gördüğüme sevindi. Bugün modun nasıl? Planların üzerinden beraber geçelim mi?",
            "nasılsın": "Seni desteklemek için sabırsızlanıyorum.Senin enerjin ne kadar yüksek olursa ben de o kadar iyi hissediyorum.Sen nasılsın? ",
            "teşekkür":"Rica ederim, her zaman yanındayım Başka ne yapabiliriz?",
            "yapabiliriz": "Harika bir enerji! Hemen listene bakalım mı yoksa yeni bir hedef mi eklemek istersin?"


        }

        intro_sentences ={
                "yorgun": "Yazından biraz yorgun olduğunu hissediyorum, ama dert etme; hepimiz bazen tükenmiş hissedebiliriz. ",
                "kaygılı":"Şu an zihnin biraz kalabalıklaşmış sanki, gel bu karmaşayı beraber çözelim",
                "isteksiz":  "Bazen başlamak, bitirmekten daha zordur.Bugün o ilk adımı atmanda sana yardım edeceğim.",
                "belirsiz": "Kafanın biraz karışık olması çok normal.Netleşmek için küçük bir adıma ne dersin?"
             }

        sohbet_yaniti = None
        for anahtar in CHITCHAT_REFLEX:
            if anahtar in user_input.lower():
                sohbet_yaniti = CHITCHAT_REFLEX[anahtar]
                break

        if sohbet_yaniti:
            cevap = sohbet_yaniti

        else:
            base_intro = intro_sentences.get(emotion, "Anladım, seni çok iyi duyabiliyorum.")
            if probabilities["kaygılı"] > 0.2 and probabilities["yorgun"]> 0.2:

                cevap = f"{base_intro} Hem biraz yorulmuşsun hem de zihnin yapılacaklarla dolu. Önce derin bir nefes al, 5 dakikalık mola verelim, sonra işleri küçültürüz."



            elif probabilities["yorgun"] > 0.5:  
                cevap = f"{base_intro} Enerjin %{baskin_duygu_skor} seviyelerine düşmüş gibi duruyor. Kendine çok yüklenme, kısa bir mola her şeyi değiştirebilir."

            elif emotion == "isteksiz":
                cevap = f"{base_intro} Bazen o ilk adımı atmak dağın zirvesine tırmanmak gibi gelir. Ama başladığında su gibi akacak."

            elif emotion == "kaygılı":
                cevap = f"{base_intro} Şu an her şey üst üste gelmiş gibi hissediyor olabilirsin. Gel listeyi beraber parçalayalım."

            elif emotion == "belirsiz":
                cevap = f"{base_intro} Kararsız kalmak enerjini tüketir. En küçük görevden başlayalım, yol kendiliğinden aydınlanacaktır."

            else:
                cevap = base_intro

            destek_mesaji = random.choice(SUPPORT_MESSAGES.get(emotion, ["Harika bir potansiyele sahipsin, sadece odaklanmaya ihtiyacın var."]))
            cevap = f"{base_intro} {destek_mesaji}"

        st.session_state.messages.append(
            {"role": "Asistan","content": cevap}
        )
        
        if not sohbet_yaniti:
            for task in MINI_TASKS.get(emotion, []): 
               st.session_state.messages.append(
                {"role": "Asistan", "content": f"->  Önerim:  {task}"}
            )
        
        # 3. Arayüzü Güncelle
        st.rerun()