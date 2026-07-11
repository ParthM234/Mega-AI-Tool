# Mega AI Tool

## What this project does
An all-in-one AI powered CLI tool built with Google Gemini API.
Combines 5 different AI features into a single menu-driven application.

## Features
1. **Text Summarizer** — condenses any text into key bullet points
2. **Sentiment Analysis** — analyzes tone and emotion of text
3. **Chat** — conversational AI with memory across messages
4. **YouTube Summarizer** — fetches video transcripts and summarizes them
5. **Resume Screener** — scores resume match against a job description

## How to run
1. Clone the repo
2. Install libraries: pip install google-genai youtube-transcript-api pymupdf
3. Get a free Gemini API key from aistudio.google.com
4. Add your API key in the code
5. Run `python mega_ai_tool.py`
6. Choose a feature from the menu (1-6)

## Requirements for specific features
- YouTube Summarizer needs a video with subtitles available
- Resume Screener needs a resume PDF and a job_description.txt file

## Libraries used
- google-genai
- youtube-transcript-api
- pymupdf

## Built with
- Python
- Google Gemini 2.5 Flash API

## Why I built this
Built as part of a self-directed summer learning program covering
data analysis, machine learning, and AI API integration. This project
consolidates everything into one practical tool.