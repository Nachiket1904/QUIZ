import streamlit as st  # Streamlit library for building web apps
from helpers.youtube_utils import extract_video_id_from_url, get_transcript_text  # YouTube-related utilities
from helpers.groqai_utils import retrieve_quiz_data  # Function to retrieve quiz data using Groq API
from helpers.quiz_utils import convert_string_to_list, get_shuffled_options  # Utility for handling quiz questions and randomizing options
from helpers.toast_messages import generate_random_toast_message  # Utility to generate random toast messages

# Set up basic configuration for the web app, including page title and layout
st.set_page_config(
    page_title="QuizMaster Pro",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Display a toast message for new users based on session state
if 'first_time' not in st.session_state:
    message, icon = generate_random_toast_message()  # Fetch a random toast message
    st.toast(message, icon=icon)  # Show the toast notification
    st.session_state.first_time = False  # Mark the user as not new

# Sidebar information about the author and external links
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

# Main app title and description
st.title(":red[QuizMaster] — Watch. Learn. Quiz. 🧠", anchor=False)
st.write("""
Ever watched a YouTube video and wondered how well you understood its content? Here's a fun twist: Instead of just watching on YouTube, come to **QuizMaster** and test your comprehension!

**How does it work?** 🤔
1. Paste the YouTube video URL of your recently watched video.
2. Enter your [Groq API Key](https://console.groq.com/docs/api-keys).

⚠️ Important: The video **must** have English captions for the tool to work.

Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test! 
""")

# Form to accept YouTube video link and Groq API key from the user
with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Enter the YouTube video link:", value="")
    GROQ_API_KEY = st.text_input("Enter your Groq API Key:", placeholder="sk-XXXX", type='password')
    submitted = st.form_submit_button("Craft my quiz!")

# Handle form submission and quiz generation
if submitted or ('quiz_data_list' in st.session_state):
    if not YOUTUBE_URL:
        st.info("Please provide a valid YouTube video link. Head over to [YouTube](https://www.youtube.com/) to fetch one.")
        st.stop()
    elif not GROQ_API_KEY:
        st.info("Please fill out the Groq API Key to proceed. If you don't have one, you can obtain it [here](https://console.groq.com/docs/api-keys).")
        st.stop()
        
    # Generate quiz using video transcription and Groq API
    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            video_id = extract_video_id_from_url(YOUTUBE_URL)  # Extract video ID from URL
            video_transcription = get_transcript_text(video_id)  # Fetch video transcription
            quiz_data_str = retrieve_quiz_data(video_transcription, GROQ_API_KEY)  # Fetch quiz data using API key
            st.session_state.quiz_data_list = convert_string_to_list(quiz_data_str)  # Convert string to list for processing

            # Initialize session state variables if not already present
            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            # Randomize the options and store the correct answers
            for question in st.session_state.quiz_data_list:
                options, correct_answer = get_shuffled_options(question[1:])  # Randomize answer options
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        # Display the quiz and handle user answers
        with st.form(key='quiz_form'):
            st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
            for i, question in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(question[0], options, index=default_index)  # Display quiz question with answer options
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index  # Store user's answer

            # Submit the quiz and display the score
            results_submitted = st.form_submit_button(label='Unveil My Score!')
            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                # Show balloons and feedback based on the score
                if score == len(st.session_state.quiz_data_list):
                    st.balloons()  # Celebrate perfect score
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                # Review incorrect answers
                for i, (ua, ca, question, options) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if options[ua] != ca:
                            st.info(f"Question: {question[0]}")
                            st.error(f"Your answer: {options[ua]}")
                            st.success(f"Correct answer: {ca}")
