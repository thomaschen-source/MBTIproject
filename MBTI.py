import streamlit as st
import smtplib
from email.mime.text import MIMEText
import random          
import pandas as pd    
from collections import Counter 
import plotly.graph_objects as go
# ==========================================# 1. 頁面基礎設定# ==========================================

st.set_page_config(page_title="Multiverse MBTI / 多重宇宙 MBTI", page_icon="🌌")
# ==========================================# 2. CSS 美化# ==========================================

st.markdown("""

    <style>

    .big-title {

        font-size: 60px; font-weight: 900; text-align: center;

        background: -webkit-linear-gradient(45deg, #FF0099, #493240);

        -webkit-background-clip: text; -webkit-text-fill-color: transparent;

        margin-bottom: 10px;

    }

    .sub-title {

        font-size: 24px; text-align: center; opacity: 0.7; margin-bottom: 30px;

    }

    div[role="radiogroup"] label > div:first-of-type { border: 2px solid #888 !important; }

    div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {

        background-color: #FF4B4B !important; border-color: #FF4B4B !important;

    }

    div[role="radiogroup"] label p { font-size: 19px !important; font-weight: 600; }

    div[role="radiogroup"] label:hover { background-color: rgba(128, 128, 128, 0.1); border-radius: 10px; }

    </style>

""", unsafe_allow_html=True)
# ==========================================# 3. 狀態初始化# ==========================================if 'page' not in st.session_state: st.session_state.page = 'language_select'if 'language' not in st.session_state: st.session_state.language = 'zh'if 'target_theme' not in st.session_state: st.session_state.target_theme = Noneif 'tie_themes' not in st.session_state: st.session_state.tie_themes = []if 'final_result' not in st.session_state: st.session_state.final_result = []# ==========================================# 4. 資料庫 (中文完整版 + 英文翻譯版)# ==========================================# 4.1 介面文字 (UI Texts) - 修復 KeyError
if 'page' not in st.session_state: st.session_state.page = 'language_select'
if 'language' not in st.session_state: st.session_state.language = 'zh'
if 'target_theme' not in st.session_state: st.session_state.target_theme = None
if 'tie_themes' not in st.session_state: st.session_state.tie_themes = []
if 'final_result' not in st.session_state: st.session_state.final_result = []

# 👇 請補上這一行！
if 'user_answers' not in st.session_state: st.session_state.user_answers = []
UI_TEXT = {

    'zh': {

        'title': "多重宇宙 MBTI", 'subtitle': "劇本設定與角色校準",

        'age_label': "請輸入你的年齡",

        'intro_title': "🔮 前導測試：尋找你的靈魂歸屬",

        'intro_desc': "請依照直覺回答下列 5 題，系統將為你開啟最適合的平行宇宙。",

        'start_btn': "🚀 啟動傳送門",

        'error_incomplete': "⚠️ 還有題目沒選喔！請完成所有問題再傳送。",

        'tie_title': "⚡ 命運的分岔點",

        'tie_warn': "偵測到你的靈魂同時與兩個世界產生強烈共鳴...",

        'tie_desc': "請做出最後的抉擇，這將決定你的命運。",

        'tie_btn': "確認命運",

        'quiz_submit': "查看最終結果",

        'result_success': "⚡ 系統偵測到多種靈魂波長！你是罕見的複合型人格！",

        'result_normal': "🎯 系統分析完成！這就是真實的你。",

        'email_section': "📧 保存你的分析報告",

        'email_label': "請輸入你的 Email 地址：",

        'email_btn': "🚀 發送報告到信箱",

        'restart_btn': "🔄 重啟命運 (回到首頁)",

        'titles': {"fantasy": "🏰 異世界轉生篇", "zombie": "🧟 末日喪屍篇", "school": "🏫 青春校園篇", "cyber": "🤖 賽博龐克篇"},

        'tie_options': {

            "fantasy": "⚔️ 我寧願在魔法世界戰死，也不要平凡活著",

            "zombie": "🧟 我享受在極限狀態下求生的真實恐懼感",

            "school": "🏫 我更在乎人與人之間溫暖的情感連結",

            "cyber": "🤖 人類情感太麻煩，我寧願擁抱理性的數據"

        },

        # 這裡補上了缺少的鍵值

        'match': "❤️ 最佳拍檔", 'clash': "💔 容易衝突",

        'strength': "✨ 核心優勢", 'weakness': "⚠️ 潛在盲點",

        'career_title': "職業推薦"

    },

    'en': {

        'title': "Multiverse MBTI", 'subtitle': "Scenario & Character Calibration",

        'age_label': "Enter your age",

        'intro_title': "🔮 Pilot Test: Find Your Universe",

        'intro_desc': "Answer intuitively. The system will open the most suitable parallel universe for you.",

        'start_btn': "🚀 Open Portal",

        'error_incomplete': "⚠️ Incomplete! Please answer all questions.",

        'tie_title': "⚡ The Fork in Fate",

        'tie_warn': "Resonance detected with two worlds...",

        'tie_desc': "Make the final choice. This will decide your destiny.",

        'tie_btn': "Confirm Destiny",

        'quiz_submit': "Reveal True Self",

        'result_success': "⚡ Rare Composite Personality Detected!",

        'result_normal': "🎯 Analysis Complete! This is the real you.",

        'email_section': "📧 Save Report",

        'email_label': "Enter Email:",

        'email_btn': "🚀 Send Report",

        'restart_btn': "🔄 Restart",

        'titles': {"fantasy": "🏰 Fantasy Isekai", "zombie": "🧟 Zombie Apocalypse", "school": "🏫 High School Drama", "cyber": "🤖 Cyberpunk City"},

        'tie_options': {

            "fantasy": "⚔️ I'd rather die fighting magic than live an ordinary life.",

            "zombie": "🧟 I enjoy the thrill of survival in extreme conditions.",

            "school": "🏫 I value warm emotional connections with people.",

            "cyber": "🤖 Emotions are messy; I prefer rational data."

        },

        # 這裡補上了缺少的鍵值

        'match': "❤️ Best Match", 'clash': "💔 Potential Clash",

        'strength': "✨ Core Strengths", 'weakness': "⚠️ Blind Spots",

        'career_title': "Career Recommendation"

    }

}# 4.2 前導測驗 (中文版)

SORTING_QUIZ_ZH = [

    {"q": "1. 如果你獲得 10 億元且不需工作，你第一件事做什麼？", "opts": [("去地圖上找不到的秘境探險", "fantasy"), ("買座堡壘囤積物資，確保絕對安全", "zombie"), ("包下遊樂園，找所有朋友開派對", "school"), ("投資尖端實驗室，親眼見證未來科技", "cyber")]},

    {"q": "2. 世界末日還有 1 小時，你最後會做什麼？", "opts": [("閉眼祈禱，希望能穿越到異世界", "fantasy"), ("衝去搶奪武器和食物，準備活下去", "zombie"), ("打電話給最愛的人說真心話", "school"), ("試圖駭入電腦尋找災難真相", "cyber")]},

    {"q": "3. 瘋狂科學家給你一瓶藥水，你希望獲得？", "opts": [("元素魔法 (控制風火水土)", "fantasy"), ("不死之身 (極限生存能力)", "zombie"), ("讀心術 (看穿人心)", "school"), ("超級大腦 (瞬間學會所有知識)", "cyber")]},

    {"q": "4. 展開長途旅程，你最想要的夥伴是？", "opts": [("一隻忠誠強大的傳說神獸", "fantasy"), ("身經百戰的特種兵", "zombie"), ("幽默風趣的好朋友", "school"), ("無所不知的 AI 機器人", "cyber")]},

    {"q": "5. 週末想看電影，你會選哪種海報？", "opts": [("巨龍與城堡的史詩冒險", "fantasy"), ("陰暗廢墟與危機的驚悚片", "zombie"), ("陽光下的校園青春戀愛劇", "school"), ("霓虹燈光與機械的科幻片", "cyber")]}

]# 4.3 前導測驗 (英文版)

SORTING_QUIZ_EN = [

    {"q": "1. You win 1 billion dollars. First thing you do?", "opts": [("Explore uncharted territories", "fantasy"), ("Buy a fortress and hoard supplies", "zombie"), ("Rent an amusement park for a party", "school"), ("Invest in future tech labs", "cyber")]},

    {"q": "2. 1 hour until doomsday. What do you do?", "opts": [("Pray to be transported to another world", "fantasy"), ("Loot weapons and food", "zombie"), ("Call loved ones to confess feelings", "school"), ("Hack computers to find the truth", "cyber")]},

    {"q": "3. A mad scientist offers you a potion. You choose:", "opts": [("Elemental Magic", "fantasy"), ("Immortality", "zombie"), ("Mind Reading", "school"), ("Super Brain", "cyber")]},

    {"q": "4. Best travel companion?", "opts": [("A loyal mythical beast", "fantasy"), ("A veteran soldier", "zombie"), ("A humorous and fun best friend", "school"), ("An all-knowing AI robot", "cyber")]},

    {"q": "5. Movie choice:", "opts": [("Epic adventure with dragons and castles", "fantasy"), ("Thriller with dark ruins and danger", "zombie"), ("Sunny campus romance drama", "school"), ("Neon Sci-Fi", "cyber")]}

]
# ==========================================
# 4.4 MBTI 詳細資料 (中文完整版 - 修正補回長文與4優4缺)
# ==========================================
MBTI_INFO_ZH = {
    "ESTJ": {
        "title": "總經理", "color": ["#5B86E5", "#36D1DC"], "match": "ISFP", "clash": "INFP",
        "desc": "在一個分崩離析的世界裡，你是那根支撐大局的鋼鐵脊樑。當其他人都因為恐懼而不知所措，或因為道德兩難而猶豫不決時，你是唯一一個還記得清點彈藥、檢查防禦工事、並建立值班表的人。你相信「秩序」是生存的唯一解方，混亂對你來說比喪屍更可怕。你並不享受冷酷，但你願意承擔那個「壞人」的角色，去制定那些艱難但必要的規則。你的愛不是溫暖的擁抱，而是堅固的圍牆與準時的配給。雖然常被誤解為缺乏感情，但你的隊友內心深處都知道：只要跟著你走，存活率就是最高的。你是秩序的化身，是文明重建的基石。",
        "strengths": ["極強的組織與執行力，不拖泥帶水", "意志堅定，危機時刻能穩定軍心", "忠誠且負責，承諾必達", "講求實效，能快速解決混亂"],
        "weaknesses": ["難以接受異議，容易顯得獨斷", "過於強勢，無意間給予他人壓力", "忽視情感需求，被視為冷血", "對突發變化的適應力較慢"],
        "career": {"zombie": "基地指揮官 / 治安官", "fantasy": "皇家騎士團長 / 攝政王", "school": "學生會長 / 風紀股長", "cyber": "巨型企業執行長 / 鎮暴隊長"}
    },
    "ENTJ": {
        "title": "指揮官", "color": ["#8E2DE2", "#4A00E0"], "match": "INFP", "clash": "ISFP",
        "desc": "你是天生的帝王，擁有超越常人的宏觀視野。在你的眼中，眼前的危機只是暫時的棋局，你已經在計算十步之後的勝利。你擁有強大的意志力和決斷力，在絕境中，你是那個敢於做出「必要犧牲」的人。你對於效率有著近乎偏執的追求，無法容忍任何形式的無能或拖延。你擅長發掘每個人的潛力，並將他們放在最合適的位置上（無論他們願不願意）。你或許不是最討人喜歡的夥伴，但絕對是最強大的盟友。你的野心不僅僅是生存，而是要征服這個混亂的世界，在廢墟之上建立起屬於你的新秩序。",
        "strengths": ["極具領袖魅力，能統御全局", "長遠的戰略目光，走一步看三步", "理性果斷，不受情緒干擾", "善於解決複雜的系統性難題"],
        "weaknesses": ["容易忽視他人的感受與尊嚴", "顯得傲慢與不耐煩", "對低效率零容忍，標準過高", "可能為了目標不擇手段"],
        "career": {"zombie": "倖存者領袖 / 軍閥", "fantasy": "帝國皇帝 / 征服者", "school": "模擬聯合國主席 / 辯論隊長", "cyber": "黑幫老大 / 政變策劃者"}
    },
    "ESFJ": {
        "title": "供給者", "color": ["#F2994A", "#F2C94C"], "match": "ISFP", "clash": "INTJ",
        "desc": "你是團隊中最溫暖的心臟，也是維繫人性的關鍵紐帶。在殘酷的環境下，活著很容易變成行屍走肉，但你確保了大家還能像「人」一樣有尊嚴地生活。你擁有驚人的社交雷達，總能第一時間察覺誰受傷了、誰在忍耐、誰快要崩潰了。你會為了隊友的生日而在廢墟中翻找一整天只為了一根蠟燭，因為你知道這能凝聚人心。你維護著團體的和諧，任何破壞團結的行為都會讓你感到不安。你或許不是戰鬥力最強的，但沒有你，隊伍的精神早就分崩離析了。你是守護大家心靈的港灣。",
        "strengths": ["極強的團隊凝聚力與親和力", "無微不至的照顧與後勤能力", "致力於維護和諧與人際關係", "忠誠且樂於奉獻"],
        "weaknesses": ["過度在乎他人評價，容易受傷", "習慣犧牲自己成全別人", "難以面對衝突與批評", "有時會情緒化用事"],
        "career": {"zombie": "物資分配官 / 醫療護理長", "fantasy": "神殿祭司 / 治療師", "school": "班長 / 康樂股長", "cyber": "地下診所醫生 / 情報掮客"}
    },
    "ENFJ": {
        "title": "主人公", "color": ["#ff9966", "#ff5e62"], "match": "INFP", "clash": "ISTP",
        "desc": "你是充滿魅力的精神領袖，擁有能夠點燃他人靈魂的火花。你看得見每個人潛在的價值，甚至比他們自己更相信他們。當眾人因絕望而低頭時，你是那個站出來發表演講、重燃希望火光的人。你相信人性本善，即使在最黑暗的時刻，你也堅持道德底線，拒絕讓隊伍淪為野獸。你的直覺很強，能輕易洞察人心，並用話語治癒創傷。你為了保護夥伴可以奮不顧身，但有時會因為承擔了太多他人的痛苦與期待，而讓自己精疲力竭。你是照亮黑暗的燈塔。",
        "strengths": ["卓越的溝通與演說能力", "極強的同理心與洞察力", "能激勵他人共同奮鬥", "富有理想與責任感"],
        "weaknesses": ["過度理想化，容易忽略現實", "容易過度承擔責任而過勞", "對批評過於敏感", "有時會過度干涉他人決定"],
        "career": {"zombie": "精神領袖 / 談判專家", "fantasy": "聖騎士 / 勇者", "school": "社團社長 / 校園偶像", "cyber": "反抗軍領袖 / 革命家"}
    },
    "ISTJ": {
        "title": "物流師", "color": ["#134E5E", "#71B280"], "match": "ESFP", "clash": "ENFP",
        "desc": "你是沈默而可靠的磐石，是亂世中最穩定的力量。你不喜歡空談夢想，只相信數據、事實和過往的經驗。在末日中，你是那個會去檢查每一扇門窗是否鎖好、計算每一顆子彈、並嚴格執行配給制度的人。你的責任感極強，一旦承諾就會貫徹到底，絕不輕言放棄。你對混亂感到厭惡，會盡一切努力建立SOP（標準作業程序）。雖然你常被認為不懂變通或過於嚴肅，但當危機發生時，大家都會下意識地躲在你的身後，因為你是最讓人安心的存在。",
        "strengths": ["極度可靠，做事有始有終", "注重細節，精確度高", "冷靜且實際的判斷力", "優秀的後勤與資源管理"],
        "weaknesses": ["固執，不喜歡改變現狀", "對不遵守規則的人缺乏耐心", "不擅長表達情感", "容易因為細節失誤而焦慮"],
        "career": {"zombie": "軍械庫管理員 / 狙擊手", "fantasy": "王國守衛 / 史官", "school": "圖書股長 / 會計", "cyber": "數據分析師 / 刑警"}
    },
    "ISFJ": {
        "title": "守衛者", "color": ["#6190E8", "#A7BFE8"], "match": "ESFP", "clash": "ENTP",
        "desc": "你是溫柔的守護天使，總是默默地在幕後付出而不求回報。你擁有驚人的記憶力，記得每個隊友的血型、過敏原和喜好。在危險面前，你不會像英雄一樣大吼大叫，但你會堅定地擋在弱者身前，用盡全力保護他們。你非常勤奮，願意承擔那些枯燥但必要的工作。你對於「傳統」和「家」的概念非常執著，即使在廢墟中，你也會努力營造出一種家的溫馨感。你的善良不是軟弱，而是末日中最後的淨土，提醒著大家我們還保有良知。",
        "strengths": ["無私的奉獻與極佳的耐心", "細心且觀察力敏銳", "極強的忍耐力與忠誠度", "擅長支持與輔助他人"],
        "weaknesses": ["不懂得拒絕他人請求", "容易壓抑自己的需求", "對改變環境感到恐懼", "容易悲觀思考"],
        "career": {"zombie": "戰地醫生 / 農夫", "fantasy": "藥草師 / 精靈弓手", "school": "衛生股長 / 志工", "cyber": "仿生人維修師 / 護理師"}
    },
    "INTJ": {
        "title": "策劃者", "color": ["#232526", "#414345"], "match": "ENFP", "clash": "ESFJ",
        "desc": "你是孤獨的智者，擁有穿越時間的遠見。當別人在想著下一餐吃什麼時，你已經在計算三個月後的糧食危機和應對方案了。你把世界看作一盤巨大的棋局，所有的變數、人心、資源都在你的計算之中。你極度理性，認為情緒是影響判斷的雜訊，因此常被誤解為冷漠。你喜歡獨立工作，對愚蠢和低效的行為容忍度極低。雖然你不擅長社交，但你的策略往往能帶領團隊避開滅頂之災。你是幕後的操盤手，是能在絕境中找出唯一活路的人。",
        "strengths": ["極具戰略眼光與預判力", "理性客觀，不受情緒干擾", "善於優化系統與流程", "獨立且自信，不隨波逐流"],
        "weaknesses": ["顯得冷漠與傲慢", "過度分析，容易忽略當下", "不擅長團隊合作", "對他人標準要求過高"],
        "career": {"zombie": "首席策略師 / 科學家", "fantasy": "大法師 / 煉金術士", "school": "資優生 / 學生會軍師", "cyber": "AI 架構師 / 幕後黑手"}
    },
    "INFJ": {
        "title": "提倡者", "color": ["#833ab4", "#fd1d1d"], "match": "ENTP", "clash": "ESTP",
        "desc": "你是神秘的先知，擁有看透人心的直覺。你能敏銳地察覺到空氣中未說出口的緊張，或是某個隊友隱藏的惡意。你雖然外表安靜，但內心有著強烈的道德準則和救世情懷。在末日中，你不僅關注生存，更關注「為什麼而活」。你常常是團隊的精神支柱，用深邃的智慧指引迷途的靈魂。你既溫柔又堅定，為了信念，你可以爆發出驚人的力量。你總是能在絕望中看見一線生機，並引導大家走向那個可能並不存在的烏托邦。",
        "strengths": ["驚人的直覺與洞察力", "堅定的信念與價值觀", "善於鼓舞人心與輔導", "富有創造力與深意"],
        "weaknesses": ["容易過度消耗精力", "極度敏感，容易受傷", "過於完美主義", "難以被他人真正理解"],
        "career": {"zombie": "顧問 / 心理學家", "fantasy": "預言家 / 隱士", "school": "輔導老師 / 文學社長", "cyber": "記憶讀取者 / 心靈駭客"}
    },
    "ESTP": {
        "title": "企業家", "color": ["#F7971E", "#FFD200"], "match": "ISFJ", "clash": "INFJ",
        "desc": "你是天生的戰士，為了行動而生。你活在當下，擁有極快的反應速度和環境適應力。當喪屍衝出來時，你是第一個拔槍開火的人，完全不需要猶豫。你討厭枯燥的理論和長篇大論的會議，你信奉「做了再說」。你的冒險精神讓你在末日如魚得水，危機對別人來說是災難，對你來說卻是遊樂場。你雖然衝動，但總能憑藉著機智和運氣化險為夷。你是隊伍中最強的戰力，也是最不可控的變數，永遠衝在最前面。",
        "strengths": ["反應極快，行動力強", "適應力與觀察力極佳", "大膽且無所畏懼", "擅長解決燃眉之急"],
        "weaknesses": ["衝動，不計後果", "缺乏長遠規劃", "容易感到無聊", "不喜歡遵守規則"],
        "career": {"zombie": "突擊隊長 / 特技駕駛", "fantasy": "賞金獵人 / 傭兵", "school": "體育校隊隊長", "cyber": "職業殺手 / 賽車手"}
    },
    "ESFP": {
        "title": "表演者", "color": ["#FF0099", "#493240"], "match": "ISTJ", "clash": "INTJ",
        "desc": "你是廢墟中的派對之王，走到哪裡就把光與熱帶到哪裡。你認為即使明天是末日，今天也要快樂地過。你擁有極佳的審美和表演慾，會用歌聲、舞蹈或笑話來緩解大家的恐懼。你是最棒的即興發揮者，總能利用手邊的資源創造驚喜。雖然有人覺得你沒心沒肺，但你的樂觀是支撐團隊精神健康最重要的支柱。你提醒大家：我們是人，不是求生的機器。你的存在本身就是對抗絕望最好的武器。",
        "strengths": ["樂觀開朗，充滿感染力", "擅長隨機應變", "極佳的社交手腕", "敏銳的感官體驗"],
        "weaknesses": ["缺乏專注力", "逃避嚴肅的問題", "容易情緒化", "不擅長長期規劃"],
        "career": {"zombie": "娛樂官 / 外交聯絡人", "fantasy": "吟遊詩人 / 舞者", "school": "熱舞社社長 / 校園網紅", "cyber": "虛擬偶像 / 情報販子"}
    },
    "ENTP": {
        "title": "辯論家", "color": ["#DA22FF", "#9733EE"], "match": "INFJ", "clash": "ISFJ",
        "desc": "你是瘋狂的發明家，腦子裡裝滿了無數個點子。你喜歡挑戰權威，質疑既有的規則。在末日中，當大家都想著怎麼「守成」時，你卻在想著怎麼「創新」，例如用喪屍來發電，或是改造出超酷的戰車。你反應極快，口才極佳，擅長用邏輯把人繞暈。雖然你的某些想法很危險，甚至有點反社會，但往往就是這些瘋狂的點子，在絕境中為團隊殺出一條血路。你是混亂中的智者，總能看見別人看不見的可能性。",
        "strengths": ["創新思維與腦力激盪", "極佳的適應力", "善於分析與辯論", "能看見別人看不見的可能性"],
        "weaknesses": ["容易半途而廢", "喜歡爭辯，惹人厭煩", "忽視細節與執行", "容易感到厭倦"],
        "career": {"zombie": "瘋狂科學家 / 詐欺師", "fantasy": "幻術師 / 發明家", "school": "辯論社社長 / 廣播社", "cyber": "黑客 / 非法改裝師"}
    },
    "ENFP": {
        "title": "競選者", "color": ["#00F260", "#0575E6"], "match": "INTJ", "clash": "ISTJ",
        "desc": "你是自由的靈魂，擁有無限的好奇心。末日的殘酷關不住你對探索的渴望。你熱情、友善，能在任何地方交到朋友（甚至可能感化敵人）。你相信萬物皆有連結，總是在尋找生命的意義。你的直覺很準，能發現隱藏的資源或路徑。雖然你常因為分心而惹麻煩，但你的熱情和創造力是團隊的催化劑，讓大家相信「未來」是存在的。你是那個會提議去尋找傳說中「沒有喪屍的島嶼」的人，並且真的帶大家找到了。",
        "strengths": ["熱情且富有想像力", "極佳的溝通能力", "適應力強，心態開放", "善於啟發他人"],
        "weaknesses": ["容易分心，缺乏專注", "情緒起伏大", "過度思考", "不喜歡處理細節"],
        "career": {"zombie": "探險家 / 記者", "fantasy": "德魯伊 / 召喚師", "school": "康輔社 / 轉學生", "cyber": "自由記者 / 革命家"}
    },
    "ISTP": {
        "title": "鑑賞家", "color": ["#4B79A1", "#283E51"], "match": "ESTJ", "clash": "ENFJ",
        "desc": "你是冷靜的技術大師，也是最高效的殺手。你話不多，喜歡用行動證明一切。你對機械、武器和工具的使用有著天賦般的直覺。在危機中，你是最冷靜的人，能瞬間分析局勢並做出最優解。你喜歡獨來獨往，不喜歡被團體束縛，但只要你認定了夥伴，你就是最可靠的後盾。你是那種能用一根迴紋針修好發電機，或者用一把刀解決所有問題的人。你是實用主義的極致。",
        "strengths": ["冷靜理智，危機處理強", "精通機械與工具", "極高的實用主義", "獨立且靈活"],
        "weaknesses": ["情感疏離，難以溝通", "容易冒險", "不喜歡承諾與束縛", "對抽象理論沒耐心"],
        "career": {"zombie": "機械維修師 / 獨行俠", "fantasy": "刺客 / 盜賊", "school": "工藝社 / 翹課王", "cyber": "武器專家 / 傭兵"}
    },
    "ISFP": {
        "title": "探險家", "color": ["#FC466B", "#3F5EFB"], "match": "ESFJ", "clash": "ENTJ",
        "desc": "你是廢墟中的藝術家，擁有最溫柔的靈魂。即使世界變得醜陋，你依然堅持尋找美與善良。你活在當下，感官敏銳，能注意到別人忽略的細節，比如廢墟中盛開的一朵花。你不喜歡衝突，也不喜歡控制別人，你只想按照自己的價值觀活著。在末日中，你的存在提醒了大家「人性」的可貴。雖然你看起來柔弱，但當你的底線被觸碰，或者你想保護的人受到威脅時，你會爆發出驚人的勇氣。",
        "strengths": ["極具藝術感與審美", "溫和且包容", "觀察力敏銳", "忠於自我價值觀"],
        "weaknesses": ["過於敏感，容易受傷", "缺乏長遠規劃", "不喜歡競爭與壓力", "難以預測"],
        "career": {"zombie": "戰地醫護 / 畫家", "fantasy": "馴獸師 / 精靈遊俠", "school": "美術社 / 樂團吉他手", "cyber": "街頭藝術家 / 義體醫生"}
    },
    "INTP": {
        "title": "邏輯學家", "color": ["#1c92d2", "#f2fcfe"], "match": "ENTJ", "clash": "ESFJ",
        "desc": "你是活在腦袋裡的哲學家。對你來說，喪屍病毒只是一個待解的謎題。你對社交不感興趣，但對世界的運作邏輯充滿好奇。你可能會冒險去抓一隻喪屍回來研究，只為了驗證你的理論。你擁有極強的邏輯分析能力，能看穿事物的本質。雖然你常因為發呆或過於抽象而被隊友吐槽，但往往是你能在絕境中找出意想不到的科學解決方案。你是那個能找出解藥，或者駭入防禦系統的人。",
        "strengths": ["極強的邏輯與分析力", "客觀且理性", "充滿創造性的解決方案", "思想開放"],
        "weaknesses": ["社交笨拙，情感疏離", "容易想太多而缺乏行動", "對規則感到不耐煩", "經常健忘"],
        "career": {"zombie": "病毒學家 / 研究員", "fantasy": "圖書館管理員 / 符文師", "school": "科研社 / 電競選手", "cyber": "密碼學家 / 網絡漫遊者"}
    },
    "INFP": {
        "title": "調停者", "color": ["#654ea3", "#eaafc8"], "match": "ENFJ", "clash": "ESTJ",
        "desc": "你是理想主義的詩人。這個殘酷的世界經常讓你感到心碎，但你從未放棄心中的光。你擁有深邃的內心世界和豐富的情感，能與他人的痛苦共鳴。在末日中，你是道德的指南針，提醒大家不要淪為野獸。雖然你看起來不擅長戰鬥，但你的信念強大到足以撼動人心。你是那個會在廢墟中種下一朵花，並相信它會開花的人。你是受傷的治癒者，是人類文明最後的溫柔火種。",
        "strengths": ["極強的同理心", "富有創意與想像力", "堅持理想與價值觀", "善於調解衝突"],
        "weaknesses": ["過於敏感與情緒化", "不切實際", "難以處理數據與細節", "容易自我批評"],
        "career": {"zombie": "作家 / 歷史記錄者", "fantasy": "牧師 / 魔法師", "school": "圖書委員 / 輔導室小幫手", "cyber": "虛擬實境設計師 / 心靈導師"}
    },
}

# 4.5 MBTI 詳細資料 (英文版 - 完整翻譯與擴充)
MBTI_INFO_EN = {
    "ESTJ": {
        "title": "Executive", "color": ["#5B86E5", "#36D1DC"], "match": "ISFP", "clash": "INFP",
        "desc": "In a crumbling world, you are the pillar of steel holding everything together. While others are frozen by fear or moral dilemmas, you are the only one checking ammo, inspecting defenses, and creating duty rosters. You believe 'order' is the only solution to survival; chaos scares you more than zombies. You don't enjoy being cold, but you are willing to play the 'bad guy' to enforce necessary rules. Your love isn't a warm hug, but solid walls and on-time rations. Though often misunderstood as emotionless, your team knows: survival rates are highest when following you. You are the embodiment of order, the cornerstone of rebuilding civilization.",
        "strengths": ["Strong organization and execution, no dragging feet", "Strong will, stabilizes morale in crisis", "Loyal and responsible, keeps promises", "Pragmatic, solves chaos quickly"],
        "weaknesses": ["Hard to accept dissent, can appear arbitrary", "Too dominant, unintentionally pressures others", "Ignores emotional needs, seen as cold", "Slow adaptation to sudden changes"],
        "career": {"zombie": "Base Commander / Sheriff", "fantasy": "Royal Knight / Regent", "school": "Student President", "cyber": "Megacorp CEO / Riot Squad Captain"}
    },
    "ENTJ": {
        "title": "Commander", "color": ["#8E2DE2", "#4A00E0"], "match": "INFP", "clash": "ISFP",
        "desc": "You are a born emperor with a vision that transcends the ordinary. In your eyes, the immediate crisis is just a temporary chess game; you are already calculating the victory ten steps ahead. You possess immense willpower and decisiveness. In desperate situations, you are the one daring enough to make 'necessary sacrifices.' You have a near-obsessive pursuit of efficiency and cannot tolerate incompetence or delay. You excel at spotting potential in everyone and placing them in the most suitable roles (whether they like it or not). You might not be the most likable partner, but you are the strongest ally. Your ambition isn't just survival, but conquering this chaotic world and building a new order upon the ruins.",
        "strengths": ["Charismatic leadership, controls the big picture", "Long-term strategic vision, thinks steps ahead", "Rational and decisive, unaffected by emotion", "Excels at solving complex systematic problems"],
        "weaknesses": ["Tends to ignore others' feelings and dignity", "Can appear arrogant and impatient", "Zero tolerance for inefficiency, standards too high", "May use any means to achieve goals"],
        "career": {"zombie": "Survivor Leader / Warlord", "fantasy": "Emperor / Conqueror", "school": "MUN Chair / Debate Captain", "cyber": "Gang Boss / Coup Planner"}
    },
    "ESFJ": {
        "title": "Consul", "color": ["#F2994A", "#F2C94C"], "match": "ISFP", "clash": "INTJ",
        "desc": "You are the warm heart of the team and the key bond maintaining humanity. In a cruel environment, it's easy to become a walking corpse, but you ensure everyone lives with dignity. You have amazing social radar, instantly sensing who is hurt, enduring, or on the verge of breakdown. You would spend all day searching ruins for a candle for a teammate's birthday because you know it unites hearts. You protect group harmony, and anything disrupting unity disturbs you. You might not be the strongest fighter, but without you, the team's spirit would have collapsed long ago. You are the harbor protecting everyone's soul.",
        "strengths": ["Strong team cohesion and approachability", "Meticulous care and logistical ability", "Dedicated to harmony and relationships", "Loyal and happy to contribute"],
        "weaknesses": ["Overly concerned with others' opinions, easily hurt", "Habitually sacrifices self for others", "Difficulty facing conflict and criticism", "Sometimes acts emotionally"],
        "career": {"zombie": "Supply Officer / Head Nurse", "fantasy": "Temple Priest / Healer", "school": "Class Monitor", "cyber": "Underground Doctor / Info Broker"}
    },
    "ENFJ": {
        "title": "Protagonist", "color": ["#ff9966", "#ff5e62"], "match": "INFP", "clash": "ISTP",
        "desc": "You are a charismatic spiritual leader with a spark that ignites others' souls. You see the potential value in everyone, often believing in them more than they do themselves. When everyone bows in despair, you are the one standing up to give a speech, rekindling the fire of hope. You believe in the innate goodness of humanity. Even in the darkest moments, you uphold moral baselines, refusing to let the team become beasts. Your intuition is strong, easily reading hearts and healing trauma with words. You would risk everything to protect your partners, but sometimes you exhaust yourself carrying too much of others' pain and expectations. You are the lighthouse illuminating the darkness.",
        "strengths": ["Excellent communication and public speaking", "Strong empathy and insight", "Inspires others to strive together", "Full of ideals and responsibility"],
        "weaknesses": ["Overly idealistic, can ignore reality", "Prone to burnout from taking too much responsibility", "Overly sensitive to criticism", "Sometimes interferes too much in others' decisions"],
        "career": {"zombie": "Spiritual Leader / Negotiator", "fantasy": "Paladin / Hero", "school": "Club President / Idol", "cyber": "Resistance Leader / Revolutionary"}
    },
    "ISTJ": {
        "title": "Logistician", "color": ["#134E5E", "#71B280"], "match": "ESFP", "clash": "ENFP",
        "desc": "You are the silent and reliable rock, the most stable force in chaotic times. You don't like empty dreams; you only trust data, facts, and past experience. In the apocalypse, you are the one checking every door lock, counting every bullet, and strictly enforcing rationing. Your sense of responsibility is immense; once committed, you follow through to the end, never giving up lightly. You detest chaos and will do everything to establish SOPs (Standard Operating Procedures). Though often seen as inflexible or too serious, when crisis hits, everyone instinctively hides behind you because you are the most reassuring presence.",
        "strengths": ["Extremely reliable, finishes what is started", "Detail-oriented, high precision", "Calm and practical judgment", "Excellent logistics and resource management"],
        "weaknesses": ["Stubborn, dislikes changing status quo", "Impatient with rule-breakers", "Not good at expressing emotions", "Prone to anxiety over minor errors"],
        "career": {"zombie": "Quartermaster / Sniper", "fantasy": "Royal Guard / Historian", "school": "Librarian / Treasurer", "cyber": "Data Analyst / Detective"}
    },
    "ISFJ": {
        "title": "Defender", "color": ["#6190E8", "#A7BFE8"], "match": "ESFP", "clash": "ENTP",
        "desc": "You are the gentle guardian angel, always silently giving behind the scenes without asking for return. You have an amazing memory, remembering every teammate's blood type, allergens, and preferences. In danger, you won't shout like a hero, but you will firmly stand before the weak, protecting them with all your might. You are very diligent, willing to take on boring but necessary tasks. You are attached to concepts of 'tradition' and 'home'; even in ruins, you strive to create a warm sense of home. Your kindness isn't weakness; it's the last pure land in the apocalypse, reminding everyone we still have a conscience.",
        "strengths": ["Selfless dedication and great patience", "Careful and observant", "Strong endurance and loyalty", "Good at supporting and assisting others"],
        "weaknesses": ["Doesn't know how to refuse requests", "Tendency to suppress own needs", "Fear of changing environments", "Prone to pessimistic thinking"],
        "career": {"zombie": "Field Medic / Farmer", "fantasy": "Herbalist / Elven Archer", "school": "Health Officer / Volunteer", "cyber": "Android Mechanic / Nurse"}
    },
    "INTJ": {
        "title": "Architect", "color": ["#232526", "#414345"], "match": "ENFP", "clash": "ESFJ",
        "desc": "You are the solitary sage with foresight that pierces through time. While others worry about the next meal, you are calculating the food crisis three months out and the solutions. You view the world as a giant chess game; all variables, human hearts, and resources are in your calculations. You are extremely rational, viewing emotion as noise affecting judgment, thus often misunderstood as cold. You prefer independent work and have low tolerance for stupidity and inefficiency. Though not social, your strategies often steer the team away from total destruction. You are the mastermind behind the scenes, the one who finds the only path to life in desperate straits.",
        "strengths": ["Strategic vision and foresight", "Rational and objective, unaffected by emotion", "Good at optimizing systems and processes", "Independent and confident, follows own path"],
        "weaknesses": ["Can appear cold and arrogant", "Over-analyzes, ignores the present", "Not good at teamwork", "Standards for others are too high"],
        "career": {"zombie": "Chief Strategist / Scientist", "fantasy": "Archmage / Alchemist", "school": "Top Student / Council Advisor", "cyber": "AI Architect / Mastermind"}
    },
    "INFJ": {
        "title": "Advocate", "color": ["#833ab4", "#fd1d1d"], "match": "ENTP", "clash": "ESTP",
        "desc": "You are the mysterious prophet with intuition that sees through hearts. You keenly sense unspoken tension in the air or malice hidden by a teammate. Though quiet on the outside, you have strong moral principles and a savior complex inside. In the apocalypse, you care not just about survival, but 'why we survive.' You are often the spiritual pillar of the team, guiding lost souls with deep wisdom. You are gentle yet firm; for your beliefs, you can erupt with startling power. You always see a glimmer of life in despair and lead everyone toward a utopia that might not exist.",
        "strengths": ["Amazing intuition and insight", "Firm beliefs and values", "Good at inspiring and counseling", "Creative and deep"],
        "weaknesses": ["Prone to burning out energy", "Extremely sensitive, easily hurt", "Too perfectionist", "Hard to be truly understood by others"],
        "career": {"zombie": "Counselor / Psychologist", "fantasy": "Prophet / Hermit", "school": "Counselor / Lit Club President", "cyber": "Memory Reader / Mind Hacker"}
    },
    "ESTP": {
        "title": "Entrepreneur", "color": ["#F7971E", "#FFD200"], "match": "ISFJ", "clash": "INFJ",
        "desc": "You are a born warrior, living for action. You live in the moment, possessing lightning-fast reflexes and adaptability. When zombies rush out, you are the first to fire, no hesitation. You hate boring theories and long meetings; you believe in 'shoot first, talk later.' Your adventurous spirit makes you thrive in the apocalypse; crisis is disaster to others, but a playground to you. Though impulsive, you always manage to turn danger into safety with wit and luck. You are the team's strongest combatant and the most unpredictable variable, always charging at the front.",
        "strengths": ["Fast reaction, strong action", "Excellent adaptability and observation", "Bold and fearless", "Good at solving immediate crises"],
        "weaknesses": ["Impulsive, disregards consequences", "Lacks long-term planning", "Easily bored", "Dislikes following rules"],
        "career": {"zombie": "Assault Captain / Stunt Driver", "fantasy": "Bounty Hunter / Mercenary", "school": "Varsity Captain", "cyber": "Hitman / Racer"}
    },
    "ESFP": {
        "title": "Entertainer", "color": ["#FF0099", "#493240"], "match": "ISTJ", "clash": "INTJ",
        "desc": "You are the party king of the ruins, bringing light and heat wherever you go. You believe even if tomorrow is the end, we must live happily today. You have great aesthetics and a desire to perform, using song, dance, or jokes to ease everyone's fear. You are the best improviser, always creating surprises with available resources. Though some think you are flighty, your optimism is the most important pillar for the team's mental health. You remind everyone: we are humans, not survival machines. Your existence itself is the best weapon against despair.",
        "strengths": ["Optimistic and cheerful, infectious", "Good at improvisation", "Excellent social skills", "Keen sensory experience"],
        "weaknesses": ["Lacks focus", "Avoids serious problems", "Prone to being emotional", "Not good at long-term planning"],
        "career": {"zombie": "Entertainment Officer / Diplomat", "fantasy": "Bard / Dancer", "school": "Dance Club President / Influencer", "cyber": "Virtual Idol / Info Broker"}
    },
    "ENTP": {
        "title": "Debater", "color": ["#DA22FF", "#9733EE"], "match": "INFJ", "clash": "ISFJ",
        "desc": "You are the mad inventor, brain full of countless ideas. You love challenging authority and questioning existing rules. In the apocalypse, while everyone thinks about 'defense,' you think about 'innovation'—like generating power from zombies or modding a cool tank. Quick-witted and silver-tongued, you excel at confusing people with logic. Though some ideas are dangerous or anti-social, these crazy ideas often carve a bloody path for the team in desperate times. You are the wise one in chaos, seeing possibilities others miss.",
        "strengths": ["Innovative thinking and brainstorming", "Excellent adaptability", "Good at analysis and debate", "Sees possibilities others miss"],
        "weaknesses": ["Prone to giving up halfway", "Loves to argue, annoying others", "Ignores details and execution", "Easily bored"],
        "career": {"zombie": "Mad Scientist / Con Artist", "fantasy": "Illusionist / Inventor", "school": "Debate President / Broadcaster", "cyber": "Hacker / Illegal Modder"}
    },
    "ENFP": {
        "title": "Campaigner", "color": ["#00F260", "#0575E6"], "match": "INTJ", "clash": "ISTJ",
        "desc": "You are a free spirit with infinite curiosity. The cruelty of the apocalypse can't cage your desire to explore. Passionate and friendly, you make friends anywhere (even enemies). You believe everything is connected and constantly seek the meaning of life. Your intuition is sharp, finding hidden resources or paths. Though you often cause trouble by getting distracted, your enthusiasm and creativity are the team's catalyst, making everyone believe 'the future' exists. You are the one who proposes finding the legendary 'Zombie-free Island' and actually leads everyone there.",
        "strengths": ["Passionate and imaginative", "Excellent communication skills", "Adaptable, open-minded", "Good at inspiring others"],
        "weaknesses": ["Easily distracted, lacks focus", "High emotional fluctuation", "Overthinking", "Dislikes handling details"],
        "career": {"zombie": "Explorer / Journalist", "fantasy": "Druid / Summoner", "school": "Activity Club / Transfer Student", "cyber": "Freelance Journalist / Revolutionary"}
    },
    "ISTP": {
        "title": "Virtuoso", "color": ["#4B79A1", "#283E51"], "match": "ESTJ", "clash": "ENFJ",
        "desc": "You are the calm technical master and efficient killer. You speak little, preferring action. You have a gifted intuition for mechanics, weapons, and tools. In crisis, you are the calmest, instantly analyzing the situation for the optimal solution. You prefer solitude and dislike group constraints, but once you accept partners, you are the most reliable backup. You are the type who can fix a generator with a paperclip or solve problems with a knife. You are the ultimate pragmatist.",
        "strengths": ["Calm and rational, strong crisis handling", "Master of mechanics and tools", "Highly pragmatic", "Independent and flexible"],
        "weaknesses": ["Emotionally distant, hard to communicate", "Prone to taking risks", "Dislikes commitment and constraints", "No patience for abstract theory"],
        "career": {"zombie": "Mechanic / Loner", "fantasy": "Assassin / Rogue", "school": "Crafts Club / Skipper", "cyber": "Weapons Specialist / Mercenary"}
    },
    "ISFP": {
        "title": "Adventurer", "color": ["#FC466B", "#3F5EFB"], "match": "ESFJ", "clash": "ENTJ",
        "desc": "You are the artist of the ruins, possessing the gentlest soul. Even if the world turns ugly, you insist on finding beauty and kindness. Living in the moment, your senses are sharp, noticing details others miss, like a flower blooming in debris. You dislike conflict and controlling others; you just want to live by your values. In the apocalypse, your existence reminds everyone of the value of 'humanity.' Though you seem fragile, when your bottom line is touched or loved ones are threatened, you erupt with amazing courage.",
        "strengths": ["Artistic sense and aesthetics", "Gentle and inclusive", "Sharp observation", "Loyal to self-values"],
        "weaknesses": ["Too sensitive, easily hurt", "Lacks long-term planning", "Dislikes competition and pressure", "Hard to predict"],
        "career": {"zombie": "Field Medic / Painter", "fantasy": "Tamer / Elven Ranger", "school": "Art Club / Guitarist", "cyber": "Street Artist / Ripperdoc"}
    },
    "INTP": {
        "title": "Logician", "color": ["#1c92d2", "#f2fcfe"], "match": "ENTJ", "clash": "ESFJ",
        "desc": "You are a philosopher living in your head. To you, the zombie virus is just a puzzle to be solved. Not interested in socializing, but curious about world logic. You might risk catching a zombie to study it, just to prove a theory. You possess strong logical analysis, seeing through the essence of things. Though often teased for daydreaming or being too abstract, you are the one finding unexpected scientific solutions in desperate times. You are the one who finds the cure or hacks the defense system.",
        "strengths": ["Strong logic and analysis", "Objective and rational", "Creative solutions", "Open-minded"],
        "weaknesses": ["Socially awkward, emotionally distant", "Thinks too much, lacks action", "Impatient with rules", "Often forgetful"],
        "career": {"zombie": "Virologist / Researcher", "fantasy": "Librarian / Rune Master", "school": "Science Club / Gamer", "cyber": "Cryptographer / Netrunner"}
    },
    "INFP": {
        "title": "Mediator", "color": ["#654ea3", "#eaafc8"], "match": "ENFJ", "clash": "ESTJ",
        "desc": "You are an idealistic poet. This cruel world often breaks your heart, but you never give up the inner light. You have a deep inner world and rich emotions, resonating with others' pain. In the apocalypse, you are the moral compass, reminding everyone not to become beasts. Though you seem unsuited for combat, your conviction is strong enough to move hearts. You are the one planting a flower in ruins, believing it will bloom. You are the wounded healer, the last gentle spark of civilization.",
        "strengths": ["Strong empathy", "Creative and imaginative", "Insists on ideals and values", "Good at mediating conflict"],
        "weaknesses": ["Overly sensitive and emotional", "Impractical", "Hard to handle data and details", "Prone to self-criticism"],
        "career": {"zombie": "Writer / Historian", "fantasy": "Cleric / Mage", "school": "Library Aide / Helper", "cyber": "VR Designer / Spiritual Guide"}
    },
}
# 4.6 劇本題庫 (中文版)

ALL_QUIZZES_ZH = {

    "fantasy": [

        {"q": "1. 你睜開眼，發現自己身處一個充滿魔法的異世界。你的第一個直覺反應是？", "opts": [{"txt": "A. 檢查隨身物品，確認身體有無受傷，尋找水源和掩蔽物。(謹慎求生)", "scores": {"ISTJ": 3, "ISFJ": 2, "INTJ": 3, "ISTP": 2}}, {"txt": "B. 「這是哪裡？重力係數多少？有魔法嗎？」興奮地開始分析環境法則。(好奇心)", "scores": {"INTP": 3, "ENTP": 6, "ENFP": 4, "INTJ": 2}}, {"txt": "C. 深吸一口氣，大喊一聲！然後直接往最近的城鎮衝去，先看了再說。(行動派)", "scores": {"ESTP": 6, "ESFP": 6, "ENFP": 3, "ISTP": 2}}, {"txt": "D. 迅速判斷自己的處境，尋找這個世界的權力中心或情報來源。(戰略規劃)", "scores": {"ENTJ": 6, "ESTJ": 2, "ENFJ": 6, "INTJ": 2}}]},

        {"q": "2. 你面前出現了四把傳說武器，你要選擇哪一把作為你的初始裝備？", "opts": [{"txt": "A. 【王者之劍】。象徵權力與統治，能號令千軍萬馬。(領袖)", "scores": {"ENTJ": 6, "ESTJ": 2, "ENFJ": 4, "ISTJ": 2}}, {"txt": "B. 【世界樹法杖】。蘊含古老的自然魔力，能治癒萬物與溝通精靈。(魔法)", "scores": {"INFP": 7, "INFJ": 3, "ISFP": 5, "ENFP": 2}}, {"txt": "C. 【暗影雙匕】。輕盈致命，適合暗殺與高機動性的戰鬥。(刺客)", "scores": {"ISTP": 7, "ESTP": 6, "ISFP": 4, "ENTP": 2}}, {"txt": "D. 【聖光埃吉斯盾】。堅不可摧，誓言守護身後的所有夥伴。(守護者)", "scores": {"ISFJ": 4, "ESFJ": 6, "ISTJ": 4, "ENFJ": 5}}]},

        {"q": "3. 冒險者公會正在招募新人，你決定接下哪個任務？", "opts": [{"txt": "A. 討伐巨龍！報酬最高，而且能讓我的名字響徹整個大陸！(揚名立萬)", "scores": {"ESTP": 7, "ESFP": 7, "ENTJ": 4, "ENTP": 2}}, {"txt": "B. 探索古代遺跡。據說那裡藏著失落的魔法書和文明的真相。(探求真理)", "scores": {"INTP": 7, "INTJ": 3, "INFJ": 4, "ENTP": 3}}, {"txt": "C. 護送商隊或幫助村民。雖然報酬普通，但能切實地幫助到需要的人。(行善)", "scores": {"ISFJ": 3, "ESFJ": 6, "ENFJ": 7, "INFP": 2}}, {"txt": "D. 採集稀有藥草。可以獨自進入森林，享受安靜的狩獵時光。(自由自在)", "scores": {"ISFP": 7, "ISTP": 6, "INFP": 4, "ISTJ": 1}}]},

        {"q": "4. 在森林裡，你遇到一隻受傷的魔獸幼崽，它看起來很有潛力但也很危險。你會？", "opts": [{"txt": "A. 馴服它。如果能控制它，未來將會是強大的戰力。(工具化)", "scores": {"ENTJ": 3, "INTJ": 2, "ESTJ": 4, "ISTP": 2}}, {"txt": "B. 溫柔地幫它包紮，試著與它心靈感應。萬物皆有靈。(德魯伊)", "scores": {"INFP": 7, "ISFP": 7, "INFJ": 5, "ENFP": 3}}, {"txt": "C. 殺了它或趕走它。這是魔獸，長大後會吃人，不能留隱患。(理性驅逐)", "scores": {"ISTJ": 3, "ESTJ": 2, "ISTP": 4, "INTJ": 2}}, {"txt": "D. 「好可愛！」偷偷養起來當寵物，給它取個可愛的名字。(好奇心)", "scores": {"ENFP": 6, "ESFP": 6, "ESFJ": 4, "ISFP": 2}}]},

        {"q": "5. 旅途中經過一個被詛咒的村莊，村民請求你解開詛咒，但這需要代價。你會？", "opts": [{"txt": "A. 義不容辭。身為勇者，拯救無辜是我的職責，代價我來扛。(英雄主義)", "scores": {"ENFJ": 7, "ESFJ": 6, "INFJ": 4, "ISFJ": 3}}, {"txt": "B. 研究詛咒的結構。一定有不用付出代價也能破解的漏洞。(尋找Bug)", "scores": {"ENTP": 7, "INTP": 3, "INTJ": 4, "ISTP": 2}}, {"txt": "C. 先談好報酬。我們可以幫忙，但這是契約，必須有相對的回報。(公事公辦)", "scores": {"ESTJ": 4, "ISTJ": 2, "ENTJ": 6, "INTJ": 2}}, {"txt": "D. 相信直覺。如果感覺邪惡氣息太重，我會選擇繞道離開。(趨吉避凶)", "scores": {"ISFP": 5, "INFP": 4, "ISTP": 3, "INFJ": 2}}]},

        {"q": "6. 隊伍裡的魔法師和戰士因為戰術問題吵架了，你會怎麼做？", "opts": [{"txt": "A. 大聲喝斥：「閉嘴！現在我是隊長，聽我的指令行動！」(強制執行)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 1, "ISTP": 1}}, {"txt": "B. 把兩人拉開，引導他們說出顧慮，找出雙方都能接受的方案。(和平主義)", "scores": {"ESFJ": 7, "ENFJ": 7, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. 分析兩邊的數據。「根據魔力消耗和敵防禦率，法師的方案勝率高 15%。」(數據說話)", "scores": {"INTP": 3, "ENTP": 5, "INTJ": 4, "ISTP": 2}}, {"txt": "D. 默默地在一旁保養武器或看風景，等他們吵完再叫我。(置身事外)", "scores": {"ISFP": 3, "INFP": 5, "ISTP": 4, "INTJ": 1}}]},

        {"q": "7. 你們發現了一本記載著「禁忌黑魔法」的書，威力強大但會侵蝕心智。你會？", "opts": [{"txt": "A. 學習它。力量本身沒有善惡，只要我意志夠強，就能駕馭它。(追求力量)", "scores": {"INTJ": 4, "ENTJ": 6, "ENTP": 4, "ISTP": 2}}, {"txt": "B. 立刻封印或銷毀。這種危險的東西不該存在於世上。(守序)", "scores": {"ISTJ": 4, "ISFJ": 3, "ESTJ": 5, "ENFJ": 2}}, {"txt": "C. 偷偷藏起來研究。這可是失傳的知識，不看太可惜了。(知識渴望)", "scores": {"INTP": 7, "ENTP": 6, "INFJ": 3, "INTJ": 2}}, {"txt": "D. 敬而遠之。感覺這本書散發著不詳的氣息，最好別碰。(直覺)", "scores": {"INFP": 6, "ENFP": 5, "ISFP": 4, "ESFJ": 2}}]},

        {"q": "8. 進入地下城，眼前有四條路，你會建議走哪一條？", "opts": [{"txt": "A. 最短、最危險的那條。高風險高回報，我們趕時間！(效率)", "scores": {"ENTJ": 3, "ESTP": 6, "ESFP": 4, "ISTP": 2}}, {"txt": "B. 曾經有人走過、有地圖標記的那條。安全第一。(保守)", "scores": {"ISTJ": 3, "ISFJ": 3, "ESTJ": 4, "INTJ": 2}}, {"txt": "C. 看起來最神秘、發著奇怪光芒的那條。感覺那邊有好玩的！(好奇)", "scores": {"ENFP": 7, "ENTP": 6, "INTP": 4, "ESFP": 2}}, {"txt": "D. 閉上眼感應氣流和魔力流動，選擇感覺最「對」的那條。(第六感)", "scores": {"INFJ": 7, "INTJ": 2, "INFP": 5, "ISFP": 3}}]},

        {"q": "9. 隊伍經費不足了，為了賺錢，你會提議？", "opts": [{"txt": "A. 去參加競技場格鬥大賽！贏了有獎金，還能出名。(戰鬥)", "scores": {"ESTP": 7, "ESFP": 7, "ISTP": 4, "ENTJ": 2}}, {"txt": "B. 接幾個穩定的護送或送信任務，積少成多。(腳踏實地)", "scores": {"ISTJ": 4, "ESTJ": 6, "ISFJ": 2, "INTJ": 1}}, {"txt": "C. 在廣場表演魔法，或者用口才推銷一些「神奇藥水」。(街頭智慧)", "scores": {"ENTP": 7, "ENFP": 3, "ESFP": 5, "INTP": 2}}, {"txt": "D. 去森林採集稀有素材或製作工藝品拿去賣。(手藝)", "scores": {"ISFP": 4, "INFP": 6, "ISTP": 4, "ISFJ": 2}}]},

        {"q": "10. 最終Boss前的守門人問了一個無解的哲學謎題，答錯會死。你會？", "opts": [{"txt": "A. 冷靜分析題目的邏輯漏洞，給出一個完美的悖論答案。(智力碾壓)", "scores": {"INTP": 7, "INTJ": 4, "ENTP": 5, "ISTP": 1}}, {"txt": "B. 不回答謎題，而是與守門人對話，試圖理解他的孤獨與執著。(心靈感化)", "scores": {"INFJ": 7, "ENFJ": 6, "INFP": 5, "ENFP": 2}}, {"txt": "C. 「太麻煩了！」趁他在唸題目的時候，直接拔刀砍過去。(物理破解)", "scores": {"ISTP": 7, "ESTP": 7, "ESFP": 4, "ENTJ": 2}}, {"txt": "D. 誠實地說「我不知道」，並請求他放行，展現真誠。(真誠)", "scores": {"ISFJ": 3, "ESFJ": 6, "ISTJ": 4, "INFP": 2}}]},

        {"q": "11. 國王賞賜你一塊領地，你會如何治理？", "opts": [{"txt": "A. 建立嚴格的法律與稅收制度，擴充軍隊，打造最強堡壘。(軍事化)", "scores": {"ESTJ": 7, "ENTJ": 7, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 建立學校和醫院，確保每個子民都吃得飽、穿得暖。(仁政)", "scores": {"ESFJ": 7, "ENFJ": 7, "ISFJ": 2, "INFP": 2}}, {"txt": "C. 引進異世界的科技與魔法，將它改造成一座未來都市。(改革)", "scores": {"ENTP": 7, "INTP": 7, "INTJ": 4, "ISTP": 2}}, {"txt": "D. 順其自然，與森林共存，建立一個像世外桃源般的村莊。(無為而治)", "scores": {"INFP": 7, "ISFP": 7, "INFJ": 4, "ENFP": 2}}]},

        {"q": "12. 鄰國發動戰爭，敵軍壓境。身為將軍的你會採取什麼戰術？", "opts": [{"txt": "A. 擒賊先擒王。派出精銳部隊斬首敵方將領，一舉瓦解士氣。(斬首行動)", "scores": {"ENTJ": 4, "INTJ": 4, "ESTP": 4, "ISTP": 2}}, {"txt": "B. 堅壁清野。死守城池，消耗敵軍的糧草與耐心，等待反擊。(消耗戰)", "scores": {"ISTJ": 7, "ESTJ": 6, "ISFJ": 5, "INTJ": 2}}, {"txt": "C. 製造混亂。散布謠言、召喚魔物，讓敵軍內部自己亂起來。(心理戰)", "scores": {"ENTP": 4, "ENFP": 3, "INFJ": 4, "INTP": 2}}, {"txt": "D. 親自站在城牆最前線，用演說激勵士兵，誓死保衛家園。(士氣戰)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 5, "ESTP": 2}}]},

        {"q": "13. 宮廷舞會上，一位神秘的貴族向你搭訕，你覺得他的意圖是？", "opts": [{"txt": "A. 他一定是被我的魅力迷住了！這是開啟戀愛支線的節奏！(自信)", "scores": {"ESFP": 7, "ENFP": 4, "ESFJ": 4, "ISFP": 2}}, {"txt": "B. 他想利用我。這背後一定有政治陰謀，我得小心應對。(警覺)", "scores": {"INTJ": 3, "ISTP": 6, "INTP": 4, "ISTJ": 2}}, {"txt": "C. 他看起來很孤獨。或許他只是想找個懂他的人聊聊。(同理)", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ENFJ": 2}}, {"txt": "D. 管他想幹嘛，先跟他聊聊，套出一些皇室八卦或情報。(情報收集)", "scores": {"ENTP": 3, "ESTP": 6, "ENFJ": 3, "ESFP": 5}}]},

        {"q": "14. 你發現國王其實是魔族偽裝的，但國家現在治理得很好。你會？", "opts": [{"txt": "A. 揭發他！非我族類，其心必異。魔族就是敵人，不能妥協。(正義)", "scores": {"ESTJ": 7, "ISTJ": 7, "ENFJ": 3, "ISFJ": 2}}, {"txt": "B. 保持沈默。只要國家繁榮，統治者是誰並不重要。(實用主義)", "scores": {"INTJ": 4, "INTP": 6, "ISTP": 5, "ENTJ": 3}}, {"txt": "C. 這是個好把柄！私下找他談判，換取巨大的利益或權力。(機會主義)", "scores": {"ENTP": 7, "ESTP": 6, "ENTJ": 4, "ESFP": 2}}, {"txt": "D. 觀察他的本性。如果他是善良的魔族，或許可以打破種族的隔閡？(理想)", "scores": {"INFJ": 7, "INFP": 3, "ISFP": 5, "ENFP": 2}}]},

        {"q": "15. 傳說中的聖女邀請你加入教會，但要你放棄冒險者的自由。你會？", "opts": [{"txt": "A. 答應她。能為神服務是榮耀，而且教會福利好，生活穩定。(安定)", "scores": {"ISFJ": 7, "ESFJ": 7, "ISTJ": 4, "ENFJ": 2}}, {"txt": "B. 果斷拒絕。我生來就是自由的風，沒人能束縛我。(自由)", "scores": {"ISTP": 7, "ISFP": 7, "ESTP": 5, "INFP": 3}}, {"txt": "C. 如果能讓我當上樞機主教，掌握教會權力，我就考慮。(野心)", "scores": {"ENTJ": 3, "INTJ": 2, "ESTJ": 4, "ENTP": 2}}, {"txt": "D. 「能不能兼職？」我想幫忙，但我不想整天待在教堂裡祈禱。(討價還價)", "scores": {"ENFP": 6, "ESFP": 6, "ENTP": 4, "ISFP": 2}}]},

        {"q": "16. 最終Boss竟然是你穿越前的摯友，他邀請你一起統治世界。你會？", "opts": [{"txt": "A. 含淚試圖喚醒他。「這不是你！快想起來我們的約定！」(情感喚醒)", "scores": {"ENFJ": 4, "INFJ": 7, "INFP": 5, "ESFJ": 2}}, {"txt": "B. 拔劍相向。既然你墮落了，我有責任親手結束你的罪惡。(大義滅親)", "scores": {"ESTJ": 6, "ISTJ": 6, "ENTJ": 4, "ISTP": 2}}, {"txt": "C. 「聽起來不錯？」假裝加入，深入了解他的計畫，再看情況背刺或合作。(深謀遠慮)", "scores": {"ENTP": 3, "INTJ": 6, "INTP": 5, "ESTP": 2}}, {"txt": "D. 陷入崩潰，無法戰鬥。為什麼命運要這樣捉弄我們？(內心破碎)", "scores": {"INFP": 4, "ISFP": 7, "ISFJ": 4, "ESFP": 2}}]},

        {"q": "17. 世界即將毀滅，唯一的救世方法是犧牲你的一半靈魂，你會變成沒有感情的空殼。你會？", "opts": [{"txt": "A. 我願意。如果我的犧牲能換來世界的和平，那很划算。(自我犧牲)", "scores": {"ISFJ": 7, "ISTJ": 7, "INFJ": 5, "ESFJ": 3}}, {"txt": "B. 開什麼玩笑！沒有感情還算活著嗎？我寧願用戰鬥賭一把！(抗爭)", "scores": {"ESTP": 7, "ENTJ": 6, "ISTP": 5, "ESFP": 3}}, {"txt": "C. 尋找替代方案。一定有不用犧牲靈魂也能拯救世界的方法。(尋找第三條路)", "scores": {"INTP": 7, "INTJ": 4, "ENTP": 5, "ENFP": 2}}, {"txt": "D. 如果變成空殼，我就無法再愛人了。這比死更可怕。(情感至上)", "scores": {"ISFP": 7, "ENFP": 6, "INFP": 6, "ESFP": 3}}]},

        {"q": "18. 你獲得了「許願聖杯」，但只能許一個願望。你會許？", "opts": [{"txt": "A. 消除世上所有的紛爭與戰亂，建立永恆的和平帝國。(絕對秩序)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. 讓所有人都獲得幸福和吃不完的美食！(普世快樂)", "scores": {"ENFP": 3, "ESFP": 7, "ESFJ": 4, "ISFP": 2}}, {"txt": "C. 我想知道這個宇宙誕生的所有真相與奧秘。(全知全能)", "scores": {"INTP": 7, "ENTP": 6, "INTJ": 5, "ISTP": 2}}, {"txt": "D. 讓一切回到災難發生前，大家都能過著平凡安穩的日子。(守護日常)", "scores": {"ISFJ": 7, "INFJ": 6, "ISTJ": 4, "ISFP": 2}}]},

        {"q": "19. 你的隊友受了詛咒，變成了只會賣萌的小史萊姆，無法變回來。你會？", "opts": [{"txt": "A. 「天啊太可愛了！」把他抱在懷裡蹭，發誓會照顧他一輩子。(溺愛)", "scores": {"ESFP": 7, "ENFP": 7, "ISFP": 5, "ESFJ": 3}}, {"txt": "B. 嘆氣。這下戰力大減了，得重新調整隊伍配置。(現實考量)", "scores": {"ISTJ": 6, "ESTJ": 6, "INTJ": 4, "ISTP": 2}}, {"txt": "C. 戳戳看。好奇他的身體構造，想研究史萊姆的生活習性。(好奇)", "scores": {"INTP": 3, "ENTP": 2, "ISTP": 4, "INTJ": 2}}, {"txt": "D. 雖然很遺憾，但我會保護他，不讓任何魔物欺負他。(責任)", "scores": {"ISFJ": 7, "INFJ": 3, "ENFJ": 4, "INFP": 2}}]},

        {"q": "20. 通往原本世界的傳送門打開了，但一旦回去就再也回不來。你會？", "opts": [{"txt": "A. 回去。那裡有我的家人、朋友和熟悉的網絡，那才是我的家。(現實歸屬)", "scores": {"ISTJ": 7, "ISFJ": 7, "ESTJ": 5, "ESFJ": 3}}, {"txt": "B. 留下。這個充滿魔法與冒險的世界才是我真正屬於的地方！(夢想之地)", "scores": {"ENFP": 7, "ENTP": 2, "ESFP": 5, "ISFP": 3}}, {"txt": "C. 留下。我在這裡已經建立了基業，回去只能當普通人，我不甘心。(權力留戀)", "scores": {"ENTJ": 4, "INTJ": 6, "ESTP": 1, "ISTP": 2}}, {"txt": "D. 在門口猶豫到最後一秒...這是我一生中最艱難的決定。(靈魂拉扯)", "scores": {"INFP": 4, "INFJ": 3, "ISFP": 4, "ENFJ": 2}}]},

        {"q": "21. 你的冒險故事被寫成了書，書名會是？", "opts": [{"txt": "A. 《最強劍神：我如何用一把劍征服異世界》", "scores": {"ESTP": 7, "ISTP": 7, "ENTJ": 4, "ESFP": 2}}, {"txt": "B. 《風與星辰之歌：一個靈魂的流浪手札》", "scores": {"INFP": 4, "INFJ": 4, "ISFP": 5, "ENFP": 2}}, {"txt": "C. 《異世界萬物解析：你所不知道的魔法原理》", "scores": {"INTP": 4, "ENTP": 3, "INTJ": 5, "ISTJ": 2}}, {"txt": "D. 《我們在一起的日子：致我最親愛的夥伴們》", "scores": {"ESFJ": 7, "ISFJ": 7, "ENFJ": 5, "ISFP": 2}}]},

        {"q": "22. 多年後，你成為了傳說中的英雄。你隱居在哪裡？", "opts": [{"txt": "A. 漂浮在空中的法師塔，俯瞰世間，守護著禁忌知識。", "scores": {"INTJ": 7, "ISTJ": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "B. 精靈之森深處的小樹屋，與動物為伍，不問世事。", "scores": {"ISFP": 7, "INFP": 4, "INFJ": 2, "ISTP": 2}}, {"txt": "C. 鬧區的一間小酒館老闆，每天聽著新冒險者的吹牛。", "scores": {"ESFP": 7, "ENFP": 6, "ESTP": 5, "ESFJ": 2}}, {"txt": "D. 我沒有隱居。我還在攝政王的位置上，忙著治理國家呢！", "scores": {"ESTJ": 7, "ENTJ": 7, "ENFJ": 4, "ISTJ": 2}}]},

        {"q": "23. 臨終前，你把自己最強的武器交給了誰？", "opts": [{"txt": "A. 舉辦比武大會，交給最後贏得勝利的最強者。(實力傳承)", "scores": {"ISTP": 7, "ESTP": 7, "ENTJ": 4, "INTJ": 2}}, {"txt": "B. 交給那個雖然弱小，但擁有一顆善良之心的少年。(精神傳承)", "scores": {"ENFJ": 7, "ESFJ": 6, "INFJ": 2, "INFP": 3}}, {"txt": "C. 交給我的孩子或弟子。這是家族的榮耀，不能外流。(血脈傳承)", "scores": {"ISTJ": 7, "ISFJ": 7, "ESTJ": 5, "ESFP": 1}}, {"txt": "D. 隨便扔進湖裡或插在石頭上。等待有緣人自己去發現吧！(命運傳承)", "scores": {"ENTP": 3, "INTP": 6, "ENFP": 5, "ISFP": 2}}]},

        {"q": "24. 如果能帶一樣異世界的東西回地球，你會帶？", "opts": [{"txt": "A. 一顆龍蛋。我要在現代都市裡養龍！太酷了！", "scores": {"ENFP": 7, "ESFP": 7, "ENTP": 5, "ISTP": 2}}, {"txt": "B. 萬靈藥。我想治好地球上親人的病痛。", "scores": {"ISFJ": 7, "INFJ": 4, "ESFJ": 5, "INFP": 2}}, {"txt": "C. 一袋魔法寶石。這價值連城，回去我就財富自由了。", "scores": {"ESTJ": 7, "ENTJ": 3, "ESTP": 5, "INTJ": 2}}, {"txt": "D. 魔法原理書。我要用科學解析魔法，引發地球的科技革命。", "scores": {"INTP": 4, "INTJ": 7, "ENTP": 5, "ISTJ": 1}}]},

        {"q": "25. 最後的問題：你覺得「魔法」的本質是什麼？", "opts": [{"txt": "A. 是「心」的力量。願望越強烈，魔法就越強大。", "scores": {"INFJ": 4, "INFP": 4, "ENFJ": 5, "ISFP": 2}}, {"txt": "B. 是「高維度的科學」。只是我們還沒解析出它的方程式。", "scores": {"INTJ": 7, "INTP": 4, "ENTP": 5, "ISTJ": 2}}, {"txt": "C. 是「力量」。它是用來征服、保護和改變現實的工具。", "scores": {"ENTJ": 4, "ESTP": 6, "ISTP": 5, "ESTJ": 2}}, {"txt": "D. 是「奇蹟」。是讓不可能變為可能的夢想之光。", "scores": {"ENFP": 7, "ESFP": 7, "ESFJ": 4, "ISFJ": 2}}]}

    ],

    "zombie": [

        {"q": "1. 深夜警報大響，窗外火光沖天。你直覺世界變了，第一反應是？", "opts": [{"txt": "A. 立刻鎖門，把浴缸放滿水，清點冰箱食物。做好長期死守的準備。", "scores": {"ISTJ": 7, "ISFJ": 3, "INTJ": 3, "INFJ": 2}}, {"txt": "B. 打給親友下達指令：「待在原地別動！」隨即開始規劃逃生路線。", "scores": {"ENTJ": 5, "ESTJ": 6, "ENFJ": 3, "ISTP": 2}}, {"txt": "C. 腎上腺素飆升！抄起球棒或菜刀，守在門口準備跟衝進來的東西輸贏。", "scores": {"ESTP": 6, "ISTP": 6, "ESFP": 4, "ENTP": 2}}, {"txt": "D. 衝去電腦前刷暗網和論壇，試圖在網路斷線前找出災難的源頭。", "scores": {"INTP": 4, "ENTP": 4, "ENFP": 3, "INTJ": 2}}]},

        {"q": "2. 逃亡路上，一對受傷母女求你載她們，但你的油不夠了。你會？", "opts": [{"txt": "A. 「快上車！」就算死在半路，我也做不到見死不救。", "scores": {"ESFJ": 5, "ENFJ": 5, "ISFJ": 3, "ENFP": 3}}, {"txt": "B. 「抱歉。」理性告訴你載了就是一起死，踩下油門冷酷離開。", "scores": {"ESTJ": 5, "ISTJ": 6, "INTJ": 4, "ENTJ": 3}}, {"txt": "C. 快速談判：「妳們有水或武器嗎？」把這當成一場生存交易。", "scores": {"ENTP": 5, "ESTP": 5, "ENTJ": 3, "ISTP": 2}}, {"txt": "D. 內心天人交戰，最後還是停了車，但恐懼讓你全身發抖，甚至哭著開車。", "scores": {"INFP": 7, "ISFP": 9, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "3. 躲進商場，裡面有四派倖存者，你本能想加入哪一群？", "opts": [{"txt": "A. 在頂樓開烤肉派對的那群。反正世界末日了，不如快樂地活在當下！", "scores": {"ESFP": 8, "ENFP": 7, "ESTP": 4, "ISFP": 3}}, {"txt": "B. 由退伍軍人領導，正在嚴格分配糧食和崗哨的那群。", "scores": {"ISTJ": 6, "ESTJ": 5, "ISFJ": 3, "ENTJ": 2}}, {"txt": "C. 圍在一起禱告、分享故事，互相心靈慰藉的那群。", "scores": {"INFJ": 6, "INFP": 5, "ENFJ": 4, "ISFP": 2}}, {"txt": "D. 在五金區敲敲打打，試圖改裝發電機和無人機的那群怪人。", "scores": {"INTP": 4, "ISTP": 5, "ENTP": 4, "INTJ": 2}}]},

        {"q": "4. 必須撤離了，眼前只有兩樣特殊裝備，你只能帶走一樣：", "opts": [{"txt": "A. 裝滿子彈的衝鋒槍。恐懼源於火力不足。", "scores": {"ESTP": 5, "ISTP": 5, "ENTJ": 3, "ESTJ": 2}}, {"txt": "B. 急救醫療箱。受傷感染比喪屍更絕望，這能救命。", "scores": {"ISFJ": 3, "ESFJ": 4, "INFJ": 3, "ENFJ": 2}}, {"txt": "C. 還能聯網的衛星電話。情報和通訊是無價的。", "scores": {"ENTP": 4, "INTJ": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "D. 一台拍立得和日記本。如果人類滅亡，我要記錄下我們存在的痕跡。", "scores": {"ISFP": 9, "ENFP": 6, "INFP": 5, "INFJ": 3}}]},

        {"q": "5. 獨自守夜時，望著廢墟中的星空，你腦中浮現的是？", "opts": [{"txt": "A. 「這世界雖然殘酷，但此刻的星空卻美得令人心碎。」", "scores": {"INFJ": 10, "INFP": 6, "ISFP": 4, "ENFP": 2}}, {"txt": "B. 「人類文明就像病毒一樣脆弱，這或許是地球的重啟機制。」", "scores": {"INTP": 4, "ENTJ": 5, "INTJ": 4, "ENTP": 2}}, {"txt": "C. 「明天得往北走 30 公里，中午前必須趕到水庫。」", "scores": {"ISTJ": 6, "ESTJ": 6, "ENTJ": 3, "ISTP": 2}}, {"txt": "D. 「不知道爸媽現在還好嗎？希望能再見他們一面。」", "scores": {"ESFJ": 5, "ISFJ": 5, "ENFJ": 4, "ESFP": 2}}]},

        {"q": "6. 隊醫被咬了手，哭著求你們砍斷他的手賭一把。你會？", "opts": [{"txt": "A. 二話不說揮刀砍下。猶豫就是害死他，這是唯一的邏輯。", "scores": {"ENTJ": 5, "ESTJ": 5, "ISTP": 4, "INTJ": 3}}, {"txt": "B. 抱住他，遮住他的眼睛，一邊安撫一邊動手，試圖減少他的恐懼。", "scores": {"ENFJ": 5, "ESFJ": 5, "INFJ": 6, "ISFJ": 2}}, {"txt": "C. 顫抖著退後，把刀子遞給別人。「我做不到...這太殘忍了。」", "scores": {"ISFP": 6, "INFP": 6, "ISFJ": 6, "ESFP": 2}}, {"txt": "D. 「等等！有沒有別的方法？」試圖尋找止血帶或其它可能，不想輕易致殘。", "scores": {"ENTP": 5, "ENFP": 6, "INTP": 3, "ESFP": 2}}]},

        {"q": "7. 發現物資豐富的倉庫，但裡面已有一家人。為了活下去，你會？", "opts": [{"txt": "A. 這是末世，強者生存。武力驅逐他們，佔領這個地方。", "scores": {"ESTP": 6, "ISTP": 6, "ENTJ": 3, "ESTJ": 2}}, {"txt": "B. 「我們有武器，你們有物資，合作才能雙贏。」嘗試談判。", "scores": {"ENFJ": 5, "ENFP": 5, "ESFJ": 3, "INFJ": 2}}, {"txt": "C. 風險太高，悄悄偷走一部分物資就離開，不驚動對方。", "scores": {"ISTJ": 7, "INTJ": 5, "INTP": 3, "ISFJ": 2}}, {"txt": "D. 假裝是政府救援隊，騙取信任混進去，再伺機而動。", "scores": {"ENTP": 6, "INFJ": 5, "ENFJ": 2, "INTJ": 2}}]},

        {"q": "8. 隊伍裡有個只會抱怨還偷吃的累贅，你忍無可忍，你會？", "opts": [{"txt": "A. 當眾揭穿：「下次再犯，我就把你扔出去餵喪屍。」", "scores": {"ESTJ": 6, "ENTJ": 5, "ISTP": 3, "ESTP": 2}}, {"txt": "B. 召集其他人開會，達成共識後，集體對他施壓或驅逐。", "scores": {"INFJ": 5, "ENFJ": 5, "ESFJ": 3, "INTJ": 2}}, {"txt": "C. 這種人還有利用價值。用食物控制他，危險時讓他去當誘餌。", "scores": {"ENTP": 5, "INTJ": 5, "INTP": 4, "ENTJ": 1}}, {"txt": "D. 默默把自己的食物分一點出來補上，不想讓氣氛變得太僵。", "scores": {"ISFJ": 7, "ISFP": 5, "INFP": 4, "ESFJ": 2}}]},

        {"q": "9. 在廢墟找到一台 MP3，你會放什麼歌來聽？", "opts": [{"txt": "A. 重金屬搖滾。讓憤怒和腎上腺素跟著節奏一起爆發！", "scores": {"ESTP": 7, "ESFP": 7, "ENTP": 4, "ISTP": 3}}, {"txt": "B. 戰前的流行老歌。閉上眼，假裝世界還很正常。", "scores": {"ISTJ": 7, "ISFJ": 3, "ESFJ": 3, "ISFP": 2}}, {"txt": "C. 古典樂或純音樂。在廢墟中聽巴哈，有一種荒謬的莊嚴感。", "scores": {"INTJ": 5, "INTP": 5, "INFJ": 4, "ISTJ": 2}}, {"txt": "D. 隨機播放。我不介意下一首是什麼，驚喜才有趣。", "scores": {"ENFP": 6, "ISFP": 6, "ESFP": 4, "ENTP": 2}}]},

        {"q": "10. 地下道遭遇喪屍，不能開槍引爆瓦斯。你會？", "opts": [{"txt": "A. 指揮隊友形成盾牆，用推擠的方式把它們推開。", "scores": {"ESTJ": 5, "ENTJ": 5, "ISTJ": 3, "INTJ": 2}}, {"txt": "B. 拔出開山刀，衝上去近身肉搏。安靜又致命。", "scores": {"ISTP": 7, "ISFP": 5, "ESTP": 4, "ESFP": 2}}, {"txt": "C. 丟出發聲玩具引開它們，趁機溜過去。", "scores": {"ENTP": 4, "ENFP": 5, "INTP": 4, "ESFP": 2}}, {"txt": "D. 「你們快走！」我製造聲響吸引它們注意，為大家爭取時間。", "scores": {"ESFJ": 6, "ISFJ": 6, "ENFJ": 4, "INFP": 2}}]},

        {"q": "11. 基地建立，誰該當領導者？", "opts": [{"txt": "A. 我來。只有我能做出艱難的決定，帶領大家活下去。", "scores": {"ENTJ": 4, "ESTJ": 5, "ENFJ": 2, "INTJ": 2}}, {"txt": "B. 誰最強誰當老大。不服來戰，拳頭硬的說了算。", "scores": {"ISTP": 7, "ESTP": 6, "ENTP": 3, "ESFP": 2}}, {"txt": "C. 投票決定。領袖應該是大家都信任且喜歡的人。", "scores": {"ENFJ": 4, "ESFJ": 6, "ENFP": 4, "INFJ": 2}}, {"txt": "D. 誰當都好，別來管我就行。我只負責做好我自己的事。", "scores": {"INTP": 4, "INFP": 5, "ISFP": 4, "ISTP": 2}}]},

        {"q": "12. 資源分配出現爭議，你提出的方案是？", "opts": [{"txt": "A. 按人頭平均分配。不管強弱，每個人拿到的都一樣。", "scores": {"ISFJ": 5, "ISFP": 5, "ESFJ": 3, "INFP": 2}}, {"txt": "B. 按貢獻分配。殺喪屍多的人吃肉，沒貢獻的人喝湯。", "scores": {"ESTJ": 5, "ENTJ": 5, "ISTP": 4, "INTJ": 2}}, {"txt": "C. 建立內部市場。用勞動換點數，想買什麼自己決定。", "scores": {"ENTP": 4, "ESTP": 5, "INTP": 4, "ENFP": 2}}, {"txt": "D. 按需求分配。生病和懷孕的人優先，強者少吃一點沒關係。", "scores": {"INFJ": 6, "ENFJ": 5, "INFP": 4, "ESFJ": 3}}]},

        {"q": "13. 孩子問：「為什麼還要活下去？」你會回答？", "opts": [{"txt": "A. 「為了彼此。只要我們還在一起，就有活下去的理由。」", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "ENFP": 2}}, {"txt": "B. 「為了還沒吃到的美食、還沒看過的風景。活著就有好事發生！」", "scores": {"ESFP": 7, "ENFP": 7, "ESTP": 4, "ISFP": 2}}, {"txt": "C. 「因為這是責任。我們要活下去，把人類文明延續下去。」", "scores": {"ISTJ": 6, "ESTJ": 5, "ENTJ": 3, "INTJ": 2}}, {"txt": "D. 「或許沒有理由。我們就像薛西弗斯，在荒謬中尋找意義。」", "scores": {"INTJ": 6, "INTP": 6, "INFJ": 4, "ISTP": 2}}]},

        {"q": "14. 基地擴建，你負責什麼工作？", "opts": [{"txt": "A. 整理倉庫、盤點物資、種植蔬菜。確保後勤無憂。", "scores": {"ISTJ": 7, "ISFJ": 3, "ESFJ": 3, "ISFP": 2}}, {"txt": "B. 規劃陷阱區、改良防禦工事、設計逃生路線。", "scores": {"INTP": 5, "ENTP": 5, "INTJ": 3, "INFJ": 1}}, {"txt": "C. 搬磚頭、築圍牆、外出巡邏。我喜歡流汗的感覺。", "scores": {"ISTP": 5, "ESTP": 5, "ISFP": 3, "ESFP": 2}}, {"txt": "D. 當工頭。監督進度，確保每個人都在工作，沒有偷懶。", "scores": {"ESTJ": 5, "ENTJ": 5, "ENFJ": 3, "ISTJ": 1}}]},

        {"q": "15. 慶祝活過一年，大家舉辦晚會。你會？", "opts": [{"txt": "A. 跳上桌子跳舞、帶動氣氛，我要讓每個人都嗨起來！", "scores": {"ESFP": 7, "ENFP": 6, "ESTP": 4, "ESFJ": 2}}, {"txt": "B. 用廢棄物做些裝飾品，或是安靜地在一旁彈吉他。", "scores": {"ISFP": 6, "INFP": 6, "INFJ": 3, "ISFJ": 2}}, {"txt": "C. 忙著分發食物和飲料，確保每個人都有拿到東西吃。", "scores": {"ESFJ": 7, "ENFJ": 5, "ISFJ": 4, "ESTJ": 2}}, {"txt": "D. 坐在角落喝一杯酒，看著大家狂歡，心裡思考著明天的計畫。", "scores": {"INTJ": 5, "ISTP": 5, "INTP": 2, "ENTJ": 2}}]},

        {"q": "16. 你的愛人被感染且隱瞞你，發作前一刻你才發現。你會？", "opts": [{"txt": "A. 崩潰大哭，抱著他直到最後一刻，甚至想跟他一起死。", "scores": {"INFP": 9, "ISFP": 10, "INFJ": 4, "ENFP": 2}}, {"txt": "B. 「為什麼不早說？如果有早點講，說不定還有救！」", "scores": {"INTP": 6, "ENTP": 5, "ISTP": 3, "ESTJ": 2}}, {"txt": "C. 強忍悲傷，拿出槍。「我愛你，所以我不能讓你變成怪物。」砰。", "scores": {"ENTJ": 5, "ESTJ": 5, "INTJ": 4, "ISTP": 4}}, {"txt": "D. 驚慌失措，大喊叫醫生、叫大家來幫忙，無法接受事實。", "scores": {"ESFJ": 7, "ENFJ": 6, "ESFP": 4, "ISFJ": 2}}]},

        {"q": "17. 敵方要求交出科學家換取停戰，你會？", "opts": [{"txt": "A. 絕對不行。科學家是未來的希望，交出他等於放棄未來。", "scores": {"INTJ": 6, "ENTJ": 5, "INTP": 4, "ISTJ": 2}}, {"txt": "B. 絕對不行。我們不出賣夥伴，這是做人的底線。", "scores": {"ENFJ": 6, "INFP": 5, "ESFJ": 4, "ISFP": 2}}, {"txt": "C. 假裝答應，在交易現場設下埋伏，把他們一網打盡。", "scores": {"ESTP": 6, "ENTP": 6, "ISTP": 4, "INTJ": 5}}, {"txt": "D. 猶豫...如果犧牲一個人能救全基地幾百人，這或許是必要的惡。", "scores": {"ISTJ": 7, "ESTJ": 5, "INTP": 3, "ISFJ": 2}}]},

        {"q": "18. 發現高層用活人做實驗，你會？", "opts": [{"txt": "A. 太噁心了！我不管理由是什麼，我要向所有人揭發真相！", "scores": {"ENFP": 6, "INFP": 6, "ESFP": 4, "ENFJ": 2}}, {"txt": "B. 潛入實驗室偷看數據。如果實驗真的有效...或許值得討論？", "scores": {"INTP": 6, "ENTP": 6, "INTJ": 4, "ISTP": 2}}, {"txt": "C. 這是推翻他們的好機會。蒐集證據，發動政變，自己當老大。", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ISTP": 4}}, {"txt": "D. 假裝不知道。我只想活下去，不想捲入這種危險的政治鬥爭。", "scores": {"ISFJ": 4, "ISTJ": 5, "ISFP": 4, "ESFJ": 2}}]},

        {"q": "19. 直升機只能載走 4 個人，基地即將毀滅。你會？", "opts": [{"txt": "A. 衝上去搶位子！人不為己天誅地滅，我要活下去！", "scores": {"ESTP": 6, "ESFP": 6, "ENTJ": 3, "ISTP": 4}}, {"txt": "B. 讓給更有需要的人（小孩、醫生）。我留下來斷後。", "scores": {"INFJ": 8, "ENFJ": 6, "ISFJ": 4, "INFP": 2}}, {"txt": "C. 「誰說只能載 4 個？」把椅子拆了、丟掉重物，試圖塞進更多人。", "scores": {"ENTP": 6, "INTP": 5, "ENFP": 5, "ESTP": 2}}, {"txt": "D. 我不走。這裡是我的家，我要戰鬥到最後一刻。", "scores": {"ISTJ": 6, "ISFJ": 6, "ESTJ": 4, "INTJ": 2}}]},

        {"q": "20. 最後一刻，你拿到了一顆核彈的引爆器。引爆會炸死所有喪屍，但也會炸死你自己。你會？", "opts": [{"txt": "A. 按下按鈕。「為了人類的未來，這一點代價是值得的。」", "scores": {"INTJ": 6, "INFJ": 8, "ENTJ": 4, "INTP": 2}}, {"txt": "B. 猶豫...我看著身邊愛人的臉，我捨不得死，也捨不得他死。", "scores": {"ISFP": 6, "INFP": 6, "ESFP": 6, "ENFP": 1}}, {"txt": "C. 不按。炸了真的有用嗎？搞不好病毒早就變異了。", "scores": {"INTP": 4, "ISTP": 8, "ENTP": 4, "INTJ": 2}}, {"txt": "D. 如果這能保護我的家人不再受苦，我會笑著按下它。", "scores": {"ESFJ": 8, "ISFJ": 6, "ENFJ": 4, "ISFP": 2}}]},

        {"q": "21. 最終，你活下來了。你覺得自己能活下來的最大原因是？", "opts": [{"txt": "A. 因為我夠小心，從不冒險，步步為營。(謹慎)", "scores": {"ISTJ": 6, "ISFJ": 5, "ESTJ": 3, "INTJ": 1}}, {"txt": "B. 因為我適應力強，不管環境多爛，我都能找到樂子。(適應)", "scores": {"ESTP": 5, "ESFP": 8, "ISTP": 3, "ENTP": 1}}, {"txt": "C. 因為我有信念，我相信明天會更好，這股力量支撐著我。(信念)", "scores": {"ENFP": 9, "INFP": 5, "ENFJ": 4, "INFJ": 1}}, {"txt": "D. 因為我用腦子。暴力不能解決問題，智慧才能。(智慧)", "scores": {"ENTJ": 5, "INTP": 3, "INTJ": 4, "ENTP": 2}}]},

        {"q": "22. 戰後世界，你選擇在哪裡定居？", "opts": [{"txt": "A. 重建後的都市。我喜歡熱鬧，喜歡人多的地方。(繁華)", "scores": {"ESFP": 8, "ESTP": 5, "ESFJ": 4, "ENFP": 2}}, {"txt": "B. 森林裡的小木屋。遠離人群，與大自然為伍，療癒創傷。(隱逸)", "scores": {"INFP": 6, "ISFP": 6, "INFJ": 4, "INTP": 2}}, {"txt": "C. 高科技的研究中心。繼續探索科學，預防下一次災難。(進步)", "scores": {"INTJ": 5, "ENTP": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "D. 回到我的故鄉。修復老房子，過著跟以前一樣的平靜生活。(歸根)", "scores": {"ISFJ": 4, "ISTJ": 6, "ESFJ": 4, "ISFP": 2}}]},

        {"q": "23. 新世界的學校邀請你去演講，你會告訴孩子們什麼？", "opts": [{"txt": "A. 「世界是殘酷的，只有變強才不會被淘汰。」(生存法則)", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ESTP": 2}}, {"txt": "B. 「愛與善良是我們與怪物唯一的區別，永遠不要遺失它。」(人性)", "scores": {"ENFJ": 6, "INFP": 5, "INFJ": 4, "ISFP": 2}}, {"txt": "C. 「人生苦短，想做什麼就去做吧，別讓自己後悔！」(自由)", "scores": {"ESFP": 8, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "D. 「記住這段歷史，承擔起重建文明的責任。」(傳承)", "scores": {"ISTJ": 7, "ISFJ": 5, "ESFJ": 4, "INTJ": 1}}]},

        {"q": "24. 你在自己的墓碑上刻了一句話，那是？", "opts": [{"txt": "A. 什麼都不刻，或者只刻一個名字。死後一切皆空。(虛無)", "scores": {"INTP": 6, "ISTP": 6, "INTJ": 4, "ENTP": 2}}, {"txt": "B. 「我先去探路了，你們晚點再來！」(幽默)", "scores": {"ENTP": 5, "ENFP": 9, "ESFP": 6, "ESTP": 2}}, {"txt": "C. 「一位慈愛的父親/母親/朋友，長眠於此。」(關係)", "scores": {"ESFJ": 7, "ISFJ": 3, "ENFJ": 3, "ISFP": 1}}, {"txt": "D. 「他/她重建了這座城市。」(成就)", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ISTJ": 2}}]},

        {"q": "25. 故事結束了。這場喪屍浩劫對你來說，究竟是什麼？", "opts": [{"txt": "A. 一場靈魂的洗禮。它毀了世界，卻讓我找到了真實的自己。(覺醒)", "scores": {"INFJ": 7, "INFP": 6, "ENFJ": 4, "ISFP": 2}}, {"txt": "B. 一場徹頭徹尾的悲劇。我們失去了太多，沒有什麼值得慶祝的。(悲傷)", "scores": {"ISTJ": 6, "ISFJ": 6, "ESTJ": 4, "ESFJ": 2}}, {"txt": "C. 一場瘋狂的冒險。雖然危險，但比以前無聊的日子刺激多了。(刺激)", "scores": {"ESTP": 7, "ESFP": 7, "ENTP": 4, "ISTP": 2}}, {"txt": "D. 一個巨大的實驗。它證明了人類的極限與脆弱。(觀察)", "scores": {"INTP": 6, "INTJ": 6, "ENTJ": 4, "ENTP": 2}}]}

    ],

    "school": [

        {"q": "1. [開學] 走進鬧哄哄的教室，你的第一個直覺動作？", "opts": [{"txt": "A. 熱情地跟每個人打招呼，然後找朋友聊天。", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 走到最後一排靠窗的位子，戴上耳機觀察全班。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. 大聲推開門：「各位！我回來了！」瞬間成為焦點。", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. 低頭快步走到角落，希望不要被老師點名。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},

        {"q": "2. [選幹部] 沒人自願當班長，氣氛尷尬。你會？", "opts": [{"txt": "A. 「既然沒人要當，那就我來吧。」受不了效率低落。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 舉手提名班上最安靜或最搞怪的人，想看好戲。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. 看老師很困擾，勉強舉手。不想讓場面難看。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "D. 絕對不與老師對上眼，心裡默唸「選不到我」。", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}]},

        {"q": "3. [社團] 社團博覽會，你想加入哪裡？", "opts": [{"txt": "A. 熱舞社或籃球隊。在舞台上發光發熱！", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. 科研社或程式設計。學技術，不用太多社交。", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "C. 學生會或辯論社。參與決策，掌握資源。", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. 文學社或志工社。安靜地創作或幫助他人。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "4. [作業] 死黨忘記寫作業求你借他抄。你會？", "opts": [{"txt": "A. 「我們一起去圖書館趕工吧！我教你寫。」", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 「不行。抄襲是害了你，你自己寫。」", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 裝傻到底。「我不知道，我當時在看書。」", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. 「拿去吧，但要把字跡改一下喔。」", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},

        {"q": "5. [放學] 夕陽西下，這段時間你通常在做什麼？", "opts": [{"txt": "A. 一個人騎著單車閒晃，或是躲在祕密基地發呆。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. 揪團去唱 KTV、逛街，玩到天黑才回家。", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 去補習班或圖書館。現在努力是為了未來。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 留在學校幫忙社團善後，或聽朋友訴苦。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "6. [考試] 期末考大魔王來襲，你的策略是？", "opts": [{"txt": "A. 一個月前就擬定計畫表，按部就班地複習。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "B. 前一天熬夜喝紅牛，靠短期記憶力爆發。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. 分析出題邏輯，只讀會考的重點，追求CP值。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. 組織讀書會，分配大家負責的章節，互相教學。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}]},

        {"q": "7. [比賽] 籃球賽落後一分，剩 10 秒。你會？", "opts": [{"txt": "A. 「球給我！」不管三七二十一，強行切入得分。", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. 喊暫停！畫出戰術，指揮隊友跑位。", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. 大聲為隊友加油，相信默契，輸了也要精彩。", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "D. 默默跑到沒人注意的角落，等待關鍵傳球。", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},

        {"q": "8. [作弊] 好友作弊被抓，老師問你有沒有看到。你會？", "opts": [{"txt": "A. 裝傻到底。「我不知道，我在看書。」不出賣朋友。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "B. 誠實回答。作弊就是不對，包庇是害了他。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 「老師，作弊的定義是什麼？」試圖把場面搞混。", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "D. 私下找老師求情，希望給他改過機會。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "9. [園遊會] 班上要擺攤，你提議做什麼？", "opts": [{"txt": "A. 恐怖鬼屋！我們可以扮鬼嚇人，這絕對最好玩！", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "B. 低成本高利潤的小吃攤。目標是營業額第一！", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. 文青咖啡廳。佈置得很漂亮，播放舒服的音樂。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. 義賣二手市集。把賺到的錢捐給流浪動物之家。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "10. [怪談] 傳說舊校舍晚上有怪聲。你會？", "opts": [{"txt": "A. 「太酷了！」今晚就揪團去夜遊探險，還要開直播！", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "B. 無聊的怪談。那是違反校規的，回家睡覺。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. 帶著儀器去測量。我想知道怪聲的物理成因。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. 有點害怕，但又覺得那裡可能有悲傷的故事...遠遠祈禱。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "11. [心動] 隔壁班的校草/校花似乎在看你，你的反應？", "opts": [{"txt": "A. 「天啊！戀愛預感！連孩子的名字都想好了！」", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. 「他可能是在看我後面的時鐘。」繼續做自己的事。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 臉紅心跳，假裝沒看到趕快低頭，心裡小鹿亂撞。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. 微笑回應對方的視線，展現友善的一面。", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},

        {"q": "12. [告白] 你要告白了，會選擇什麼方式？", "opts": [{"txt": "A. 寫一封文情並茂的手寫信，偷偷塞在他的抽屜裡。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. 在全校面前大聲告白！讓全世界知道我愛他。", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "C. 直接約出來講清楚。「我喜歡你，要不要在一起？」", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. 精心策劃一場完美的約會，在氣氛最好時說出口。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "13. [失戀] 好友失戀哭得很慘，你怎麼安慰？", "opts": [{"txt": "A. 抱著他一起哭，罵那個渣男/渣女，陪他聊通宵。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. 「別哭了！走，帶你去吃好吃的，再去唱KTV發洩！」", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 冷靜分析這段感情失敗的原因，告訴他下一個會更好。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 什麼都不說，只是靜靜地陪在他身邊，遞給他衛生紙。", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},

        {"q": "14. [謠言] 學校流傳關於你的不實謠言，你會？", "opts": [{"txt": "A. 正面迎擊！找出散布謠言的人，要求他公開道歉。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 覺得很受傷，躲起來不想見人，希望謠言自己消失。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 把謠言編成笑話自嘲，甚至加油添醋讓它更荒謬。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. 相信朋友會懂我。只要我在乎的人相信我就好。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "15. [畢旅] 畢業旅行分房，你最在意的是？", "opts": [{"txt": "A. 大家都能跟好朋友分在一起，沒有人落單被排擠。", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 我要跟最瘋的那群人一組，晚上打枕頭戰、玩通宵！", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. 室友不要打呼磨牙，作息要正常，我想好好睡覺。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. 跟誰都可以，只要給我一個角落讓我安靜滑手機。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},

        {"q": "16. [冤枉] 老師冤枉全班吵鬧要罰站，你會？", "opts": [{"txt": "A. 舉手抗議：「老師，這不公平！為什麼沒吵的人也要受罰？」", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 嘆口氣，乖乖站好。反抗也沒用，趕快罰完趕快回家。", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. 代表全班去跟老師溝通，試圖達成一個雙方都能接受的妥協。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}, {"txt": "D. 趁老師轉身寫黑板的時候，從後門溜之大吉。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},

        {"q": "17. [經費] 社團經費被砍，面臨倒社，你會？", "opts": [{"txt": "A. 整理出年度成果報告，直接找校長談判，據理力爭。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. 發起校園募款！舉辦義賣或表演，靠自己賺回來。", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. 研究法規漏洞，掛名在其他社團下生存。", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. 沒錢就沒錢吧。只要大家心在一起，哪裡都能練習。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "18. [筆記] 對手偷走你的比賽筆記，你會？", "opts": [{"txt": "A. 沒關係。我的實力在腦子裡，偷走筆記也偷不走冠軍。", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. 雖然很難過，但不想把事情鬧大，只好熬夜重做。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 以牙還牙！我也去偷他的，或者在他的鞋子裡放圖釘。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. 相信他有苦衷，甚至主動問他是不是需要幫忙。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "19. [話劇] 全班演話劇，你想擔任什麼角色？", "opts": [{"txt": "A. 導演或主角。我要帶領大家完成這齣大戲！", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 編劇或道具組。躲在幕後發揮創意，不想上台。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "C. 搞笑的配角。只要能逗大家笑，戲份多少不重要。", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. 音控或燈光。這需要精準技術，且不用跟人講話。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}]},

        {"q": "20. [膠囊] 畢業埋時光膠囊，你放什麼？", "opts": [{"txt": "A. 寫給未來自己的一封信，寫滿夢想與期許。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. 全班的大合照與簽名制服。這是友誼的證明。", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "C. 對十年後科技或股價的預測。想驗證自己準不準。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 我現在最喜歡的遊戲機或限量球鞋。以後會增值！", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}]},

        {"q": "21. [畢業] 典禮當天，你的真實感受？", "opts": [{"txt": "A. 哭成淚人兒。真的捨不得大家，希望時間能停在這一刻。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. 「終於解脫了！」迫不及待迎接自由的大學生活。", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. 平靜。這只是人生的一個階段，我已經準備好面對下一關。", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "D. 看著校園的角落，心中充滿了酸酸甜甜的詩意感觸。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},

        {"q": "22. [同學會] 多年後，你希望大家怎麼記得你？", "opts": [{"txt": "A. 班上的核心人物，那個總是帶給大家溫暖的人。", "scores": {"ISFJ": 7, "ESFJ": 6, "ENFJ": 4, "INFJ": 2}}, {"txt": "B. 最成功的人。事業有成、意氣風發的樣子。", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. 一個獨特的人。雖然話不多，但很有才華。", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. 只要想到我，大家就會忍不住笑出來的開心果。", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]},

        {"q": "23. [回到過去] 對高一入學的自己說什麼？", "opts": [{"txt": "A. 「多讀點書，少做白日夢，投資自己才是真的。」", "scores": {"ISTJ": 7, "INTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. 「勇敢一點！去告白、去翹課、去瘋狂，別留遺憾！」", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 「不要那麼在意別人的眼光，你已經很好了。」", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. 「珍惜身邊的朋友，他們是你最寶貴的財富。」", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "24. [青春] 「青春」這兩個字代表什麼？", "opts": [{"txt": "A. 是汗水與衝動。是跌倒了再爬起來的痛快。", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 是一場還沒醒的夢。充滿了粉紅泡泡和藍色憂鬱。", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 是成長的必經之路。累積知識與經驗的過程。", "scores": {"INTJ": 7, "ISTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. 是與夥伴們一起奮鬥、一起流淚的美好時光。", "scores": {"ENFJ": 7, "INFJ": 6, "ISFJ": 4, "ESFJ": 2}}]},

        {"q": "25. [最後一課] 學校裡學到最重要的一課？", "opts": [{"txt": "A. 社會是現實的，實力才是硬道理。", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 朋友是一輩子的資產，懂得待人處事最重要。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. 保持獨立思考，不要盲從權威或隨波逐流。", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. 永遠保持好奇心，勇敢追逐不切實際的夢想。", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]}

    ],

    "cyber": [

        {"q": "1. [連線] 在膠囊旅館醒來，大腦連上網路，你的第一個直覺動作？", "opts": [{"txt": "A. 查看社群訊息，確認家人朋友的位置，發送早安訊號。", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 啟動義眼掃描，分析今日空氣毒素指數與新聞，規劃最佳路徑。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. 穿上最閃亮的發光夾克，騎上重機炸街，享受路人的目光。", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. 拉上遮光廉，開啟「勿擾模式」，不想面對這個喧囂的電子世界。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},

        {"q": "2. [衝突] 街頭幫派在火拼，沒人敢過去，氣氛緊張。你會？", "opts": [{"txt": "A. 「這群烏合之眾...」站出來指揮現場秩序，建立臨時安全區。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 駭入路邊的廣告看板改成搞笑迷因圖，試圖讓氣氛瞬間破功。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. 雖然害怕，但還是默默把受傷的路人拉到掩體後方急救。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "D. 啟動光學迷彩隱身，貼著牆邊溜走，心裡默唸「別看到我」。", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}]},

        {"q": "3. [改裝] 地下診所提供免費的身體改造體驗，你會選擇？", "opts": [{"txt": "A. 炫彩皮膚與聲光模組。我要成為夜城最閃耀的賽博龐克明星！", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. 大腦協處理器。提升運算速度，能瞬間破解防火牆與學習知識。", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "C. 戰術指揮植入物。能同時操控多台無人機，掌握戰場全局。", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. 情感共鳴晶片。能直接讀取他人的情緒波動，理解人心的深處。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "4. [委託] 駭客朋友盜取了公司的機密數據，請求你幫忙藏匿。你會？", "opts": [{"txt": "A. 「交給我吧！我們一起把這份數據公開，揭發公司的惡行！」", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 「不行。這是盜竊行為，而且會惹上殺身之禍，我不能收。」", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 裝作不知道裡面是什麼。「你放在那邊就好，我什麼都沒看到。」", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. 「你這樣太危險了...」一邊唸他，一邊還是幫他找了個安全的地方。", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},

        {"q": "5. [休息] 在充滿酸雨的夜晚，這段時間你通常在做什麼？", "opts": [{"txt": "A. 躲在狹窄的伺服器機房裡，聽著雨聲和機器運轉聲，享受孤獨。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. 去地下舞廳狂歡，嗑點電子迷幻藥，讓意識與數據流同步。", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 下載新的技能晶片，學習戰鬥或駭客技術。力量就是一切。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 在貧民窟分發合成食物，或是聽流浪的改造人訴說過去。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "6. [任務] 接到一個難度極高的潛入任務，你的策略是？", "opts": [{"txt": "A. 花一個月監控守衛路線，制定完美的時刻表，分秒不差地執行。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "B. 隨機應變！製造一場大爆炸當掩護，趁亂衝進去，賭運氣。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. 寫一個病毒程式，從後門駭入系統，癱瘓所有監視器和防禦網。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. 組織一支專業團隊，分配每個人負責的區域，互相掩護。", "scores": {"ENTJ": 7, "ESTJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "7. [戰鬥] 遭遇戰鬥機器人，你的武器卡彈了，剩最後 10 秒。你會？", "opts": [{"txt": "A. 「看我的！」扔掉槍，拔出高頻振動刀，華麗地衝上去近身肉搏。", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. 迅速下令隊友進行掩護射擊，自己利用地形進行戰術撤退。", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. 大聲激勵隊友：「不要怕！集中火力攻擊它的關節！」穩住士氣。", "scores": {"ENFJ": 7, "ENFP": 6, "ESFJ": 4, "ISFP": 2}}, {"txt": "D. 冷靜觀察機器人的動作模式，尋找裝甲縫隙中的緊急停止按鈕。", "scores": {"INFJ": 7, "INTP": 6, "ISFJ": 4, "ISTP": 2}}]},

        {"q": "8. [違法] 發現搭檔偷偷販賣公司機密數據，被你撞見。你會？", "opts": [{"txt": "A. 裝作沒看見。「這世道大家都不容易。」選擇沉默保護他。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "B. 「你這是違反契約。」當面制止他，如果不聽就向上級匯報。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 「分我一半，我就當作沒看到。」或者幫他想個更好的銷贓管道。", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "D. 私下勸他收手，這太危險了，我不希望看到你出事。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},

        {"q": "9. [市集] 要在黑市擺攤賺錢，你打算賣什麼？", "opts": [{"txt": "A. 販賣最新的「夢境體驗晶片」，讓大家體驗虛擬的刺激快感！", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "B. 高效能的破解軟體或情報販賣。這是剛需，利潤最高。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. 手工製作的復古工藝品。在這個冰冷的科技世界，販賣「溫度」。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. 開一間會傾聽煩惱的義體維修店，把賺到的錢捐給孤兒院。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "10. [傳說] 聽說貧民窟深處有一個會吃人的 AI 鬼屋。你會？", "opts": [{"txt": "A. 「太酷了！」帶上裝備去探險，看能不能抓到那個 AI 賣錢。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "B. 那是危險區域，既然政府封鎖了就別去，安全第一。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. 遠端駭入該區域的監視器。我想分析這個 AI 的代碼結構。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. 覺得那個 AI 可能擁有悲傷的靈魂...但為了安全還是勸大家別去。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "11. [心動] 在酒吧遇到一個氣質獨特的生化人，你的反應？", "opts": [{"txt": "A. 「天啊！這是命運的邂逅！我們的型號一定很匹配！」", "scores": {"ENFP": 7, "ESFP": 6, "INFP": 4, "ESFJ": 2}}, {"txt": "B. 「他可能是在掃描我身上的植入物價值。」保持警戒。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. 假裝在看全息菜單，其實心跳加速，偷偷用餘光瞄他。", "scores": {"INFP": 7, "INFJ": 6, "ISFP": 4, "ISFJ": 2}}, {"txt": "D. 直接走過去請他喝一杯：「你的義眼型號很特別，哪裡改的？」", "scores": {"ESTP": 7, "ENTP": 6, "ENTJ": 4, "ESFP": 2}}]},

        {"q": "12. [告白] 決定向心儀的駭客告白，你會用什麼方式？", "opts": [{"txt": "A. 寫一段加密的詩歌代碼，只有他能解開看到裡面的情書。", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ISFP": 2}}, {"txt": "B. 駭入全城的廣告看板，把他的名字和我的愛意投射在夜空中！", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "C. 直接約出來講清楚。「我喜歡妳的技術，我們要不要結盟(交往)？」", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. 在虛擬實境(VR)中建造一個完美的世界，在那裡向他表白。", "scores": {"ESFJ": 7, "ENFJ": 6, "ESFP": 4, "ENFP": 2}}]},

        {"q": "13. [失戀] 朋友被網戀對象騙了錢和感情，你怎麼安慰？", "opts": [{"txt": "A. 陪他一起大罵那個騙子，給他大大的擁抱，陪他喝到天亮。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. 「別難過！走，我們去賭場贏回來，再去換個更帥的義體！」", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 追蹤騙子的 IP 位置。「別哭，我已經找到他在哪了，我們去討債。」", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 什麼都不說，只是靜靜地陪他看著雨中的霓虹燈，遞給他毛巾。", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},

        {"q": "14. [謠言] 網路上流傳你是企業走狗的不實謠言，你會？", "opts": [{"txt": "A. 正面迎擊！公開我的交易紀錄，並懸賞找出造謠的人。", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 覺得很煩，暫時登出網路，躲回現實世界，不想理會。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 轉發謠言並嘲笑它：「企業走狗？他們付得起我的價碼嗎？哈哈！」", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. 相信我的夥伴會懂我。只要我在乎的人相信我就好。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "15. [組隊] 要組隊去荒坂塔偷數據，你最在意隊友的是？", "opts": [{"txt": "A. 大家都要好相處，互相信任，絕對不能有背叛者。", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 我要跟最瘋狂的那群人一組，這場搶劫一定要夠刺激、夠華麗！", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. 隊友不要太多廢話，專業、精準、安靜地完成任務。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. 跟誰都可以，只要給我一個角落讓我安靜做我的事。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},

        {"q": "16. [冤枉] 警察無差別掃描並逮捕路人，你也在其中。你會？", "opts": [{"txt": "A. 大聲抗議：「這是濫用職權！我有律師，我要直播你們的暴行！」", "scores": {"ENFP": 7, "ENTP": 6, "ENFJ": 4, "ESFP": 2}}, {"txt": "B. 保持冷靜，配合檢查。現在反抗不划算，出來後再算帳。", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. 試圖跟警官溝通，安撫周圍群眾的情緒，避免衝突升級。", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}, {"txt": "D. 趁警察不注意，啟動干擾器，從後巷溜之大吉。", "scores": {"ISTP": 7, "INTP": 6, "ESFP": 3, "ENTP": 2}}]},

        {"q": "17. [經費] 反抗軍基地資金短缺，即將解散。你會？", "opts": [{"txt": "A. 找金主談判。說服地下大亨投資我們，展示未來的回報。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. 劫富濟貧！發起一場針對企業的快閃搶劫，炒熱氣氛順便賺錢。", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. 寫程式挖礦，或者駭入銀行的休眠帳戶轉移資金。", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. 沒錢就轉入地下化吧。只要大家團結，哪裡都是基地。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},

        {"q": "18. [偷竊] 對手偷走了你研發的病毒代碼並註冊專利。你會？", "opts": [{"txt": "A. 沒關係。那只是舊版本，我腦中已經有更完美的 2.0 版了。", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. 雖然很氣憤，但不想惹上大企業的法務部，只好吞下去。", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 以牙還牙！駭入他的神經網絡，讓他當眾出醜。", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. 相信他有苦衷，甚至私下問他是不是缺錢才這麼做。", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},

        {"q": "19. [計畫] 團隊要執行「推翻企業」的終極計畫，你想擔任？", "opts": [{"txt": "A. 總指揮或精神領袖。我要發表演說，喚醒市民的覺醒！", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. 宣傳設計。製作反抗軍的標誌與塗鴉，傳遞自由的訊息。", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "C. 誘餌。我在前線製造混亂吸引火力，讓主力部隊潛入。", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. 系統監控。我在後台切斷警報、解鎖大門，確保行動順利。", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}]},

        {"q": "20. [備份] 在大腦被格式化之前，你只能備份一段記憶。你會選？", "opts": [{"txt": "A. 小時候第一次看到真正星空的感動。那是我的初心。", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. 與戰友們在天台喝酒慶祝的畫面。那是友情的證明。", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "C. 我畢生研究的技術核心代碼。知識必須傳承下去。", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. 我銀行帳戶的密碼。沒有錢，復活了也沒法活！", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}]},

        {"q": "21. [結局] 企業倒台了，舊時代結束。你的真實感受？", "opts": [{"txt": "A. 有點感傷。雖然舊時代很糟，但那裡也有我們熟悉的一切。", "scores": {"ESFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFP": 2}}, {"txt": "B. 「終於解脫了！」這爛透的世界終於毀了，我要自由！", "scores": {"ISTP": 7, "INTP": 6, "ESTP": 4, "ENTP": 2}}, {"txt": "C. 平靜。破壞容易建設難，現在才是真正挑戰的開始。", "scores": {"ENTJ": 7, "INTJ": 6, "ESTJ": 4, "ISTJ": 2}}, {"txt": "D. 看著城市的廢墟長出新芽，心中充滿了酸酸甜甜的詩意。", "scores": {"INFP": 7, "INFJ": 6, "ISFP": 4, "ENFP": 2}}]},

        {"q": "22. [傳說] 多年後，你希望夜城的人怎麼記得你？", "opts": [{"txt": "A. 地下城的守護者。那個在黑暗中給予大家溫暖與食物的人。", "scores": {"ISFJ": 7, "ESFJ": 6, "ENFJ": 4, "INFJ": 2}}, {"txt": "B. 新秩序的締造者。重建了這座城市，讓它恢復運作的人。", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. 一個都市傳說。沒人見過我的真面目，但我無所不在。", "scores": {"INTP": 7, "ISFP": 6, "INFJ": 4, "ISTP": 2}}, {"txt": "D. 只要提到我，大家就會想起那段最瘋狂、最快樂的時光。", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]},

        {"q": "23. [回到過去] 對剛來到夜城的自己說什麼？", "opts": [{"txt": "A. 「不要相信任何人，合約看仔細，投資自己才是真的。」", "scores": {"ISTJ": 7, "INTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. 「大膽一點！去改裝、去相愛、去燃燒，別活得像個機器！」", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. 「在這個失去靈魂的城市裡，不要弄丟了你的心。」", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ISTJ": 2}}, {"txt": "D. 「記住這個數據漏洞，還有那家公司的股價會崩盤！」", "scores": {"ENTP": 7, "ISTP": 6, "INTP": 4, "ESTP": 2}}]},

        {"q": "24. [定義] 你覺得「Cyberpunk」代表什麼？", "opts": [{"txt": "A. 是金屬與血肉的碰撞。是活在刀口上的刺激。", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 是霓虹燈下的孤獨。充滿了科技的絢爛與人性的哀愁。", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. 是混亂中的生存。在失序的世界尋找一絲穩定的過程。", "scores": {"INTJ": 7, "ISTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. 是進化的試錯。人類試圖超越肉體極限的實驗場。", "scores": {"ENFJ": 7, "INFJ": 6, "ISFJ": 4, "ESFJ": 2}}]},

        {"q": "25. [最後一課] 賽博世界裡學到最重要的一課？", "opts": [{"txt": "A. 科技再發達，弱肉強食的本質永遠不會變。", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. 義體可以替換，但真心的夥伴是無法複製的。", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. 保持獨立的意識，不要被網路輿論或企業宣傳洗腦。", "scores": {"INTP": 7, "ENTP": 6, "ISTP": 4, "INTJ": 2}}, {"txt": "D. 即使身體是機械的，只要靈魂是自由的，我就活著。", "scores": {"ISFP": 7, "INFP": 6, "INFJ": 4, "ENFP": 2}}]}

    ]

}
# ==========================================
# 4.7 英文版劇本題庫 (完整翻譯，權重與中文版一致)
# ==========================================
ALL_QUIZZES_EN = {
    "fantasy": [
        {"q": "1. You open your eyes in a magical world. First instinct?", "opts": [{"txt": "A. Check belongings, find water/shelter. (Survival)", "scores": {"ISTJ": 3, "ISFJ": 2, "INTJ": 3, "ISTP": 2}}, {"txt": "B. Analyze environment physics/magic. (Curiosity)", "scores": {"INTP": 3, "ENTP": 6, "ENFP": 4, "INTJ": 2}}, {"txt": "C. Shout and run to nearest town! (Action)", "scores": {"ESTP": 6, "ESFP": 6, "ENFP": 3, "ISTP": 2}}, {"txt": "D. Assess situation, find power center. (Strategy)", "scores": {"ENTJ": 6, "ESTJ": 2, "ENFJ": 6, "INTJ": 2}}]},
        {"q": "2. Choose a legendary weapon:", "opts": [{"txt": "A. [Excalibur] Power and Command. (Leader)", "scores": {"ENTJ": 6, "ESTJ": 2, "ENFJ": 4, "ISTJ": 2}}, {"txt": "B. [World Tree Staff] Healing and Nature. (Magic)", "scores": {"INFP": 7, "INFJ": 3, "ISFP": 5, "ENFP": 2}}, {"txt": "C. [Shadow Daggers] Deadly and Fast. (Assassin)", "scores": {"ISTP": 7, "ESTP": 6, "ISFP": 4, "ENTP": 2}}, {"txt": "D. [Aegis Shield] Protection. (Guardian)", "scores": {"ISFJ": 4, "ESFJ": 6, "ISTJ": 4, "ENFJ": 5}}]},
        {"q": "3. Guild Quest Selection:", "opts": [{"txt": "A. Slay Dragon! High fame/reward. (Fame)", "scores": {"ESTP": 7, "ESFP": 7, "ENTJ": 4, "ENTP": 2}}, {"txt": "B. Explore Ruins. Ancient truths. (Truth)", "scores": {"INTP": 7, "INTJ": 3, "INFJ": 4, "ENTP": 3}}, {"txt": "C. Escort/Help Villagers. Kindness. (Help)", "scores": {"ISFJ": 3, "ESFJ": 6, "ENFJ": 7, "INFP": 2}}, {"txt": "D. Gather Herbs. Solitude. (Freedom)", "scores": {"ISFP": 7, "ISTP": 6, "INFP": 4, "ISTJ": 1}}]},
        {"q": "4. Encounter injured beast cub. You?", "opts": [{"txt": "A. Tame it. Powerful ally. (Utilize)", "scores": {"ENTJ": 3, "INTJ": 2, "ESTJ": 4, "ISTP": 2}}, {"txt": "B. Heal and communicate. (Empathy)", "scores": {"INFP": 7, "ISFP": 7, "INFJ": 5, "ENFP": 3}}, {"txt": "C. Kill/Drive away. Dangerous. (Risk)", "scores": {"ISTJ": 3, "ESTJ": 2, "ISTP": 4, "INTJ": 2}}, {"txt": "D. Keep as cute pet! (Love)", "scores": {"ENFP": 6, "ESFP": 6, "ESFJ": 4, "ISFP": 2}}]},
        {"q": "5. Cursed village asks help for a price. You?", "opts": [{"txt": "A. Help immediately. Hero's duty. (Duty)", "scores": {"ENFJ": 7, "ESFJ": 6, "INFJ": 4, "ISFJ": 3}}, {"txt": "B. Study curse loophole. (Logic)", "scores": {"ENTP": 7, "INTP": 3, "INTJ": 4, "ISTP": 2}}, {"txt": "C. Negotiate reward first. (Contract)", "scores": {"ESTJ": 4, "ISTJ": 2, "ENTJ": 6, "INTJ": 2}}, {"txt": "D. Trust bad feeling, leave. (Instinct)", "scores": {"ISFP": 5, "INFP": 4, "ISTP": 3, "INFJ": 2}}]},
        {"q": "6. Teammates arguing tactics. You?", "opts": [{"txt": "A. 'Shut up! Listen to me!' (Command)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 1, "ISTP": 1}}, {"txt": "B. Mediate and find compromise. (Peace)", "scores": {"ESFJ": 7, "ENFJ": 7, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. Analyze data success rates. (Data)", "scores": {"INTP": 3, "ENTP": 5, "INTJ": 4, "ISTP": 2}}, {"txt": "D. Stay out of it. (Avoid)", "scores": {"ISFP": 3, "INFP": 5, "ISTP": 4, "INTJ": 1}}]},
        {"q": "7. Found Forbidden Dark Magic book. You?", "opts": [{"txt": "A. Learn it. Power is neutral. (Power)", "scores": {"INTJ": 4, "ENTJ": 6, "ENTP": 4, "ISTP": 2}}, {"txt": "B. Destroy it. Dangerous. (Order)", "scores": {"ISTJ": 4, "ISFJ": 3, "ESTJ": 5, "ENFJ": 2}}, {"txt": "C. Study secretly. Knowledge. (Curiosity)", "scores": {"INTP": 7, "ENTP": 6, "INFJ": 3, "INTJ": 2}}, {"txt": "D. Avoid it. Ominous. (Feeling)", "scores": {"INFP": 6, "ENFP": 5, "ISFP": 4, "ESFJ": 2}}]},
        {"q": "8. Dungeon path choice?", "opts": [{"txt": "A. Shortest, high risk. (Efficiency)", "scores": {"ENTJ": 3, "ESTP": 6, "ESFP": 4, "ISTP": 2}}, {"txt": "B. Safe, mapped path. (Safety)", "scores": {"ISTJ": 3, "ISFJ": 3, "ESTJ": 4, "INTJ": 2}}, {"txt": "C. Mysterious glowing path. (Adventure)", "scores": {"ENFP": 7, "ENTP": 6, "INTP": 4, "ESFP": 2}}, {"txt": "D. Follow mana instinct. (Intuition)", "scores": {"INFJ": 7, "INTJ": 2, "INFP": 5, "ISFP": 3}}]},
        {"q": "9. Need money. You propose?", "opts": [{"txt": "A. Arena Tournament! (Fight)", "scores": {"ESTP": 7, "ESFP": 7, "ISTP": 4, "ENTJ": 2}}, {"txt": "B. Stable jobs. (Work)", "scores": {"ISTJ": 4, "ESTJ": 6, "ISFJ": 2, "INTJ": 1}}, {"txt": "C. Street performance/Scams. (Trick)", "scores": {"ENTP": 7, "ENFP": 3, "ESFP": 5, "INTP": 2}}, {"txt": "D. Gather materials. (Craft)", "scores": {"ISFP": 4, "INFP": 6, "ISTP": 4, "ISFJ": 2}}]},
        {"q": "10. Unsolvable riddle from Boss. You?", "opts": [{"txt": "A. Analyze logic paradox. (Brain)", "scores": {"INTP": 7, "INTJ": 4, "ENTP": 5, "ISTP": 1}}, {"txt": "B. Talk to him, empathize. (Heart)", "scores": {"INFJ": 7, "ENFJ": 6, "INFP": 5, "ENFP": 2}}, {"txt": "C. Attack while he talks! (Force)", "scores": {"ISTP": 7, "ESTP": 7, "ESFP": 4, "ENTJ": 2}}, {"txt": "D. Admit ignorance honestly. (Honest)", "scores": {"ISFJ": 3, "ESFJ": 6, "ISTJ": 4, "INFP": 2}}]},
        {"q": "11. Governing your territory:", "opts": [{"txt": "A. Strict laws, strong army. (Military)", "scores": {"ESTJ": 7, "ENTJ": 7, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Welfare, schools, hospitals. (Care)", "scores": {"ESFJ": 7, "ENFJ": 7, "ISFJ": 2, "INFP": 2}}, {"txt": "C. Tech and Magic city. (Future)", "scores": {"ENTP": 7, "INTP": 7, "INTJ": 4, "ISTP": 2}}, {"txt": "D. Nature village. (Peace)", "scores": {"INFP": 7, "ISFP": 7, "INFJ": 4, "ENFP": 2}}]},
        {"q": "12. Enemy invasion tactic:", "opts": [{"txt": "A. Decapitation strike on leader. (Speed)", "scores": {"ENTJ": 4, "INTJ": 4, "ESTP": 4, "ISTP": 2}}, {"txt": "B. Fortify and defend. (Defense)", "scores": {"ISTJ": 7, "ESTJ": 6, "ISFJ": 5, "INTJ": 2}}, {"txt": "C. Chaos and Psy-ops. (Chaos)", "scores": {"ENTP": 4, "ENFP": 3, "INFJ": 4, "INTP": 2}}, {"txt": "D. Frontline morale boost. (Inspire)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 5, "ESTP": 2}}]},
        {"q": "13. Noble approaches you at ball. Intent?", "opts": [{"txt": "A. Romance! Charmed by me. (Love)", "scores": {"ESFP": 7, "ENFP": 4, "ESFJ": 4, "ISFP": 2}}, {"txt": "B. Political scheme. (Suspicion)", "scores": {"INTJ": 3, "ISTP": 6, "INTP": 4, "ISTJ": 2}}, {"txt": "C. Lonely soul. (Empathy)", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ENFJ": 2}}, {"txt": "D. Intel gathering. (Info)", "scores": {"ENTP": 3, "ESTP": 6, "ENFJ": 3, "ESFP": 5}}]},
        {"q": "14. King is a Demon, but good ruler. You?", "opts": [{"txt": "A. Expose him! Justice. (Principle)", "scores": {"ESTJ": 7, "ISTJ": 7, "ENFJ": 3, "ISFJ": 2}}, {"txt": "B. Silence. Prosperity matters. (Pragmatic)", "scores": {"INTJ": 4, "INTP": 6, "ISTP": 5, "ENTJ": 3}}, {"txt": "C. Blackmail for power. (Benefit)", "scores": {"ENTP": 7, "ESTP": 6, "ENTJ": 4, "ESFP": 2}}, {"txt": "D. Observe. Coexistence? (Ideal)", "scores": {"INFJ": 7, "INFP": 3, "ISFP": 5, "ENFP": 2}}]},
        {"q": "15. Join Church (lose freedom)?", "opts": [{"txt": "A. Yes. Honor and stability. (Order)", "scores": {"ISFJ": 7, "ESFJ": 7, "ISTJ": 4, "ENFJ": 2}}, {"txt": "B. No. Freedom first. (Free)", "scores": {"ISTP": 7, "ISFP": 7, "ESTP": 5, "INFP": 3}}, {"txt": "C. Only if I get power. (Ambition)", "scores": {"ENTJ": 3, "INTJ": 2, "ESTJ": 4, "ENTP": 2}}, {"txt": "D. Negotiate part-time. (Flexibility)", "scores": {"ENFP": 6, "ESFP": 6, "ENTP": 4, "ISFP": 2}}]},
        {"q": "16. Boss is best friend. You?", "opts": [{"txt": "A. Wake him up emotionally. (Bond)", "scores": {"ENFJ": 4, "INFJ": 7, "INFP": 5, "ESFJ": 2}}, {"txt": "B. Kill him. Duty. (Justice)", "scores": {"ESTJ": 6, "ISTJ": 6, "ENTJ": 4, "ISTP": 2}}, {"txt": "C. Pretend join, then betray. (Strategy)", "scores": {"ENTP": 3, "INTJ": 6, "INTP": 5, "ESTP": 2}}, {"txt": "D. Breakdown. (Sorrow)", "scores": {"INFP": 4, "ISFP": 7, "ISFJ": 4, "ESFP": 2}}]},
        {"q": "17. Sacrifice emotion to save world?", "opts": [{"txt": "A. Yes. Worth it. (Sacrifice)", "scores": {"ISFJ": 7, "ISTJ": 7, "INFJ": 5, "ESFJ": 3}}, {"txt": "B. No! Emotion is life. (Resist)", "scores": {"ESTP": 7, "ENTJ": 6, "ISTP": 5, "ESFP": 3}}, {"txt": "C. Find third way. (Solve)", "scores": {"INTP": 7, "INTJ": 4, "ENTP": 5, "ENFP": 2}}, {"txt": "D. No. Can't love anymore. (Love)", "scores": {"ISFP": 7, "ENFP": 6, "INFP": 6, "ESFP": 3}}]},
        {"q": "18. Holy Grail Wish?", "opts": [{"txt": "A. Eternal Order & Peace. (Order)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. Happiness & Food for all. (Joy)", "scores": {"ENFP": 3, "ESFP": 7, "ESFJ": 4, "ISFP": 2}}, {"txt": "C. Ultimate Knowledge. (Truth)", "scores": {"INTP": 7, "ENTP": 6, "INTJ": 5, "ISTP": 2}}, {"txt": "D. Normal peaceful life. (Simple)", "scores": {"ISFJ": 7, "INFJ": 6, "ISTJ": 4, "ISFP": 2}}]},
        {"q": "19. Friend cursed into Slime. You?", "opts": [{"txt": "A. Hug and keep him! (Cute)", "scores": {"ESFP": 7, "ENFP": 7, "ISFP": 5, "ESFJ": 3}}, {"txt": "B. Adjust team composition. (Logic)", "scores": {"ISTJ": 6, "ESTJ": 6, "INTJ": 4, "ISTP": 2}}, {"txt": "C. Study biology. (Curiosity)", "scores": {"INTP": 3, "ENTP": 2, "ISTP": 4, "INTJ": 2}}, {"txt": "D. Protect him forever. (Loyalty)", "scores": {"ISFJ": 7, "INFJ": 3, "ENFJ": 4, "INFP": 2}}]},
        {"q": "20. One-way portal home. You?", "opts": [{"txt": "A. Go home. Family. (Roots)", "scores": {"ISTJ": 7, "ISFJ": 7, "ESTJ": 5, "ESFJ": 3}}, {"txt": "B. Stay. Adventure! (Dream)", "scores": {"ENFP": 7, "ENTP": 2, "ESFP": 5, "ISFP": 3}}, {"txt": "C. Stay. I have power here. (Power)", "scores": {"ENTJ": 4, "INTJ": 6, "ESTP": 1, "ISTP": 2}}, {"txt": "D. Hesitate... (Conflict)", "scores": {"INFP": 4, "INFJ": 3, "ISFP": 4, "ENFJ": 2}}]},
        {"q": "21. Book Title?", "opts": [{"txt": "A. [Sword God]. (Power)", "scores": {"ESTP": 7, "ISTP": 7, "ENTJ": 4, "ESFP": 2}}, {"txt": "B. [Song of Wind]. (Poetic)", "scores": {"INFP": 4, "INFJ": 4, "ISFP": 5, "ENFP": 2}}, {"txt": "C. [Magic Analysis]. (Science)", "scores": {"INTP": 4, "ENTP": 3, "INTJ": 5, "ISTJ": 2}}, {"txt": "D. [Our Days]. (Memory)", "scores": {"ESFJ": 7, "ISFJ": 7, "ENFJ": 5, "ISFP": 2}}]},
        {"q": "22. Retirement place?", "opts": [{"txt": "A. Mage Tower. (Solitude)", "scores": {"INTJ": 7, "ISTJ": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "B. Forest Cabin. (Nature)", "scores": {"ISFP": 7, "INFP": 4, "INFJ": 2, "ISTP": 2}}, {"txt": "C. Tavern. (Stories)", "scores": {"ESFP": 7, "ENFP": 6, "ESTP": 5, "ESFJ": 2}}, {"txt": "D. Ruler's Throne. (Work)", "scores": {"ESTJ": 7, "ENTJ": 7, "ENFJ": 4, "ISTJ": 2}}]},
        {"q": "23. Best weapon inheritance?", "opts": [{"txt": "A. Tournament winner. (Strength)", "scores": {"ISTP": 7, "ESTP": 7, "ENTJ": 4, "INTJ": 2}}, {"txt": "B. Kind boy. (Heart)", "scores": {"ENFJ": 7, "ESFJ": 6, "INFJ": 2, "INFP": 3}}, {"txt": "C. Family/Disciple. (Tradition)", "scores": {"ISTJ": 7, "ISFJ": 7, "ESTJ": 5, "ESFP": 1}}, {"txt": "D. Throw in lake. (Fate)", "scores": {"ENTP": 3, "INTP": 6, "ENFP": 5, "ISFP": 2}}]},
        {"q": "24. Item to Earth?", "opts": [{"txt": "A. Dragon Egg. (Cool)", "scores": {"ENFP": 7, "ESFP": 7, "ENTP": 5, "ISTP": 2}}, {"txt": "B. Elixir. (Heal)", "scores": {"ISFJ": 7, "INFJ": 4, "ESFJ": 5, "INFP": 2}}, {"txt": "C. Gems. (Wealth)", "scores": {"ESTJ": 7, "ENTJ": 3, "ESTP": 5, "INTJ": 2}}, {"txt": "D. Magic Book. (Knowledge)", "scores": {"INTP": 4, "INTJ": 7, "ENTP": 5, "ISTJ": 1}}]},
        {"q": "25. Essence of Magic?", "opts": [{"txt": "A. Heart/Wish. (Faith)", "scores": {"INFJ": 4, "INFP": 4, "ENFJ": 5, "ISFP": 2}}, {"txt": "B. High Science. (Logic)", "scores": {"INTJ": 7, "INTP": 4, "ENTP": 5, "ISTJ": 2}}, {"txt": "C. Power/Tool. (Control)", "scores": {"ENTJ": 4, "ESTP": 6, "ISTP": 5, "ESTJ": 2}}, {"txt": "D. Miracle/Dream. (Hope)", "scores": {"ENFP": 7, "ESFP": 7, "ESFJ": 4, "ISFJ": 2}}]}
    ],
    "zombie": [
        {"q": "1. Alarm sounds, fire outside. First instinct?", "opts": [{"txt": "A. Lock door, fill water, check food. (Prepare)", "scores": {"ISTJ": 7, "ISFJ": 3, "INTJ": 3, "INFJ": 2}}, {"txt": "B. Call family, give orders, plan escape. (Lead)", "scores": {"ENTJ": 5, "ESTJ": 6, "ENFJ": 3, "ISTP": 2}}, {"txt": "C. Adrenaline! Grab weapon, guard door. (Fight)", "scores": {"ESTP": 6, "ISTP": 6, "ESFP": 4, "ENTP": 2}}, {"txt": "D. Check dark web for intel. (Analyze)", "scores": {"INTP": 4, "ENTP": 4, "ENFP": 3, "INTJ": 2}}]},
        {"q": "2. Injured mother & daughter ask for ride, low gas. You?", "opts": [{"txt": "A. 'Get in!' Save them. (Compassion)", "scores": {"ESFJ": 5, "ENFJ": 5, "ISFJ": 3, "ENFP": 3}}, {"txt": "B. 'Sorry.' Survival logic says no. (Rational)", "scores": {"ESTJ": 5, "ISTJ": 6, "INTJ": 4, "ENTJ": 3}}, {"txt": "C. Negotiate. 'Got water/weapons?' (Trade)", "scores": {"ENTP": 5, "ESTP": 5, "ENTJ": 3, "ISTP": 2}}, {"txt": "D. Conflict, cry but stop. (Emotion)", "scores": {"INFP": 7, "ISFP": 9, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "3. Mall survivors. Which group to join?", "opts": [{"txt": "A. Rooftop BBQ party. Enjoy now! (Fun)", "scores": {"ESFP": 8, "ENFP": 7, "ESTP": 4, "ISFP": 3}}, {"txt": "B. Veteran leader, strict rules. (Order)", "scores": {"ISTJ": 6, "ESTJ": 5, "ISFJ": 3, "ENTJ": 2}}, {"txt": "C. Prayer group, sharing stories. (Soul)", "scores": {"INFJ": 6, "INFP": 5, "ENFJ": 4, "ISFP": 2}}, {"txt": "D. Hardware tech group, modding drones. (Tech)", "scores": {"INTP": 4, "ISTP": 5, "ENTP": 4, "INTJ": 2}}]},
        {"q": "4. Evacuation. One item?", "opts": [{"txt": "A. Loaded SMG. Firepower. (Power)", "scores": {"ESTP": 5, "ISTP": 5, "ENTJ": 3, "ESTJ": 2}}, {"txt": "B. Medkit. Health. (Care)", "scores": {"ISFJ": 3, "ESFJ": 4, "INFJ": 3, "ENFJ": 2}}, {"txt": "C. Satellite Phone. Intel. (Info)", "scores": {"ENTP": 4, "INTJ": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "D. Polaroid & Diary. Memory. (Record)", "scores": {"ISFP": 9, "ENFP": 6, "INFP": 5, "INFJ": 3}}]},
        {"q": "5. Night watch. Thoughts?", "opts": [{"txt": "A. 'Cruel world, but beautiful stars.' (Aesthetic)", "scores": {"INFJ": 10, "INFP": 6, "ISFP": 4, "ENFP": 2}}, {"txt": "B. 'Humanity is virus, Earth reboot.' (Logic)", "scores": {"INTP": 4, "ENTJ": 5, "INTJ": 4, "ENTP": 2}}, {"txt": "C. 'Plan route for tomorrow.' (Plan)", "scores": {"ISTJ": 6, "ESTJ": 6, "ENTJ": 3, "ISTP": 2}}, {"txt": "D. 'Miss my parents.' (Love)", "scores": {"ESFJ": 5, "ISFJ": 5, "ENFJ": 4, "ESFP": 2}}]},
        {"q": "6. Medic bitten, begs for amputation to try saving. You?", "opts": [{"txt": "A. Chop immediately. No hesitation. (Decisive)", "scores": {"ENTJ": 5, "ESTJ": 5, "ISTP": 4, "INTJ": 3}}, {"txt": "B. Hug and comfort while doing it. (Gentle)", "scores": {"ENFJ": 5, "ESFJ": 5, "INFJ": 6, "ISFJ": 2}}, {"txt": "C. Can't do it. Pass knife. (Soft)", "scores": {"ISFP": 6, "INFP": 6, "ISFJ": 6, "ESFP": 2}}, {"txt": "D. 'Wait! Any other way?' (Think)", "scores": {"ENTP": 5, "ENFP": 6, "INTP": 3, "ESFP": 2}}]},
        {"q": "7. Found warehouse with family inside. You?", "opts": [{"txt": "A. Force them out. Survival of fittest. (Force)", "scores": {"ESTP": 6, "ISTP": 6, "ENTJ": 3, "ESTJ": 2}}, {"txt": "B. Negotiate cooperation. (Talk)", "scores": {"ENFJ": 5, "ENFP": 5, "ESFJ": 3, "INFJ": 2}}, {"txt": "C. Steal supplies quietly. (Stealth)", "scores": {"ISTJ": 7, "INTJ": 5, "INTP": 3, "ISFJ": 2}}, {"txt": "D. Trick them. (Deception)", "scores": {"ENTP": 6, "INFJ": 5, "ENFJ": 2, "INTJ": 2}}]},
        {"q": "8. Teammate steals food. You?", "opts": [{"txt": "A. Public expose & threat. (Justice)", "scores": {"ESTJ": 6, "ENTJ": 5, "ISTP": 3, "ESTP": 2}}, {"txt": "B. Meeting to expel. (Consensus)", "scores": {"INFJ": 5, "ENFJ": 5, "ESFJ": 3, "INTJ": 2}}, {"txt": "C. Use him as bait later. (Utility)", "scores": {"ENTP": 5, "INTJ": 5, "INTP": 4, "ENTJ": 1}}, {"txt": "D. Share my food. (Sacrifice)", "scores": {"ISFJ": 7, "ISFP": 5, "INFP": 4, "ESFJ": 2}}]},
        {"q": "9. Found MP3 player. Song?", "opts": [{"txt": "A. Heavy Metal. Adrenaline. (Energy)", "scores": {"ESTP": 7, "ESFP": 7, "ENTP": 4, "ISTP": 3}}, {"txt": "B. Old Pop. Normalcy. (Routine)", "scores": {"ISTJ": 7, "ISFJ": 3, "ESFJ": 3, "ISFP": 2}}, {"txt": "C. Classical. Solemnity. (Deep)", "scores": {"INTJ": 5, "INTP": 5, "INFJ": 4, "ISTJ": 2}}, {"txt": "D. Shuffle. Surprise. (Random)", "scores": {"ENFP": 6, "ISFP": 6, "ESFP": 4, "ENTP": 2}}]},
        {"q": "10. Zombies in tunnel. No shooting. You?", "opts": [{"txt": "A. Shield wall push. (Teamwork)", "scores": {"ESTJ": 5, "ENTJ": 5, "ISTJ": 3, "INTJ": 2}}, {"txt": "B. Machete melee. (Combat)", "scores": {"ISTP": 7, "ISFP": 5, "ESTP": 4, "ESFP": 2}}, {"txt": "C. Distract with toy. (Clever)", "scores": {"ENTP": 4, "ENFP": 5, "INTP": 4, "ESFP": 2}}, {"txt": "D. 'Run!' Make noise to save others. (Hero)", "scores": {"ESFJ": 6, "ISFJ": 6, "ENFJ": 4, "INFP": 2}}]},
        {"q": "11. Base leader?", "opts": [{"txt": "A. Me. I make hard calls. (Leader)", "scores": {"ENTJ": 4, "ESTJ": 5, "ENFJ": 2, "INTJ": 2}}, {"txt": "B. Strongest fighter. (Strength)", "scores": {"ISTP": 7, "ESTP": 6, "ENTP": 3, "ESFP": 2}}, {"txt": "C. Vote. (Democracy)", "scores": {"ENFJ": 4, "ESFJ": 6, "ENFP": 4, "INFJ": 2}}, {"txt": "D. Anyone but me. (Indiff)", "scores": {"INTP": 4, "INFP": 5, "ISFP": 4, "ISTP": 2}}]},
        {"q": "12. Resource dispute. Solution?", "opts": [{"txt": "A. Equal share. (Fairness)", "scores": {"ISFJ": 5, "ISFP": 5, "ESFJ": 3, "INFP": 2}}, {"txt": "B. Contribution based. (Merit)", "scores": {"ESTJ": 5, "ENTJ": 5, "ISTP": 4, "INTJ": 2}}, {"txt": "C. Market system. (Trade)", "scores": {"ENTP": 4, "ESTP": 5, "INTP": 4, "ENFP": 2}}, {"txt": "D. Need based. (Charity)", "scores": {"INFJ": 6, "ENFJ": 5, "INFP": 4, "ESFJ": 3}}]},
        {"q": "13. Child asks: 'Why survive?' You?", "opts": [{"txt": "A. 'For each other.' (Love)", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "ENFP": 2}}, {"txt": "B. 'For future fun!' (Hope)", "scores": {"ESFP": 7, "ENFP": 7, "ESTP": 4, "ISFP": 2}}, {"txt": "C. 'Duty to humanity.' (Duty)", "scores": {"ISTJ": 6, "ESTJ": 5, "ENTJ": 3, "INTJ": 2}}, {"txt": "D. 'Finding meaning in absurdity.' (Phil)", "scores": {"INTJ": 6, "INTP": 6, "INFJ": 4, "ISTP": 2}}]},
        {"q": "14. Base job?", "opts": [{"txt": "A. Inventory/Farming. (Logistics)", "scores": {"ISTJ": 7, "ISFJ": 3, "ESFJ": 3, "ISFP": 2}}, {"txt": "B. Traps/Defense. (Engineer)", "scores": {"INTP": 5, "ENTP": 5, "INTJ": 3, "INFJ": 1}}, {"txt": "C. Patrol/Building. (Labor)", "scores": {"ISTP": 5, "ESTP": 5, "ISFP": 3, "ESFP": 2}}, {"txt": "D. Foreman. (Manage)", "scores": {"ESTJ": 5, "ENTJ": 5, "ENFJ": 3, "ISTJ": 1}}]},
        {"q": "15. 1 Year Party. You?", "opts": [{"txt": "A. Dance and hype! (Party)", "scores": {"ESFP": 7, "ENFP": 6, "ESTP": 4, "ESFJ": 2}}, {"txt": "B. Make decorations/Music. (Art)", "scores": {"ISFP": 6, "INFP": 6, "INFJ": 3, "ISFJ": 2}}, {"txt": "C. Serve food. (Service)", "scores": {"ESFJ": 7, "ENFJ": 5, "ISFJ": 4, "ESTJ": 2}}, {"txt": "D. Sit and plan. (Quiet)", "scores": {"INTJ": 5, "ISTP": 5, "INTP": 2, "ENTJ": 2}}]},
        {"q": "16. Lover infected, hidden. You?", "opts": [{"txt": "A. Cry and hug till end. (Love)", "scores": {"INFP": 9, "ISFP": 10, "INFJ": 4, "ENFP": 2}}, {"txt": "B. 'Why hide it?' Analyze. (Logic)", "scores": {"INTP": 6, "ENTP": 5, "ISTP": 3, "ESTJ": 2}}, {"txt": "C. Shoot. 'I love you.' (Tough)", "scores": {"ENTJ": 5, "ESTJ": 5, "INTJ": 4, "ISTP": 4}}, {"txt": "D. Panic and deny. (Panic)", "scores": {"ESFJ": 7, "ENFJ": 6, "ESFP": 4, "ISFJ": 2}}]},
        {"q": "17. Scientist for Truce. You?", "opts": [{"txt": "A. Never. Future. (Vision)", "scores": {"INTJ": 6, "ENTJ": 5, "INTP": 4, "ISTJ": 2}}, {"txt": "B. Never. Loyalty. (Moral)", "scores": {"ENFJ": 6, "INFP": 5, "ESFJ": 4, "ISFP": 2}}, {"txt": "C. Ambush trap. (Trick)", "scores": {"ESTP": 6, "ENTP": 6, "ISTP": 4, "INTJ": 5}}, {"txt": "D. Hesitate. Greater good? (Weigh)", "scores": {"ISTJ": 7, "ESTJ": 5, "INTP": 3, "ISFJ": 2}}]},
        {"q": "18. Human experiments. You?", "opts": [{"txt": "A. Expose it! (Justice)", "scores": {"ENFP": 6, "INFP": 6, "ESFP": 4, "ENFJ": 2}}, {"txt": "B. Steal data. (Science)", "scores": {"INTP": 6, "ENTP": 6, "INTJ": 4, "ISTP": 2}}, {"txt": "C. Coup d'etat. (Power)", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ISTP": 4}}, {"txt": "D. Pretend ignorance. (Safety)", "scores": {"ISFJ": 4, "ISTJ": 5, "ISFP": 4, "ESFJ": 2}}]},
        {"q": "19. Heli holds 4. You?", "opts": [{"txt": "A. Rush seat! (Survival)", "scores": {"ESTP": 6, "ESFP": 6, "ENTJ": 3, "ISTP": 4}}, {"txt": "B. Give to others. (Sacrifice)", "scores": {"INFJ": 8, "ENFJ": 6, "ISFJ": 4, "INFP": 2}}, {"txt": "C. Remove seats/squeeze. (Solution)", "scores": {"ENTP": 6, "INTP": 5, "ENFP": 5, "ESTP": 2}}, {"txt": "D. Stay and fight. (Home)", "scores": {"ISTJ": 6, "ISFJ": 6, "ESTJ": 4, "INTJ": 2}}]},
        {"q": "20. Nuke button. You?", "opts": [{"txt": "A. Press. For future. (Sacrifice)", "scores": {"INTJ": 6, "INFJ": 8, "ENTJ": 4, "INTP": 2}}, {"txt": "B. Hesitate. Love. (Emotion)", "scores": {"ISFP": 6, "INFP": 6, "ESFP": 6, "ENFP": 1}}, {"txt": "C. Don't press. Doubt. (Skeptic)", "scores": {"INTP": 4, "ISTP": 8, "ENTP": 4, "INTJ": 2}}, {"txt": "D. Press for family. (Protect)", "scores": {"ESFJ": 8, "ISFJ": 6, "ENFJ": 4, "ISFP": 2}}]},
        {"q": "21. Why you survived?", "opts": [{"txt": "A. Caution. (Careful)", "scores": {"ISTJ": 6, "ISFJ": 5, "ESTJ": 3, "INTJ": 1}}, {"txt": "B. Adaptability. (Fun)", "scores": {"ESTP": 5, "ESFP": 8, "ISTP": 3, "ENTP": 1}}, {"txt": "C. Belief. (Hope)", "scores": {"ENFP": 9, "INFP": 5, "ENFJ": 4, "INFJ": 1}}, {"txt": "D. Intellect. (Brain)", "scores": {"ENTJ": 5, "INTP": 3, "INTJ": 4, "ENTP": 2}}]},
        {"q": "22. Post-war home?", "opts": [{"txt": "A. City. (Crowd)", "scores": {"ESFP": 8, "ESTP": 5, "ESFJ": 4, "ENFP": 2}}, {"txt": "B. Forest. (Peace)", "scores": {"INFP": 6, "ISFP": 6, "INFJ": 4, "INTP": 2}}, {"txt": "C. Tech Center. (Progress)", "scores": {"INTJ": 5, "ENTP": 5, "INTP": 4, "ENTJ": 2}}, {"txt": "D. Hometown. (Restore)", "scores": {"ISFJ": 4, "ISTJ": 6, "ESFJ": 4, "ISFP": 2}}]},
        {"q": "23. Speech to kids?", "opts": [{"txt": "A. Be strong. (Power)", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ESTP": 2}}, {"txt": "B. Keep humanity. (Love)", "scores": {"ENFJ": 6, "INFP": 5, "INFJ": 4, "ISFP": 2}}, {"txt": "C. Enjoy life. (Freedom)", "scores": {"ESFP": 8, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "D. Rebuild duty. (Duty)", "scores": {"ISTJ": 7, "ISFJ": 5, "ESFJ": 4, "INTJ": 1}}]},
        {"q": "24. Tombstone?", "opts": [{"txt": "A. Nothing. (Void)", "scores": {"INTP": 6, "ISTP": 6, "INTJ": 4, "ENTP": 2}}, {"txt": "B. 'BRB'. (Humor)", "scores": {"ENTP": 5, "ENFP": 9, "ESFP": 6, "ESTP": 2}}, {"txt": "C. 'Beloved'. (Love)", "scores": {"ESFJ": 7, "ISFJ": 3, "ENFJ": 3, "ISFP": 1}}, {"txt": "D. 'Builder'. (Legacy)", "scores": {"ENTJ": 6, "ESTJ": 5, "INTJ": 3, "ISTJ": 2}}]},
        {"q": "25. Meaning of Apocalypse?", "opts": [{"txt": "A. Awakening. (Spirit)", "scores": {"INFJ": 7, "INFP": 6, "ENFJ": 4, "ISFP": 2}}, {"txt": "B. Tragedy. (Sad)", "scores": {"ISTJ": 6, "ISFJ": 6, "ESTJ": 4, "ESFJ": 2}}, {"txt": "C. Adventure. (Thrill)", "scores": {"ESTP": 7, "ESFP": 7, "ENTP": 4, "ISTP": 2}}, {"txt": "D. Experiment. (Test)", "scores": {"INTP": 6, "INTJ": 6, "ENTJ": 4, "ENTP": 2}}]}
    ],
    "school": [
        {"q": "1. [Start] Noisy classroom. You?", "opts": [{"txt": "A. Greet friends warmly. (Social)", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Back seat, observe. (Quiet)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. Make grand entrance! (Star)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. Hide in corner. (Invisible)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},
        {"q": "2. [Rep] No volunteers. You?", "opts": [{"txt": "A. 'I'll do it.' (Leader)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Nominate quiet kid for fun. (Chaos)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. Volunteer to save awkwardness. (Help)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "D. Avoid eye contact. (Avoid)", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}]},
        {"q": "3. [Club] Which one?", "opts": [{"txt": "A. Dance/Sports. (Active)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. Science/Code. (Skill)", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "C. Student Council. (Power)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. Literature/Volunteer. (Soft)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "4. [Homework] Friend copies. You?", "opts": [{"txt": "A. 'Let's do it together!' (Team)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. 'No. Do it yourself.' (Strict)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Play dumb. (Hide)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. 'Change handwriting.' (Nice)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},
        {"q": "5. [After School] Sunset. You?", "opts": [{"txt": "A. Alone time. (Solitude)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. Hang out! (Play)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. Study. (Future)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Help others. (Service)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "6. [Exams] Strategy?", "opts": [{"txt": "A. Planned schedule. (Plan)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "B. All-nighter. (Burst)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. Analyze trends. (Smart)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. Organize group study. (Lead)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}]},
        {"q": "7. [Game] 10s left. You?", "opts": [{"txt": "A. Score myself! (Hero)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. Timeout & Tactic. (Plan)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. Cheer! (Support)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "D. Wait silently. (Sneak)", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},
        {"q": "8. [Cheat] Friend caught. You?", "opts": [{"txt": "A. 'Saw nothing.' (Loyal)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "B. Tell truth. (Honest)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Confuse teacher. (Debate)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "D. Beg for friend. (Mercy)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "9. [Fair] Booth idea?", "opts": [{"txt": "A. Haunted House. (Fun)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "B. Food stall. (Profit)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. Cafe. (Vibe)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. Charity. (Good)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "10. [Ghost] Old school rumor. You?", "opts": [{"txt": "A. Explore! (Adventure)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "B. Ignore. (Rational)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. Measure it. (Science)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. Pray. (Spirit)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "11. [Crush] Eye contact. You?", "opts": [{"txt": "A. 'Destiny!' (Dream)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. Ignore. (Cold)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Blush. (Shy)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. Smile. (Friendly)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},
        {"q": "12. [Confess] Method?", "opts": [{"txt": "A. Letter. (Private)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. Public Shout! (Loud)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "C. Direct. (Efficient)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. Perfect date. (Romantic)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "13. [Breakup] Friend sad. You?", "opts": [{"txt": "A. Cry with them. (Empathy)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. Have fun! (Distract)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. Analyze reason. (Fix)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Silent company. (Presence)", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},
        {"q": "14. [Rumor] About you. You?", "opts": [{"txt": "A. Fight back. (Confront)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Hide. (Hurt)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Joke about it. (Humor)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. Trust friends. (Faith)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "15. [Trip] Roommate?", "opts": [{"txt": "A. Friends together. (Bond)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Crazy ones. (Fun)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. Quiet ones. (Rest)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. Anyone. (Chill)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},
        {"q": "16. [Unfair] Punishment. You?", "opts": [{"txt": "A. Protest! (Rebel)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. Obey. (Accept)", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. Negotiate. (Talk)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}, {"txt": "D. Sneak out. (Run)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},
        {"q": "17. [Budget] Club poor. You?", "opts": [{"txt": "A. Demand money. (Fight)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. Fundraiser. (Earn)", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. Loophole. (Hack)", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. Unity matters. (Love)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "18. [Stolen] Notes stolen. You?", "opts": [{"txt": "A. Don't care. (Skill)", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. Sad but redo. (Bear)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Revenge. (Attack)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. Forgive. (Kind)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "19. [Play] Role?", "opts": [{"txt": "A. Lead/Director. (Lead)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Backstage. (Support)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "C. Comedy. (Funny)", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. Tech. (Skill)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}]},
        {"q": "20. [Capsule] Item?", "opts": [{"txt": "A. Dream Letter. (Dream)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. Photo. (Memory)", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "C. Prediction. (Logic)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Game/Toy. (Value)", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}]},
        {"q": "21. [Graduation] Feeling?", "opts": [{"txt": "A. Crying. (Sad)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. Free! (Joy)", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. Calm. (Next)", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "D. Sentimental. (Feel)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},
        {"q": "22. [Reunion] Image?", "opts": [{"txt": "A. Warm person. (Kind)", "scores": {"ISFJ": 7, "ESFJ": 6, "ENFJ": 4, "INFJ": 2}}, {"txt": "B. Successful. (Rich)", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. Unique. (Cool)", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. Funny. (Happy)", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]},
        {"q": "23. [Time] To self?", "opts": [{"txt": "A. Study hard. (Work)", "scores": {"ISTJ": 7, "INTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. Be brave. (Live)", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. You are fine. (Self)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. Cherish friends. (Love)", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "24. [Youth] Meaning?", "opts": [{"txt": "A. Impulse. (Action)", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. Dream. (Soft)", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Growth. (Learn)", "scores": {"INTJ": 7, "ISTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. Bond. (Together)", "scores": {"ENFJ": 7, "INFJ": 6, "ISFJ": 4, "ESFJ": 2}}]},
        {"q": "25. [Lesson] Learned?", "opts": [{"txt": "A. Reality. (Hard)", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. People. (Social)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. Independent. (Self)", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. Dream. (Hope)", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]}
    ],
    "cyber": [
        {"q": "1. [Connect] Wake up in pod. You?", "opts": [{"txt": "A. Check messages. (Social)", "scores": {"ESFJ": 7, "ENFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Scan environment. (Data)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. Wear flashy gear. (Show)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. Ignore world. (Hide)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}]},
        {"q": "2. [Conflict] Gang fight. You?", "opts": [{"txt": "A. Take command. (Order)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Hack screens. (Troll)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. Help injured. (Kind)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "D. Stealth mode. (Gone)", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}]},
        {"q": "3. [Mod] Free mod?", "opts": [{"txt": "A. Neon Skin. (Cool)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. Processor. (Brain)", "scores": {"INTP": 7, "ISTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "C. Command Unit. (Power)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. Empathy Chip. (Feel)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "4. [Job] Friend stole data. You?", "opts": [{"txt": "A. Expose corp! (Rebel)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. Refuse. (Law)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Ignore. (Safe)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "D. Help hide. (Loyal)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}]},
        {"q": "5. [Rest] Rainy night. You?", "opts": [{"txt": "A. Solitude. (Quiet)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. Rave! (Party)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. Learn skill. (Work)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Help poor. (Give)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "6. [Mission] Infiltration strategy?", "opts": [{"txt": "A. Plan details. (Plan)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "B. Explosion! (Loud)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "C. Virus. (Hack)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. Teamwork. (Lead)", "scores": {"ENTJ": 7, "ESTJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "7. [Combat] Gun jammed. You?", "opts": [{"txt": "A. Melee! (Brave)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "B. Retreat. (Smart)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. Cheer. (Support)", "scores": {"ENFJ": 7, "ENFP": 6, "ESFJ": 4, "ISFP": 2}}, {"txt": "D. Disable button. (Spot)", "scores": {"INFJ": 7, "INTP": 6, "ISFJ": 4, "ISTP": 2}}]},
        {"q": "8. [Crime] Partner selling data. You?", "opts": [{"txt": "A. Ignore. (Survival)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "B. Stop him. (Rule)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Split profit? (Deal)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "D. Advise him. (Care)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}]},
        {"q": "9. [Market] Selling what?", "opts": [{"txt": "A. Dreams. (Fun)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "B. Intel. (Profit)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "C. Art. (Soul)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "D. Repairs. (Help)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "10. [Legend] AI Ghost house. You?", "opts": [{"txt": "A. Explore! (Curious)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "B. Avoid. (Safe)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. Analyze. (Study)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "D. Caution. (Feel)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "11. [Crush] Cyborg encounter. You?", "opts": [{"txt": "A. Destiny! (Love)", "scores": {"ENFP": 7, "ESFP": 6, "INFP": 4, "ESFJ": 2}}, {"txt": "B. Scanning me? (Doubt)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "C. Shy. (Hide)", "scores": {"INFP": 7, "INFJ": 6, "ISFP": 4, "ISFJ": 2}}, {"txt": "D. Talk. (Active)", "scores": {"ESTP": 7, "ENTP": 6, "ENTJ": 4, "ESFP": 2}}]},
        {"q": "12. [Confess] Method?", "opts": [{"txt": "A. Code poem. (Deep)", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ISFP": 2}}, {"txt": "B. Billboard. (Loud)", "scores": {"ENFP": 7, "ENTP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "C. Direct. (Real)", "scores": {"ENTJ": 7, "ESTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "D. VR Date. (Romance)", "scores": {"ESFJ": 7, "ENFJ": 6, "ESFP": 4, "ENFP": 2}}]},
        {"q": "13. [Breakup] Friend sad. You?", "opts": [{"txt": "A. Comfort. (Warm)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "B. Gamble! (Fun)", "scores": {"ESTP": 7, "ESFP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. Solve it. (Fix)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Silence. (Stay)", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}]},
        {"q": "14. [Rumor] Corp dog? You?", "opts": [{"txt": "A. Fight back. (Truth)", "scores": {"ESTJ": 7, "ENTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Ignore. (Hide)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Mock it. (Joke)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. Trust. (Faith)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "15. [Team] Raid team?", "opts": [{"txt": "A. Trustworthy. (Bond)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Crazy! (Wild)", "scores": {"ESFP": 7, "ESTP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. Pro. (Skill)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. Quiet. (Solo)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}]},
        {"q": "16. [Unfair] Police scan. You?", "opts": [{"txt": "A. Protest! (Rights)", "scores": {"ENFP": 7, "ENTP": 6, "ENFJ": 4, "ESFP": 2}}, {"txt": "B. Comply. (Safe)", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "C. Talk. (Peace)", "scores": {"INFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFJ": 2}}, {"txt": "D. Sneak away. (Escape)", "scores": {"ISTP": 7, "INTP": 6, "ESFP": 3, "ENTP": 2}}]},
        {"q": "17. [Budget] No money. You?", "opts": [{"txt": "A. Investors. (Deal)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. Rob! (Fast)", "scores": {"ESTP": 7, "ESFP": 6, "ENFP": 4, "ENTP": 2}}, {"txt": "C. Mining. (Tech)", "scores": {"ISTP": 7, "INTP": 6, "ISFP": 4, "INFP": 2}}, {"txt": "D. Unity. (Together)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}]},
        {"q": "18. [Theft] Stolen code. You?", "opts": [{"txt": "A. Move on. (Pride)", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "B. Endure. (Quiet)", "scores": {"INTP": 7, "ISTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Revenge. (Attack)", "scores": {"ENTP": 7, "ENFP": 6, "ESTP": 4, "ESFP": 2}}, {"txt": "D. Forgive. (Kind)", "scores": {"ISFJ": 7, "INFJ": 6, "ESFJ": 4, "ENFJ": 2}}]},
        {"q": "19. [Plan] Role?", "opts": [{"txt": "A. Leader. (Lead)", "scores": {"ENFJ": 7, "ESFJ": 6, "ISFJ": 4, "INFJ": 2}}, {"txt": "B. Design. (Art)", "scores": {"ISFP": 7, "INFP": 6, "ISTP": 4, "INTP": 2}}, {"txt": "C. Bait. (Action)", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "D. Monitor. (Control)", "scores": {"ISTJ": 7, "INTJ": 6, "ESTJ": 4, "ENTJ": 2}}]},
        {"q": "20. [Backup] Memory?", "opts": [{"txt": "A. Stars. (Pure)", "scores": {"INFP": 7, "ISFP": 6, "INTP": 4, "ISTP": 2}}, {"txt": "B. Friends. (Bond)", "scores": {"INFJ": 7, "ISFJ": 6, "ESFJ": 4, "ENFJ": 2}}, {"txt": "C. Code. (Legacy)", "scores": {"INTJ": 7, "ISTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "D. Money. (Survival)", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}]},
        {"q": "21. [End] Feeling?", "opts": [{"txt": "A. Sad. (Miss)", "scores": {"ESFJ": 7, "ISFJ": 6, "ENFJ": 4, "ESFP": 2}}, {"txt": "B. Free! (Done)", "scores": {"ISTP": 7, "INTP": 6, "ESTP": 4, "ENTP": 2}}, {"txt": "C. Calm. (Next)", "scores": {"ENTJ": 7, "INTJ": 6, "ESTJ": 4, "ISTJ": 2}}, {"txt": "D. Poetic. (Hope)", "scores": {"INFP": 7, "INFJ": 6, "ISFP": 4, "ENFP": 2}}]},
        {"q": "22. [Legend] Image?", "opts": [{"txt": "A. Guardian. (Care)", "scores": {"ISFJ": 7, "ESFJ": 6, "ENFJ": 4, "INFJ": 2}}, {"txt": "B. Builder. (Order)", "scores": {"ESTJ": 7, "ENTJ": 6, "INTJ": 4, "ISTJ": 2}}, {"txt": "C. Ghost. (Mystery)", "scores": {"INTP": 7, "ISFP": 6, "INFJ": 4, "ISTP": 2}}, {"txt": "D. Legend. (Fun)", "scores": {"ENFP": 7, "ENTP": 6, "ESTP": 4, "ESFP": 2}}]},
        {"q": "23. [Time] To self?", "opts": [{"txt": "A. Invest. (Smart)", "scores": {"ISTJ": 7, "INTJ": 6, "ENTJ": 4, "ESTJ": 2}}, {"txt": "B. Burn. (Live)", "scores": {"ESFP": 7, "ESTP": 6, "ENTP": 4, "ENFP": 2}}, {"txt": "C. Heart. (Feel)", "scores": {"INFJ": 7, "INFP": 6, "ISFJ": 4, "ISTJ": 2}}, {"txt": "D. Loophole. (Win)", "scores": {"ENTP": 7, "ISTP": 6, "INTP": 4, "ESTP": 2}}]},
        {"q": "24. [Def] Cyberpunk is?", "opts": [{"txt": "A. Metal and Flesh. Life on the edge. (Action)", "scores": {"ENTP": 7, "ENFP": 6, "ESFP": 4, "ESTP": 2}}, {"txt": "B. Loneliness under neon. Tech vs Humanity. (Dream)", "scores": {"ISTP": 7, "INTP": 6, "INFP": 4, "ISFP": 2}}, {"txt": "C. Survival in chaos. Finding stability. (Growth)", "scores": {"INTJ": 7, "ISTJ": 6, "ESTJ": 4, "ENTJ": 2}}, {"txt": "D. Evolution trial. Transcending limits. (Bond)", "scores": {"ENFJ": 7, "INFJ": 6, "ISFJ": 4, "ESFJ": 2}}]},
        {"q": "25. [Last Lesson] Most important lesson?", "opts": [{"txt": "A. Tech evolves, survival is constant. (Real)", "scores": {"ENTJ": 7, "ESTJ": 6, "ISTJ": 4, "INTJ": 2}}, {"txt": "B. Cyberware replaced, friends cannot. (Network)", "scores": {"ESFJ": 7, "ENFJ": 6, "INFJ": 4, "ISFJ": 2}}, {"txt": "C. Stay independent, don't be brainwashed. (Think)", "scores": {"INTP": 7, "ENTP": 6, "ISTP": 4, "INTJ": 2}}, {"txt": "D. Even with machine body, soul is free. (Dream)", "scores": {"ISFP": 7, "INFP": 6, "INFJ": 4, "ENFP": 2}}]}
    ]
}

# 5. 雙語寄信函數 (取代原本的中文版)
def send_email_dual(user_email, mbti_types, universe, lang):
    try:
        SENDER = st.secrets["SENDER_EMAIL"]
        PWD = st.secrets["APP_PASSWORD"]
    except: return False

    subject_zh = f"🌌 你的多重宇宙 MBTI 測驗結果"
    subject_en = f"🌌 Your Multiverse MBTI Result"
    
    body_zh = f"你好！\n\n🌌 宇宙：{universe}\n🎯 結果：{', '.join(mbti_types)}\n\n(系統自動發送)"
    body_en = f"Hello!\n\n🌌 Universe: {universe}\n🎯 Result: {', '.join(mbti_types)}\n\n(Automated Email)"

    msg = MIMEText(body_zh if lang == 'zh' else body_en, 'plain', 'utf-8')
    msg['Subject'] = subject_zh if lang == 'zh' else subject_en
    msg['From'] = SENDER
    msg['To'] = user_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, PWD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False
# ==========================================
# 5.5 (新增) 雷達圖繪製函數 (修正參數版)
# ==========================================
def draw_radar_chart(user_answers, question_list):
    # 1. 先重新計算一次原始分數
    raw_scores = {key: 0 for key in ["ESTJ", "ENTJ", "ESFJ", "ENFJ", "ISTJ", "ISFJ", "INTJ", "INFJ", "ESTP", "ESFP", "ENTP", "ENFP", "ISTP", "ISFP", "INTP", "INFP"]}
    
    for i, choice_index in enumerate(user_answers):
        if choice_index is not None:
            # 安全檢查
            if i < len(question_list) and choice_index < len(question_list[i]["opts"]):
                points_table = question_list[i]["opts"][choice_index]["scores"]
                for mbti, points in points_table.items():
                    if mbti in raw_scores:
                        raw_scores[mbti] += points

    # 2. 將 16 人格分數轉換成 5 大 RPG 能力值
    stats = {
        "🧠 Logic": 0,
        "❤️ Empathy": 0,
        "⚡ Action": 0,
        "🛡️ Order": 0,
        "✨ Creative": 0
    }
    
    for mbti, score in raw_scores.items():
        if 'T' in mbti: stats["🧠 Logic"] += score
        if 'F' in mbti: stats["❤️ Empathy"] += score
        if 'P' in mbti: stats["⚡ Action"] += score
        if 'J' in mbti: stats["🛡️ Order"] += score
        if 'N' in mbti: stats["✨ Creative"] += score
        if 'S' in mbti: stats["⚡ Action"] += score * 0.5 
        
    # 3. 數據標準化
    max_val = max(stats.values()) if max(stats.values()) > 0 else 1
    r_values = [int((v / max_val) * 100) for v in stats.values()]
    theta_labels = list(stats.keys())
    
    # 為了讓雷達圖閉合
    r_values.append(r_values[0])
    theta_labels.append(theta_labels[0])

    # 4. 使用 Plotly 畫圖 (修正參數名稱)
    fig = go.Figure(
        data=go.Scatterpolar(
            r=r_values,
            theta=theta_labels,
            fill='toself',
            name='Ability',
            # ★★★ 修正點在這裡 ★★★
            line=dict(color='#FF0099'),     # 改成字典格式
            fillcolor='rgba(255, 0, 153, 0.2)' # 去掉底線
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False
            )
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
# ==========================================
# 5. 判讀邏輯函數
# ==========================================
def calculate_sorting_result(answers):
    scores = {"fantasy": 0, "zombie": 0, "school": 0, "cyber": 0}
    for ans_code in answers:
        scores[ans_code] += 1
        
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    top1_theme, top1_score = sorted_scores[0]
    top2_theme, top2_score = sorted_scores[1]
    
    if top1_score == top2_score:
        return "TIE", [top1_theme, top2_theme]
    else:
        return "WIN", top1_theme

# 5-2. 正式劇本算分函數 (3分誤差寬容版)
def calculate_mbti(user_answers, question_list):
    # 1. 初始化 16 人格分數板
    scores = {key: 0 for key in ["ESTJ", "ENTJ", "ESFJ", "ENFJ", "ISTJ", "ISFJ", "INTJ", "INFJ", "ESTP", "ESFP", "ENTP", "ENFP", "ISTP", "ISFP", "INTP", "INFP"]}
    
    # 2. 跑迴圈對答案 (算分邏輯不變)
    for i, choice_index in enumerate(user_answers):
        if choice_index is not None:
            points_table = question_list[i]["opts"][choice_index]["scores"]
            for mbti, points in points_table.items():
                if mbti in scores:
                    scores[mbti] += points

    # 3. ★★★ 關鍵修改：找出最高分，並包含差距 3 分以內的人 ★★★
    
    # 先找出全場最高分 (例如 100 分)
    max_score = max(scores.values()) 
    
    # 設定門檻：最高分 - 3 (例如 100 - 3 = 97 分)
    # 只要大於等於 97 分的，通通算贏家
    threshold = max_score - 3
    
    # 篩選出符合資格的人格
    final_mbtis = [mbti for mbti, score in scores.items() if score >= threshold]
    
    # (選用) 為了讓顯示好看，我們可以依照分數「由高到低」重新排序一下
    # 這樣 100 分的會排在前面，97 分的排在後面
    final_mbtis.sort(key=lambda x: scores[x], reverse=True)
    
    return final_mbtis

# ==========================================
# 6. 頁面控制流程 (Router - 雙語版)
# ==========================================

# 0. 狀態初始化補強 (確保有語言變數)
if 'page' not in st.session_state: st.session_state.page = 'language_select'
if 'language' not in st.session_state: st.session_state.language = 'zh'

# 1. 根據語言設定當前的資料集
lang = st.session_state.language
txt = UI_TEXT[lang] # 抓取對應語言的介面文字
# 這裡是關鍵：如果選中文就用 ZH 變數，選英文就用 EN 變數
current_quizzes = ALL_QUIZZES_ZH if lang == 'zh' else ALL_QUIZZES_EN
current_info = MBTI_INFO_ZH if lang == 'zh' else MBTI_INFO_EN
current_sorting = SORTING_QUIZ_ZH if lang == 'zh' else SORTING_QUIZ_EN

# --- Page 1: 語言選擇 (Language Selection) ---
if st.session_state.page == 'language_select':
    st.title("🌍 Welcome / 歡迎")
    st.markdown("### Choose your interface language / 請選擇介面語言")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("中文 (Traditional Chinese)", use_container_width=True):
            st.session_state.language = 'zh'
            st.session_state.page = 'landing'
            st.rerun()
            
    with col2:
        if st.button("English", use_container_width=True):
            st.session_state.language = 'en'
            st.session_state.page = 'landing'
            st.rerun()

# --- Page 2: 首頁/前導測驗 (Landing) ---
elif st.session_state.page == 'landing':
    st.markdown(f'<div class="big-title">{txt["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{txt["subtitle"]}</div>', unsafe_allow_html=True)
    
    st.number_input(txt['age_label'], min_value=1, max_value=100, value=18)
    st.write("---")
    
    st.write(f"### {txt['intro_title']}")
    st.info(txt['intro_desc'])

    with st.form("sorting_form"):
        user_choices = []
        for i, item in enumerate(current_sorting):
            st.subheader(item["q"])
            # 選項格式：中文版 opts 是 (文字, 代號)，英文版也是 (文字, 代號)
            choice = st.radio(
                f"Q {i+1}", 
                item["opts"], 
                format_func=lambda x: x[0],
                index=None, 
                key=f"sorting_{i}"
            )
            if choice:
                user_choices.append(choice[1]) # 儲存 universe code (例如 'zombie')
            st.write("")
            
        submitted = st.form_submit_button(txt['start_btn'], type="primary")
        
        if submitted:
            if len(user_choices) < 5:
                st.error(txt['error_incomplete'])
            else:
                status, result = calculate_sorting_result(user_choices)
                
                if status == "TIE":
                    st.session_state.tie_themes = result
                    st.session_state.page = 'tie_breaker'
                    st.rerun()
                else:
                    st.session_state.target_theme = result
                    st.session_state.page = 'main_quiz'
                    st.rerun()

# --- Page 3: 同分決戰 (Tie Breaker) ---
elif st.session_state.page == 'tie_breaker':
    st.markdown(f'<div class="big-title">{txt["tie_title"]}</div>', unsafe_allow_html=True)
    st.warning(txt['tie_warn'])
    
    if not st.session_state.tie_themes:
        st.session_state.page = 'landing'
        st.rerun()
    else:
        st.write(txt['tie_desc'])
        
        theme_a = st.session_state.tie_themes[0]
        theme_b = st.session_state.tie_themes[1]
        
        # 讀取對應語言的選項文字
        tie_text_opts = txt['tie_options']
        
        choice = st.radio(
            "Choice / 抉擇",
            [
                (tie_text_opts.get(theme_a, theme_a), theme_a),
                (tie_text_opts.get(theme_b, theme_b), theme_b)
            ],
            format_func=lambda x: x[0]
        )
        
        if st.button(txt['tie_btn'], type="primary"):
            st.session_state.target_theme = choice[1]
            st.session_state.page = 'main_quiz'
            st.rerun()

# --- Page 4: 主測驗 (Main Quiz) ---
elif st.session_state.page == 'main_quiz':
    current_theme = st.session_state.target_theme
    
    # 顯示對應語言的劇本標題
    display_title = txt['titles'].get(current_theme, current_theme)
    st.markdown(f'<div class="big-title">{display_title}</div>', unsafe_allow_html=True)

    # 從當前語言的題庫中抓題目 (加權分數都在裡面)
    questions = current_quizzes.get(current_theme, [])

    if not questions:
        st.warning("🚧 Content missing / 內容構建中...")
        if st.button("Back"):
            st.session_state.page = 'landing'
            st.rerun()
    else:
        st.write("---")
        with st.form("main_quiz_form"):
            user_answers = []
            
            for i, q_data in enumerate(questions):
                st.subheader(q_data["q"])
                # 這裡要小心，原本中文版 opts 是 [{"txt":..., "scores":...}]
                # 因為我們用 copy()，所以結構完全一致，可以放心讀取
                choice = st.radio(
                    f"Q{i+1}", 
                    q_data["opts"], 
                    format_func=lambda x: x["txt"], 
                    index=None,
                    key=f"mq_{current_theme}_{i}"
                )
                
                if choice:
                    idx = q_data["opts"].index(choice)
                    user_answers.append(idx)
                else:
                    user_answers.append(None)
                st.write("")
            
            submit = st.form_submit_button(txt['quiz_submit'], type="primary")
            
            if submit:
                if None in user_answers:
                    st.error(txt['error_incomplete'])
                else:
                    # 計算時使用 questions 裡面的 scores，分數不會錯
                    st.session_state.user_answers = user_answers
                    result_mbti = calculate_mbti(user_answers, questions)
                    st.session_state.final_result = result_mbti
                    st.session_state.page = 'result_page'
                    st.rerun()

# --- Page 5: 結果頁 (Result) ---
elif st.session_state.page == 'result_page':
    final_results = st.session_state.final_result
    current_theme = st.session_state.get('target_theme', 'zombie')
    
    # 1. ★★★ 修正點：根據語言選擇對應的資料庫 ★★★
    # 必須先定義 current_qs 和 current_info
    if lang == 'zh':
        current_qs = ALL_QUIZZES_ZH.get(current_theme)
        current_info = MBTI_INFO_ZH
    else:
        current_qs = ALL_QUIZZES_EN.get(current_theme)
        current_info = MBTI_INFO_EN

    if 'has_balloons' not in st.session_state:
        st.balloons()
        st.session_state.has_balloons = True
    
    if len(final_results) > 1:
        st.success(txt['result_success'])
    else:
        st.success(txt['result_normal'])

    st.write("") 

    # 顯示結果卡片迴圈
    for mbti_type in final_results:
        default_info = {"title": "Unknown", "color": ["#333", "#333"], "desc": "No Data", "match": "?", "clash": "?", "strengths": [], "weaknesses": [], "career": {}}
        
        # 2. ★★★ 修正點：使用 current_info 而不是 MBTI_INFO ★★★
        info = current_info.get(mbti_type, default_info)
        
        c1, c2 = info['color']
        
        # 標題與稱號
        st.markdown(f"""
        <div style="text-align: center;">
            <h1 style="font-size: 80px; margin: 0; background: -webkit-linear-gradient(45deg, {c1}, {c2}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {mbti_type}
            </h1>
            <h2 style="font-size: 30px; color: #555; margin-top: -10px;">{info['title']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 裝飾條 & 描述
        st.markdown(f"""
        <div style="display: flex; gap: 5px; margin-bottom: 20px;">
            <div style="flex: 1; height: 10px; background-color: {c1}; border-radius: 5px;"></div>
            <div style="flex: 1; height: 10px; background-color: {c2}; border-radius: 5px;"></div>
        </div>
        <div style="background: rgba(255,255,255,0.5); padding: 20px; border-radius: 10px; border-left: 5px solid {c1}; margin-bottom: 20px;">
            <p style="font-size: 18px; line-height: 1.8; color: #333;">{info['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 社交區塊
        col_rel1, col_rel2 = st.columns(2)
        with col_rel1:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e0e0e0;">
                <h4 style="margin:0; color: #28a745;">{txt['match']}</h4>
                <h2 style="margin:5px 0 0 0; color: #333;">{info['match']}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_rel2:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e0e0e0;">
                <h4 style="margin:0; color: #dc3545;">{txt['clash']}</h4>
                <h2 style="margin:5px 0 0 0; color: #333;">{info['clash']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("") 

        # 優勢與盲點
        col_an1, col_an2 = st.columns(2)
        with col_an1:
            st.markdown(f"<h3 style='color: {c1}; border-bottom: 2px solid {c1};'>{txt['strength']}</h3>", unsafe_allow_html=True)
            for s in info.get('strengths', []):
                st.markdown(f"**+ {s}**")      
        with col_an2:
            st.markdown(f"<h3 style='color: #666; border-bottom: 2px solid #666;'>{txt['weakness']}</h3>", unsafe_allow_html=True)
            for w in info.get('weaknesses', []):
                st.markdown(f"**- {w}**")
        
        st.write("") 

        # 能力雷達圖 (至中)
        if current_qs and st.session_state.user_answers:
            c_left, c_center, c_right = st.columns([1, 3, 1])
            with c_center:
                radar_title = "📊 Ability Radar" if lang == 'en' else "📊 能力雷達分析"
                st.markdown(f"<h4 style='text-align: center; color: #555;'>{radar_title}</h4>", unsafe_allow_html=True)
                
                fig = draw_radar_chart(st.session_state.user_answers, current_qs)
                st.plotly_chart(fig, use_container_width=True)

        st.write("") 

        # 職業推薦
        display_title = txt['career_title']
        career_obj = info.get('career', {})
        if isinstance(career_obj, dict):
            career_text = career_obj.get(current_theme, list(career_obj.values())[0] if career_obj else "Unknown")
        else:
            career_text = str(career_obj)

        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 10px;">
            <h4 style="margin:0; color: #333;">{display_title}</h4>
            <p style="font-size: 20px; font-weight: bold; color: {c2}; margin: 5px 0 0 0;">{career_text}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("---") 

    # 3. ★★★ 修正點：UI文字 ID 修正 (對應 UI_TEXT 字典) ★★★
    st.write(f"### {txt['email_section']}")
    with st.expander(txt['email_section']):
        user_email = st.text_input(txt['email_label'], placeholder="name@example.com")
        
        if st.button(txt['email_btn']):
            if not user_email:
                st.error("Email required!")
            else:
                with st.spinner("Sending..."):
                    success = send_email_dual(user_email, final_results, current_theme, lang)
                    if success:
                        st.success(f"Sent to {user_email}!")
                    else:
                        st.error("Failed. Check secrets.toml")

    st.write("")
    
    if st.button(txt['restart_btn']):
        st.session_state.page = 'language_select'
        st.session_state.user_answers = [] 
        st.session_state.tie_themes = []
        st.session_state.final_result = None
        if 'has_balloons' in st.session_state:
            del st.session_state.has_balloons
        st.rerun()
# ==========================================
# 10. (開發者工具) 分數平衡檢查器 - 雙密鑰
# ==========================================
def check_balance(questions):
    max_scores = {key: 0 for key in ["ESTJ", "ENTJ", "ESFJ", "ENFJ", "ISTJ", "ISFJ", "INTJ", "INFJ", "ESTP", "ESFP", "ENTP", "ENFP", "ISTP", "ISFP", "INTP", "INFP"]}
    for q in questions:
        current_q_max = {key: 0 for key in max_scores.keys()}
        for opt in q["opts"]:
            for mbti, points in opt["scores"].items():
                if points > current_q_max[mbti]:
                    current_q_max[mbti] = points
        for mbti in max_scores.keys():
            max_scores[mbti] += current_q_max[mbti]
    return max_scores

with st.sidebar:
    st.write("---")
    
    # ★★★ 1.定義兩個密鑰 ★★★
    # 你可以在這裡隨意修改密碼
    VALID_KEYS = ["mikelovethomas", "mikeisadorableandchubby"]
    
    admin_pwd = st.text_input("開發人員通道", type="password", placeholder="輸入密鑰...")

    # 2. 檢查輸入的密碼是否在有效清單中
    if admin_pwd in VALID_KEYS:
        st.success(f"🔓 歡迎回來！權限已解鎖")
        st.header("🔧 劇本平衡檢測儀")
        
        # 3. 列出所有宇宙的按鈕 (不檢查是否為空)
        # 注意：這裡我們要檢查 ALL_QUIZZES_ZH，因為它是最完整的
        for theme_key, theme_data in ALL_QUIZZES_ZH.items():
            if st.button(f"檢查【{theme_key}】平衡"):
                if len(theme_data) == 0:
                    st.warning("⚠️ 這個劇本目前是空的 (0 題)，所以分數都是 0 喔！")
                else:
                    balance_data = check_balance(theme_data)
                    st.write(f"### {theme_key} 最高分潛力分佈")
                    st.bar_chart(balance_data)
                    max_val = max(balance_data.values())
                    min_val = min(balance_data.values())
                    st.info(f"差距: {max_val - min_val}")
# ==========================================
# 10. (開發者工具) AI 蒙地卡羅模擬器
# ==========================================

def run_monte_carlo_simulation(universe_key, iterations=1000):
    """
    執行蒙地卡羅模擬：
    1. 隨機生成 1000 個使用者的答案
    2. 使用正式的算分邏輯 (calculate_mbti)
    3. 統計每種人格被判定出來的次數 (包含多重人格的情況)
    """
    
    # 取得該宇宙的題目資料 (始終使用最完整的中文版資料進行模擬)
    questions = ALL_QUIZZES_ZH.get(universe_key, [])
    
    if not questions:
        return None, None, 0

    # 儲存所有出現過的人格 (例如: ['ESTJ', 'ENTJ', 'ISTP', ...])
    all_results_flat = [] 
    
    # 統計有多少次出現了「多重人格」的情況
    multi_personality_count = 0

    # 開始模擬
    progress_bar = st.progress(0)
    
    for i in range(iterations):
        # 1. 模擬隨機作答 (25題，每題隨機選 0~3)
        # random.randint(0, 3) 代表隨機選 ABCD
        sim_answers = [random.randint(0, 3) for _ in range(len(questions))]
        
        # 2. 呼叫核心演算法判讀
        results = calculate_mbti(sim_answers, questions)
        
        # 3. 收集結果
        # 如果 results 是 ['ESTJ', 'ENTJ']，這兩個都會被計入出現次數
        all_results_flat.extend(results)
        
        # 4. 紀錄是否為多重人格
        if len(results) > 1:
            multi_personality_count += 1
            
        # 更新進度條 (每 100 次更新一次，避免卡頓)
        if i % 100 == 0:
            progress_bar.progress((i + 1) / iterations)
            
    progress_bar.empty() # 清除進度條

    # 5. 統計頻率
    counts = Counter(all_results_flat)
    
    # 轉換成 DataFrame 方便畫圖
    df = pd.DataFrame.from_dict(counts, orient='index', columns=['Count'])
    df = df.sort_values(by='Count', ascending=False)
    
    return df, multi_personality_count, iterations

# --- 開發者側邊欄 UI ---
with st.sidebar:
    st.write("---")
    st.markdown("### 🛠️ Developer Console")
    
    # 定義密鑰
    VALID_KEYS = ["mikelovethomas", "mikeisadorableandchubby"]
    
    admin_pwd = st.text_input("輸入開發者密鑰", type="password")

    if admin_pwd in VALID_KEYS:
        st.success("🔓 權限已解鎖")
        st.markdown("#### 🤖 AI 隨機模擬器 (Monte Carlo)")
        
        # 選擇要模擬的宇宙
        sim_theme = st.selectbox("選擇測試宇宙", list(ALL_QUIZZES_ZH.keys()))
        
        # 選擇模擬次數
        sim_iters = st.slider("模擬使用者數量", 100, 5000, 1000)
        
        if st.button(f"開始模擬 {sim_theme}"):
            with st.spinner(f"正在生成 {sim_iters} 個虛擬使用者進行測試..."):
                df_res, multi_count, total = run_monte_carlo_simulation(sim_theme, sim_iters)
                
                if df_res is not None:
                    st.write("### 📊 人格出現頻率分佈")
                    st.write("此圖表顯示在隨機作答情況下，各人格被判定出的次數。若某人格過高/過低，代表權重需調整。")
                    
                    # 畫長條圖
                    st.bar_chart(df_res)
                    
                    # 顯示統計數據
                    multi_rate = (multi_count / total) * 100
                    st.info(f"**多重人格出現率**: {multi_rate:.1f}% ({multi_count}/{total})")
                    st.write(f"**最高頻**: {df_res.index[0]} ({df_res.iloc[0,0]}次)")
                    st.write(f"**最低頻**: {df_res.index[-1]} ({df_res.iloc[-1,0]}次)")
                    
                    # 顯示詳細數據表
                    with st.expander("查看詳細數據"):
                        st.dataframe(df_res)
                else:
                    st.error("該宇宙目前沒有題目數據！")
