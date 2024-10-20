import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present
if not api_key:
    raise ValueError("API Key not found in .env file")

# Configure the API key for the model
genai.configure(api_key=api_key)

# Function to call the Gemini API
def call_gemini(prompt, system_instruction):
    """
    Function to make a structured API call to the Gemini model.
    
    Args:
    - prompt (str): The user prompt for generating content.
    - system_instruction (str): The system instruction to guide the model.

    Returns:
    - str: The content generated by the model.
    """
    full_prompt = f"{system_instruction}\n\n{prompt}"
    
    # Use the 'generate_content' method for generating text
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(full_prompt)
   
    return response.text.strip()
    

# Function to summarize text
def summarize_text(input):
    summary_prompt = f"Summarize the following text without any markdown formating:\n\n{input}"
    system_instruction = "You are an expert at summarizing transcripts."
    return call_gemini(summary_prompt, system_instruction)

# Function to generate quiz questions based on summary
 #output question in a list of python dictionary
def generate_quiz_questions(summary):
    question_prompt = f"Generate three quiz questions based on the following summary, only add '(correct)' behind correct choice:\n\n{summary}"
    system_instruction = "You are an expert in generating quiz questions from summarized content."
    return call_gemini(question_prompt, system_instruction)


def api_summarize(text_input):
    """
    API call to get the summary of the input text.
    """
    
    summary = summarize_text(text_input)
    return summary

# API 2: Quiz Generation API Call
def api_generate_quiz(summary):
    """
    API call to generate quiz questions based on the provided summary.
    """
    raw_quiz_questions = generate_quiz_questions(summary)
    quiz_questions = []
    questions = raw_quiz_questions.strip().split('\n\n')  # Split by double newlines to separate questions
    

    for question_block in questions[1: ]:
        lines = question_block.strip().split('\n')
        
        # Extract the question text (first line of the block)
        question_text = lines[0].strip()
        # Extract the choices (subsequent lines in the block)
        choices = []
        for line in lines[1:]:
            choice_text = line.strip()
            correct = '(correct)' in choice_text  # Mark the answer as correct if "(correct)" is found
             # Add the choice to the list
            choices.append({
                'text': choice_text.replace(' (correct)', '').split(') ')[1].strip(),  # Strip "a)", "b)", etc.
                'correct': correct
            })

         # Append the structured question with its choices to the quiz_questions list
        quiz_questions.append({
            'question': question_text,
            'choices': choices
        })
    return quiz_questions




# Example usage
if __name__ == '__main__':
    # Example text input (replace this with your own text)
    text_input = "According to the Olympic Foundation for Culture and Heritage, the U.S. leds the all-time medal count going into the Paris Games with a total of 2,975 Olympic medals, followed by the now-defunct Soviet Union, with 1,204 medals, and Germany, with 1,058 medals. And, as hoped, the U.S. added to its medal haul at the 2024 Games, topping 3,000 total medals within the first week of competition. The American team is helped by the sheer number of competitors representing Team USA at the Paris Games: 594 athletes, of the about 10,500 athletes competing. Four countries in this year's games have only one athlete taking a shot at medal glory: Belize, Liechtenstein, Nauru and Somalia. And since Russia was banned for this year's games, any medals garnered by its few athletes competing as individual neutral athletes won't be tallied as part of the country's overall haul. The first individual neutral athlete to medal in the Games was Viyaleta Bardzilouskaya of Belarus, who took silver in women's trampoline."
    summary = api_summarize(text_input)
    quiz_questions = api_generate_quiz(summary)


    #output question in a list of python dictionary