import streamlit as st # type: ignore
from helpers.youtube_utils import extract_video_id_from_url, get_transcript_text
from helpers.groqai_utils import get_quiz_data
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast


st.set_page_config(
    page_title="QuizMaster Pro",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Check if user is new or returning using session state.
# If user is new, show the toast message.
if 'first_time' not in st.session_state:
    message, icon = get_random_toast()
    st.toast(message, icon=icon)
    st.session_state.first_time = False

with st.sidebar:
    st.header("👨‍💻 About the Author")
    st.write("""
    **Nachiket Kapure** is an AI enthusiast currently pursuing an MSc in AI from India. Passionate about AI and coding, he loves creating interactive applications with Streamlit and AI.

    Connect, contribute, or just say hi!
    """)


    st.divider()
    st.subheader("🔗 Connect with Me", anchor=False)
    st.markdown(
        """
        - [🐙 Source Code](https://github.com/Nachiket1904)
        - [🌐 Personal Website](https://nachiportfolio.netlify.app/)
        - [👔 LinkedIn](https://linkedin.com/in/nachiket-kapure-ai-enginner/)
        """
    )

    st.divider()
    st.write("Made with ♥ in Mumbai, India")


st.title(":red[QuizMaster] — Watch. Learn. Quiz. 🧠", anchor=False)
st.write("""
Ever watched a YouTube video and wondered how well you understood its content? Here's a fun twist: Instead of just watching on YouTube, come to **QuizMaster** and test your comprehension!

**How does it work?** 🤔
1. Paste the YouTube video URL of your recently watched video.
2. Enter your [Groq API Key](https://console.groq.com/docs/api-keys).

⚠️ Important: The video **must** have English captions for the tool to work.

Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test! 
""")

# with st.expander("💡 Video Tutorial"):
#     with st.spinner("Loading video.."):
#         st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Enter the YouTube video link:", value="")
    GROQ_API_KEY = st.text_input("Enter your Groq API Key:", placeholder="sk-XXXX", type='password')
    submitted = st.form_submit_button("Craft my quiz!")

if submitted or ('quiz_data_list' in st.session_state):
    if not YOUTUBE_URL:
        st.info("Please provide a valid YouTube video link. Head over to [YouTube](https://www.youtube.com/) to fetch one.")
        st.stop()
    elif not GROQ_API_KEY:
        st.info("Please fill out the Groq API Key to proceed. If you don't have one, you can obtain it [here](https://console.groq.com/docs/api-keys).")
        st.stop()
        
    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            video_id = extract_video_id_from_url(YOUTUBE_URL)
            video_transcription = get_transcript_text(video_id)
            quiz_data_str = get_quiz_data(video_transcription, GROQ_API_KEY)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index  # Update the stored answer right after fetching it


            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")
