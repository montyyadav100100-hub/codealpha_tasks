import streamlit as st
from difflib import get_close_matches



st.set_page_config(
    page_title="Campus FAQ Assistant",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    color: #667085;
    font-size: 17px;
    margin-bottom: 25px;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    margin: 0;
    font-size: 36px;
}

.hero p {
    margin-top: 10px;
    font-size: 16px;
}

.card {
    padding: 20px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- FAQ DATA ----------------

faqs = {

    "Admissions": {
        "What is the admission process?":
        "You can apply through the university's official admission portal. Complete the application form and upload the required documents.",

        "What documents are required for admission?":
        "Common documents include academic certificates, identity proof, photographs and other documents specified by the university.",

        "Can I apply online?":
        "Yes. Applications can generally be submitted through the university's online admission portal.",

        "When does admission start?":
        "Admission dates vary each academic year. Please check the official university announcements."
    },

    "Academics": {
        "What are the college timings?":
        "Regular academic activities generally take place from 9:00 AM to 5:00 PM, depending on your timetable.",

        "Where can I find my timetable?":
        "Your timetable can usually be found through the student portal or department notices.",

        "Is attendance compulsory?":
        "Yes. Students are expected to maintain the minimum attendance required by university regulations.",

        "How can I check my examination schedule?":
        "Examination schedules are normally announced through official university notices and the student portal.",

        "Where can I get study material?":
        "Study materials may be provided by faculty members, the learning management system or the student portal."
    },

    "Fees": {
        "How can I pay my fees?":
        "Fees can be paid through the university's designated online fee payment portal.",

        "Can I pay fees online?":
        "Yes. Online fee payment is generally available through the official university payment portal.",

        "How can I get my fee receipt?":
        "After payment, you can usually download the receipt from the payment portal or student portal.",

        "What happens if I miss the fee deadline?":
        "Late payment may result in additional charges or restrictions. Contact the accounts office for assistance."
    },

    "Campus": {
        "Where is the college located?":
        "The university is located in Greater Noida, Delhi NCR.",

        "Where is the library?":
        "The library is located on the university campus. You can check the campus map or ask the administration for directions.",

        "Is Wi-Fi available on campus?":
        "Campus Wi-Fi is available in designated areas according to university network policies.",

        "Are there sports facilities?":
        "Yes. The campus provides sports and recreational facilities for students.",

        "Is there a cafeteria?":
        "Yes. Students can access food and refreshment facilities available on campus."
    },

    "Student Services": {
        "How can I get my student ID card?":
        "Student ID cards are issued through the concerned university office.",

        "How can I contact the administration?":
        "You can contact the university administration through the official administrative office or university contact channels.",

        "How can I request a hostel room?":
        "Hostel accommodation can be requested through the university hostel administration, subject to availability.",

        "How can I get a bonafide certificate?":
        "Bonafide certificates can generally be requested through the student administration or academic office.",

        "How can I apply for leave?":
        "Students should submit leave requests through the appropriate faculty member, department or student portal."
    },

    "Placements": {
        "Does the university provide placement assistance?":
        "Yes. Placement and career services provide students with recruitment opportunities, training and career guidance.",

        "How can I register for placements?":
        "Students can register through the university placement cell or designated placement portal.",

        "Are internships available?":
        "Internship opportunities can be found through the placement cell, career office and external organizations.",

        "Is there placement training?":
        "Placement preparation may include aptitude tests, technical preparation, communication training and mock interviews."
    }
}


# Create one combined dictionary
all_questions = {}

for category in faqs:
    for question in faqs[category]:
        all_questions[question] = faqs[category][question]


# ---------------- FIND ANSWER ----------------

def find_answer(user_question):

    user_question = user_question.lower().strip()

    # Exact match
    for question in all_questions:

        if user_question == question.lower():
            return all_questions[question]

    # Similar question
    question_list = list(all_questions.keys())

    matches = get_close_matches(
        user_question,
        question_list,
        n=1,
        cutoff=0.4
    )

    if matches:
        return all_questions[matches[0]]

    # Keyword matching
    for question in all_questions:

        question_words = question.lower().split()

        for word in question_words:

            if len(word) > 4 and word in user_question:

                return all_questions[question]

    return (
        "I'm sorry, I couldn't find an answer to that question. "
        "Please try asking about admissions, academics, fees, "
        "campus, student services or placements."
    )


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🎓 CampusConnect")

    st.write("### FAQ Categories")

    category = st.selectbox(
        "Choose a category",
        list(faqs.keys())
    )

    st.divider()

    st.write("### 📊 Information")

    st.write(f"**Categories:** {len(faqs)}")
    st.write(f"**FAQs:** {len(all_questions)}")
    st.write(
        f"**Questions asked:** "
        f"{len([m for m in st.session_state.messages if m['role'] == 'user'])}"
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">

<h1>🎓 CampusConnect FAQ Assistant</h1>

<p>
Your virtual campus assistant for admissions, academics,
fees, facilities, student services and placements.
</p>

</div>
""", unsafe_allow_html=True)


# ---------------- FAQ SECTION ----------------

st.subheader("💡 Frequently Asked Questions")

st.write(
    f"Popular questions from **{category}**"
)


# Display questions as buttons
for question in faqs[category]:

    if st.button(
        "❓ " + question,
        key="faq_" + question,
        use_container_width=True
    ):

        # Add question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Add answer
        st.session_state.messages.append({
            "role": "assistant",
            "content": all_questions[question]
        })

        st.rerun()


# ---------------- CHAT ----------------

st.subheader("💬 Conversation")


if len(st.session_state.messages) == 0:

    st.info(
        "👋 Hello! Choose a FAQ above or type your own question below."
    )


# Show conversation
for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    else:

        with st.chat_message("assistant"):
            st.write(message["content"])


# ---------------- CHAT INPUT ----------------

user_question = st.chat_input(
    "Ask your question..."
)


if user_question:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Generate answer
    answer = find_answer(user_question)

    # Add bot answer
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()