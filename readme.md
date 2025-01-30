QuizMaster Pro

🎯 About QuizMaster Pro

QuizMaster Pro is an interactive web application that helps users test their comprehension of YouTube videos by generating quizzes based on video transcripts. Built using Streamlit, it leverages Groq API for question generation and YouTube captions for content extraction.

🚀 Features

Automatic Quiz Generation: Paste a YouTube video URL, and the app generates a quiz based on its transcript.

AI-Powered Questions: Uses Groq AI to craft meaningful multiple-choice questions.

User-Friendly Interface: Built with Streamlit for smooth interactions.

Score Evaluation: Get instant feedback on your quiz performance.

Randomized Options: Ensures fresh and fair quiz attempts each time.

📜 How It Works

Paste a YouTube video link (ensure the video has English captions).

Enter your Groq API Key (obtain from Groq Console).

Click "Craft my quiz!" to generate a quiz.

Answer the quiz and submit to see your score.

Review incorrect answers with explanations.

🛠️ Installation & Setup

Prerequisites

Python 3.8+

Streamlit

Required dependencies in requirements.txt

Steps

Clone the repository

git clone https://github.com/Nachiket1904/QuizMasterPro.git
cd QuizMasterPro

Create a virtual environment

python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows

Install dependencies

pip install -r requirements.txt

Run the Streamlit app

streamlit run app.py

🏗️ Project Structure

QuizMasterPro/
│── helpers/
│   ├── youtube_utils.py   # YouTube video ID extraction & transcript retrieval
│   ├── groqai_utils.py    # Groq API interaction for quiz generation
│   ├── quiz_utils.py      # Utility functions for quiz handling
│   ├── toast_messages.py  # Random toast messages for engagement
│── app.py                 # Main Streamlit app
│── requirements.txt       # List of dependencies
│── README.md              # Project documentation

🌍 Deployment

You can deploy this app on Streamlit Cloud, Heroku, or AWS EC2.

Ensure you securely store API keys (e.g., in environment variables).

🔗 Connect with the Author

👨‍💻 Nachiket Kapure - MSc in AI | AI Engineer

🐙 GitHub

👔 LinkedIn

🌐 Portfolio

💡 Contributing

Feel free to fork, improve, and submit pull requests!

📜 License

This project is licensed under the MIT License.
