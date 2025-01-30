# QuizMaster Pro

## 🎯 About QuizMaster Pro
QuizMaster Pro is an interactive web application that helps users test their comprehension of YouTube videos by generating quizzes based on video transcripts. Built using **Streamlit**, it leverages **Groq API** for question generation and **YouTube captions** for content extraction.

## 🚀 Features
- **Automatic Quiz Generation**: Paste a YouTube video URL, and the app generates a quiz based on its transcript.
- **AI-Powered Questions**: Uses Groq AI to craft meaningful multiple-choice questions.
- **User-Friendly Interface**: Built with Streamlit for smooth interactions.
- **Score Evaluation**: Get instant feedback on your quiz performance.
- **Randomized Options**: Ensures fresh and fair quiz attempts each time.

## 📜 How It Works
1. **Paste a YouTube video link** (ensure the video has English captions).
2. **Enter your Groq API Key** (obtain from [Groq Console](https://console.groq.com/docs/api-keys)).
3. Click **"Craft my quiz!"** to generate a quiz.
4. Answer the quiz and submit to see your score.
5. Review incorrect answers with explanations.

## 🛠️ Installation & Setup
### Prerequisites
- Python 3.8+
- Streamlit
- Required dependencies in `requirements.txt`

### Steps
1. **Clone the repository**
   ```sh
   git clone https://github.com/Nachiket1904/QuizMasterPro.git
   cd QuizMasterPro
   ```
2. **Create a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate  # For Windows
    ```
3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```
4. **Run the Streamlit app**
    ```sh
    streamlit run app.py
    ```

## 🏗️ Project Structure
    ```sh
    QuizMasterPro/
    │── helpers/
    │   ├── youtube_utils.py   # YouTube video ID extraction & transcript retrieval
    │   ├── groqai_utils.py    # Groq API interaction for quiz generation
    │   ├── quiz_utils.py      # Utility functions for quiz handling
    │   ├── toast_messages.py  # Random toast messages for engagement
    │── app.py                 # Main Streamlit app
    │── requirements.txt       # List of dependencies
    │── README.md              # Project documentation
    ```
## 🌍 Deployment

You can deploy this app on Streamlit Cloud, Heroku, or AWS EC2.
Ensure you securely store API keys (e.g., in environment variables).

## 🔗 Connect with the Author
👨‍💻 Nachiket Kapure - MSc in AI | AI Engineer

- [🐙 GitHub](https://github.com/Nachiket1904)

- [👔 LinkedIn](https://www.linkedin.com/in/nachiket-kapure-ml-enginner/)

## 💡 Contributing
Feel free to fork, improve, and submit pull requests!
