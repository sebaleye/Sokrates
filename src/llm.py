import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig
import uuid
import re
from openai import OpenAI

def clean_response(text):
    """
    Removes <think> tags and other internal monologue artifacts from the response.
    Also handles the '>>>' delimiter for strict output control.
    """
    if not text:
        return ""
        
    # 1. Remove <think>...</think> blocks (including newlines)
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # 2. check for explicit output delimiter '>>>'
    if ">>>" in cleaned:
        parts = cleaned.split(">>>")
        # return the last part (the actual output)
        cleaned = parts[-1]
        
    # 3. remove leading/trailing quotes and common prefixes
    cleaned = cleaned.strip().strip('"').strip("'")
    
    # remove "Question:" prefix if present (case insensitive)
    if cleaned.lower().startswith("question:"):
        cleaned = cleaned[9:].strip()
        
    # remove markdown italics/bold wrappers if they wrap the whole string
    if cleaned.startswith("*") and cleaned.endswith("*"):
        cleaned = cleaned.strip("*")
    if cleaned.startswith("_") and cleaned.endswith("_"):
        cleaned = cleaned.strip("_")
        
    return cleaned.strip()

def clean_json_string(json_str):
    """
    Attempts to clean and repair a JSON string.
    """
    if not json_str:
        return ""
        
    # remove markdown code blocks
    json_str = re.sub(r'```json', '', json_str)
    json_str = re.sub(r'```', '', json_str)
    
    # attempt to fix common missing bracket errors
    # case: "core_patterns": [ ... }, "anti_patterns" (missing closing ])
    # we look for }, "key" where the previous structure implies a list
    # this is a heuristic fix for the specific error observed
    if '}, "anti_patterns"' in json_str and '}], "anti_patterns"' not in json_str:
        json_str = json_str.replace('}, "anti_patterns"', '}], "anti_patterns"')
        
    return json_str.strip()

def get_interaction_response(
    user_input, 
    system_instruction=None, 
    model_name="gemini-2.5-flash", 
    previous_interaction_id=None
):
    """
    Wrapper for LLM API interactions.
    
    Args:
        user_input (str): The text input from the user.
        system_instruction (str, optional): System instructions (only used for new interactions).
        model_name (str): Model to use.
        previous_interaction_id (str, optional): ID to continue a conversation.
        
    Returns:
        tuple: (response_text, interaction_id)
    """
    
    # check for provider configuration (default to google if not set)
    provider = st.secrets.get("LLM_PROVIDER", "google")
    
    if provider == "local":
        return _get_local_response(user_input, system_instruction, previous_interaction_id)
    
    # --- cloud provider implementation ---
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("GEMINI_API_KEY not found in secrets.toml")
        return "Error: API Key missing.", None

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    config = {
        "model": model_name,
        "input": user_input,
    }
    
    # if continuing a conversation, use the ID
    if previous_interaction_id:
        config["previous_interaction_id"] = previous_interaction_id
    # if starting a new one, we can add system instructions
    elif system_instruction:
        # note: for the interactions API, system instructions are often best passed 
        # as the initial context or prepended to the first input if the specific 
        # model/endpoint doesn't support a separate 'system_instruction' param 
        # in the create() call directly. 
        # however, the Client usually handles config. Let's check if we can pass it in config.
        # the docs show simple input. We will prepend it to be safe and explicit.
        config["input"] = f"SYSTEM INSTRUCTION:\n{system_instruction}\n\nUSER INPUT:\n{user_input}"

    try:
        interaction = client.interactions.create(**config)
        
        # get text from the last output
        response_text = interaction.outputs[-1].text
        return clean_response(response_text), interaction.id
        
    except Exception as e:
        return f"Error generating response: {str(e)}", None

def _get_local_response(user_input, system_instruction, previous_interaction_id):
    """
    Handles interaction with a local LLM (e.g., LM Studio) mimicking the Interaction API state.
    """
    # initialize local storage if needed
    if "local_interactions" not in st.session_state:
        st.session_state.local_interactions = {}
        
    # determine interaction ID
    interaction_id = previous_interaction_id
    if not interaction_id:
        interaction_id = str(uuid.uuid4())
        st.session_state.local_interactions[interaction_id] = []
        # add system instruction if new
        if system_instruction:
            st.session_state.local_interactions[interaction_id].append({
                "role": "system", 
                "content": system_instruction
            })
            
    # retrieve history
    messages = list(st.session_state.local_interactions[interaction_id])
    
    # add user input
    messages.append({"role": "user", "content": user_input})
    
    # call local LLM
    try:
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        
        completion = client.chat.completions.create(
            model="local-model", # uses loaded model
            messages=messages,
            temperature=0.7
        )
        
        response_text = completion.choices[0].message.content
        cleaned_text = clean_response(response_text)
        
        # append assistant response to history
        messages.append({"role": "assistant", "content": cleaned_text})
        
        # update state
        st.session_state.local_interactions[interaction_id] = messages
        
        return cleaned_text, interaction_id
        
    except Exception as e:
        return f"Error connecting to Local LLM: {str(e)}", None

