from google import genai
import fitz  # pymupdf
from youtube_transcript_api import YouTubeTranscriptApi

client=genai.Client(api_key="YOUR_API_KEY")

def summarize_text(text):
    prompt = f"Summarize this in 3-5 bullet points:\n{text}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def sentiment_analysis(text):
    prompt= f"Analyse the sentiment of this sentence.Say if it is Positive, Negative or Neutral and explain why in 2 lines:\n{text}"
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def chat_mode():
    conversation=client.chats.create(model="gemini-2.5-flash")
    print("Chat mode - type 'back' to move to menu")
    while True:
        user_input=input("You: ")
        if user_input.lower()=="back":
            break
        response= conversation.send_message(user_input)
        print("Bot:", response.text)

# ----------------------------
# RESUME SCREENER
# ----------------------------

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text=" ".join(page.get_text() for page in doc)
            return text
    except Exception as e1:
        print(f"Error reading PDF: {e1}")
        return None
    
def read_job_description(file_path):
    """Reads job description from a txt file"""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading job description file: {e}")
        return None
    
def screen_resume(resume_text, job_description):
    """Sends resume and job description to Gemini for scoring"""
    prompt = f"""
    You are an expert HR recruiter. Analyze this resume against the job description.
    
    Provide:
    - Match Score: X/100
    - Top 3 Strengths
    - Top 3 Weaknesses
    - Missing Skills
    - Final Verdict: Strong Match / Moderate Match / Weak Match
    
    Resume:
    {resume_text[:3000]}
    
    Job Description:
    {job_description}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None
    
def get_youtube_transcript(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        print("Invalid URL")
        return None
    ytt_api = YouTubeTranscriptApi()
    try:
        fetched = ytt_api.fetch(video_id, languages=["en"])
        return " ".join([snippet.text for snippet in fetched])
    except Exception:
        try:
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript(["en", "en-US", "en-GB", "hi"])
            fetched = transcript.fetch()
            return " ".join([snippet.text for snippet in fetched])
        except Exception as e:
            print(f"Could not fetch transcript: {e}")
            return None
        
def summarize_youtube(transcript):
    prompt = f"""
    Summarize this YouTube transcript:
    OVERVIEW: 3 sentences
    KEY POINTS: 5 bullet points
    MAIN TAKEAWAY: 1 line
    
    Transcript: {transcript[:5000]}
    """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

def main():
    print("=" * 40)
    print("        MEGA AI TOOL")
    print("=" * 40)

    while True:
        print("\n1. Summarize text")
        print("2. Sentiment analysis")
        print("3. Chat")
        print("4. YouTube summarizer")
        print("5. Resume screener")
        print("6. Quit")

        choice = input("\nChoose (1-6): ")

        if choice == "1":
            print("Paste text, press Enter twice when done:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            if not lines:
                print("Enter a valid string")
            else:
                print("\nSummary:")
                print(summarize_text("\n".join(lines)))

        elif choice == "2":
            text = input("Enter text: ")
            if not text :
                print("Enter valid sentence")
            else:
                print("\nSentiment:")
                print(sentiment_analysis(text))

        elif choice == "3":
            chat_mode()
        
        elif choice == "4":
            url = input("Paste YouTube URL: ")
            transcript = get_youtube_transcript(url)
            if transcript:
                print("\nSummary:")
                print(summarize_youtube(transcript))
            else:
                print("Could not fetch transcript")

        elif choice == "5":
            pdf_path = input("Enter path to resume PDF: ")
            resume_text = extract_text_from_pdf(pdf_path)
            if resume_text:
                jd_path = input("Enter path to job_description.txt: ")
                job_description = read_job_description(jd_path)
                print("\nAnalyzing...")
                print(screen_resume(resume_text, job_description))
            else:
                print("Could not read PDF")

        elif choice == "6":
            print("Bye!")
            break

if __name__ == "__main__":
    main()
    
