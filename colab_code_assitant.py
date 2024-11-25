import random
from groq import Groq  # Assuming you have a Python library for Groq integration.

GROQ_API_KEYS = [    ]  # add your groq keys here

def analyze_code_with_groq(code_snippet):
    """
    Analyze the given code snippet using Groq API.
    """
    try:
        # Randomly select an API key for load balancing
        groq_api = random.choice(GROQ_API_KEYS)
        client = Groq(api_key=groq_api)

        # Instruction for code analysis
        default_instruction = (
            "You are a coding assistant AI. Review the following code for errors, "
            "suggest improvements, and explain any issues clearly."
        )

        # Sending the request to Groq's chat completion API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": default_instruction},
                {"role": "user", "content": f"Analyze this code:\n{code_snippet}"},
            ],
            model="llama3-70b-8192",  # Assuming Groq supports this model
            temperature=0.5,
            stream=False,
        )

        # Retrieve and return the response
        analysis_content = chat_completion.choices[0].message.content
        return analysis_content

    except Exception as e:
        return f"Error during analysis: {str(e)}"

def main():
    print("AI-Powered Code Assistant")
    print("Analyze your code and get real-time suggestions using Groq.")
    print("=" * 50)

    while True:
        # Prompt user to input code
        code_input = input("\nPaste your code here (or type 'exit' to quit):\n")
        if code_input.strip().lower() == 'exit':
            print("Goodbye!")
            break
        elif code_input.strip():
            print("Analyzing your code... Please wait.")
            # Call the function to analyze the code
            feedback = analyze_code_with_groq(code_input)
            print("\nFeedback and Suggestions:")
            print("=" * 50)
            print(feedback)
        else:
            print("Please provide valid code input before analysis.")

if __name__ == "__main__":
    main()
