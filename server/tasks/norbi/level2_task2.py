from fastapi import APIRouter, Request, Response
import re

router = APIRouter(prefix="/level2/task2")

# Global State: Stores the vocabulary learned so far
vocabulary = {}

@router.post("")
async def solve_task(request: Request):
    # Extract Hint from Headers
    # Header format: "... here you have 1 word from the new language: food=fi"
    task_desc = request.headers.get('task-description', '')
    
    # Use Regex to find the "word=translation" pattern
    # Looking for alphabetic characters, an equals sign, and alphabetic characters
    match = re.search(r'(\w+)=(\w+)', task_desc)
    
    if match:
        english_word = match.group(1)
        alien_word = match.group(2)
        
        # Update the global dictionary
        vocabulary[english_word] = alien_word
        print(f"[LEARNED] {english_word} -> {alien_word}")

    # Read Query from Body
    # The body contains the word we need to translate right now
    target_word = (await request.body()).decode('utf-8').strip()

    # Translate
    translated_word = vocabulary.get(target_word)

    if translated_word:
        return Response(content=translated_word, media_type="text/plain")
    else:
        # If the word hasn't been learned yet, we might return the original
        # or an empty string. Based on the logs, you likely accumulate 
        # knowledge over many retries or continuous requests.
        return Response(content="", media_type="text/plain")
