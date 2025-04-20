import os
import random
import requests
import json
import re
from dotenv import load_dotenv
from prompt_templates import PROMPT_PRESETS
from config import NUM_SENTENCES

load_dotenv()

# LM Studio API settings
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"  # Default port
MODEL_NAME = "llama2-13b-psyfighter2"  # Use your model's identifier

def extract_insult_lines(content):
    # First, try to extract numbered lines
    lines = []
    raw_lines = content.split("\n")
    
    for line in raw_lines:
        # Look for numbered lines (with or without quotes)
        line = line.strip()
        if re.match(r'^\d+\.', line):
            # Extract everything after the number and period
            insult = re.sub(r'^\d+\.\s*', '', line)
            # Remove quotes if present (optional)
            insult = insult.strip('"\'')
            if insult:
                lines.append(insult)
    
    # If no numbered lines found, split the paragraph into sentences
    if not lines and content:
        # Split by sentence-ending punctuation
        sentences = re.split(r'(?<=[.!?])\s+', content)
        # Filter out empty sentences and take up to NUM_SENTENCES
        lines = [s.strip() for s in sentences if s.strip()]
        lines = lines[:NUM_SENTENCES]
    
    return lines[:NUM_SENTENCES]

def generate_insults(language):
    prompt = random.choice(PROMPT_PRESETS[language])

    # LM Studio uses OpenAI-compatible format
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "max_tokens": 800
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Sending request to LM Studio at {LM_STUDIO_API_URL}")
        response = requests.post(LM_STUDIO_API_URL, headers=headers, json=payload)
        
        print(">> Response status:", response.status_code)
        print(">> Raw response text:\n", response.text)

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(">> Extracted content:\n", content)
        lines = extract_insult_lines(content)
        
        # If no lines were extracted, try to get at least something
        if not lines and content:
            # Split by newlines and take maximum 5 lines
            simple_lines = [line.strip() for line in content.split("\n") if line.strip()]
            lines = simple_lines[:NUM_SENTENCES]
        
        return lines

    except Exception as e:
        print("❌ Failed to parse response:", e)
        if 'response' in locals():
            print("→ HTTP Status:", response.status_code)
            print("→ Raw Body:", response.text)
        else:
            print("→ No response received")
        return ["[AI Error] Unable to generate insults."]