import streamlit as st
import json
import re
from src.llm import get_interaction_response, clean_json_string
from src.generator import generate_anti_portfolio_html
from src.utils import extract_text_from_pdf, extract_text_from_url
from src.prompts import (
    SYSTEM_PROMPT_ARCHIVIST,
    SYSTEM_PROMPT_CRITIC,
    SYSTEM_PROMPT_DIRECTOR,
    SYSTEM_PROMPT_SOKRATES,
    SYSTEM_PROMPT_EXTRACTOR,
    SYSTEM_PROMPT_TRAJECTORY_PREDICTOR
)
from src.github_analyzer import GitHubAnalyzer, get_github_analysis_prompt
from src.maieutic_questions import get_phase_questions, generate_adaptive_question
from src.multi_source_analyzer import MultiSourceAnalyzer, get_multi_source_analysis_prompt

# setup & configuration
st.set_page_config(page_title="SOKRATES", layout="wide")

# custom CSS for the "Anti-Portfolio" aesthetic
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    h1 { font-family: 'Courier New', monospace; letter-spacing: -2px; }
    .stChatMessage { border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = "onboarding" # onboarding -> processing -> interviewing -> generating -> complete
if "user_context" not in st.session_state:
    st.session_state.user_context = ""
if "patterns" not in st.session_state:
    st.session_state.patterns = {}
if "analysis_facts" not in st.session_state:
    st.session_state.analysis_facts = ""
if "analysis_tensions" not in st.session_state:
    st.session_state.analysis_tensions = ""
if "sokrates_interaction_id" not in st.session_state:
    st.session_state.sokrates_interaction_id = None
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "github_data" not in st.session_state:
    st.session_state.github_data = None
if "github_analysis" not in st.session_state:
    st.session_state.github_analysis = None
if "multi_source_data" not in st.session_state:
    st.session_state.multi_source_data = None
if "multi_source_analysis" not in st.session_state:
    st.session_state.multi_source_analysis = None

# app interface flow

st.title("S O K R A T E S")
st.markdown("### The Anti-Portfolio Generator")

# step 1: onboarding (the "mindset reset")
if st.session_state.step == "onboarding":
    st.markdown("""
    **This is not a CV generator.** We are not looking for your job titles. We are looking for your *trajectory*.
    
    Provide your raw background to begin the search.
    """)
    
    col1, col2 = st.columns(2)

    with col1:
        uploaded_files = st.file_uploader("Upload Documents (CV, LinkedIn PDF)", type=['pdf', 'txt'], accept_multiple_files=True)
        urls_input = st.text_area("External Links (GitHub, Personal Site) - One per line", height=100)
        github_username = st.text_input("GitHub Username (Optional - enables learning velocity analysis)")

    with col2:
        raw_input = st.text_area("Brain Dump / Bio / Notes", height=300)
    
    if st.button("Initialize Sokrates"):
        combined_context = ""

        # Process GitHub Analysis (Optional but powerful)
        if github_username:
            with st.spinner(f"Analyzing GitHub activity for @{github_username}..."):
                try:
                    analyzer = GitHubAnalyzer()
                    github_data = analyzer.analyze_user(github_username)
                    if github_data:
                        st.session_state.github_data = github_data
                        combined_context += f"\n--- GITHUB ANALYSIS ---\n"
                        combined_context += f"Repositories: {len(github_data['project_complexity'])}\n"
                        combined_context += f"Languages: {', '.join([lang['language'] for lang in github_data['language_evolution'][:5]])}\n"
                        combined_context += f"Learning Pattern Signals Detected\n"
                        st.success(f"✓ GitHub analysis complete - {len(github_data['commit_timeline'])} data points extracted")
                    else:
                        st.warning(f"Could not analyze GitHub user @{github_username}")
                except Exception as e:
                    st.warning(f"GitHub analysis skipped: {str(e)}")

        # Process Files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(uploaded_file)
                    combined_context += f"\n--- FILE: {uploaded_file.name} ---\n{text}\n"
                else: # txt
                    text = str(uploaded_file.read(), "utf-8")
                    combined_context += f"\n--- FILE: {uploaded_file.name} ---\n{text}\n"

        # Process URLs
        if urls_input:
            urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
            for url in urls:
                with st.spinner(f"Fetching {url}..."):
                    text = extract_text_from_url(url)
                    combined_context += text

        # Process Raw Input
        if raw_input:
            combined_context += f"\n--- USER NOTES ---\n{raw_input}\n"

        if combined_context:
            st.session_state.user_context = combined_context
            st.session_state.step = "processing"
            st.rerun()
        else:
            st.warning("Please provide some input (File, URL, or Text) to proceed.")

# step 1.5: processing (archivist & critic)
elif st.session_state.step == "processing":
    with st.status("Analyzing your professional DNA...", expanded=True) as status:

        # NEW: Multi-source data extraction
        st.write("Extracting structured data from all sources...")
        multi_analyzer = MultiSourceAnalyzer()
        multi_source_data = multi_analyzer.analyze_text(st.session_state.user_context)
        st.session_state.multi_source_data = multi_source_data

        # Show what was found
        skills_found = multi_source_data['skills']['total_unique_skills']
        projects_found = multi_source_data['projects']['total']
        timeline_years = multi_source_data['timeline']['span']['total_years']
        st.write(f"✓ Found: {skills_found} skills, {projects_found} projects, {timeline_years} year timeline")

        # agent 1: the archivist
        st.write("Archivist is separating facts from narrative...")

        # Enhanced context with structured data
        enhanced_context = f"""
USER CONTENT:
{st.session_state.user_context}

STRUCTURED DATA EXTRACTED:
- Timeline: {timeline_years} years of professional activity
- Skills: {skills_found} unique skills across {len(multi_source_data['skills']['by_category'])} categories
- Projects: {projects_found} projects identified
- Education: {len(multi_source_data['education']['formal'])} formal degrees, {len(multi_source_data['education']['certifications'])} certifications
- Learning Signals: {multi_source_data['learning_signals']['total']} growth indicators found
- Career Progression: {multi_source_data['career_progression']['progression_detected']}

Now extract the key FACTS from the content above.
        """

        facts, _ = get_interaction_response(
            user_input=enhanced_context,
            system_instruction=SYSTEM_PROMPT_ARCHIVIST
        )
        st.session_state.analysis_facts = facts
        st.write("Facts extracted.")

        # agent 2: the silent critic
        st.write("Silent Critic is identifying tensions...")

        # Enhanced tensions analysis with structured data
        tensions_context = f"""
FACTS:
{facts}

DATA PATTERNS DETECTED:
- Skill diversity: {multi_source_data['learning_velocity_indicators'].get('skill_diversity', {}).get('breadth_score', 'N/A')}% breadth
- Average project complexity: {multi_source_data['projects'].get('complexity_distribution', {}).get('average', 'N/A')}
- Learning signals: {multi_source_data['learning_signals']['by_type']}
- Career progression: {multi_source_data['career_progression']['progression_detected']}

Identify tensions and unanswered questions.
        """

        tensions, _ = get_interaction_response(
            user_input=tensions_context,
            system_instruction=SYSTEM_PROMPT_CRITIC
        )
        st.session_state.analysis_tensions = tensions
        st.write("Tensions identified.")

        status.update(label="Analysis Complete", state="complete", expanded=False)
    
    # prepare sokrates context
    initial_context = f"""
    USER CONTEXT:
    {st.session_state.user_context}
    
    ARCHIVIST REPORT (FACTS):
    {st.session_state.analysis_facts}
    
    SILENT CRITIC REPORT (TENSIONS):
    {st.session_state.analysis_tensions}
    
    Start the interview now.
    """
    
    with st.spinner("Summoning Sokrates..."):
        # first sokrates message (initializes the interaction ID)
        intro_msg, interaction_id = get_interaction_response(
            user_input=initial_context, 
            system_instruction=SYSTEM_PROMPT_SOKRATES
        )
    
    # Fallback if empty response (local model issue)
    if not intro_msg or not intro_msg.strip():
        intro_msg = "I have analyzed your background. Shall we begin?"
    
    # save the ID for the conversation loop
    st.session_state.sokrates_interaction_id = interaction_id
    
    # save to UI history
    st.session_state.messages.append({"role": "assistant", "content": intro_msg})
    
    st.session_state.step = "interviewing"
    st.rerun()

# step 2: the maieutic conversation
elif st.session_state.step == "interviewing":
    
    # distinct visual container for the chat
    chat_container = st.container()
    
    # display chat history
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
    
    # user input
    if prompt := st.chat_input("Your answer..."):
        # add user message to UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # generate AI response using the interaction ID
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Determine Phase
            st.session_state.turn_count += 1
            turn = st.session_state.turn_count
            
            # HARD STOP at Turn 3 (Accelerated Mode)
            if turn >= 3:
                st.session_state.step = "generating"
                st.rerun()
            
            # --- DIRECTOR AGENT STEP ---
            # The Director decides WHAT to ask based on the history
            transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-4:]]) # Last few turns
            
            # Define Phase for Director
            if turn == 1:
                phase_context = "PHASE 1: ORIGINS. We need to know WHY they do what they do."
            elif turn == 2:
                phase_context = "PHASE 2: PROCESS. We need to know HOW they work (chaos vs structure)."
            else:
                phase_context = "PHASE 3: POTENTIAL. Test their limits with a hypothetical scenario."

            director_input = f"""
            CURRENT PHASE: {phase_context} (Turn {turn}/3)
            TENSIONS: {st.session_state.analysis_tensions}
            
            RECENT HISTORY:
            {transcript}
            
            USER JUST SAID: "{prompt}"
            
            Decide the next question directive.
            """
            
            # Combined spinner for both Director and Sokrates
            with st.spinner("Thinking..."):
                directive, _ = get_interaction_response(
                    user_input=director_input,
                    system_instruction=SYSTEM_PROMPT_DIRECTOR
                )

                # --- SOKRATES EXECUTION STEP ---
                # Sokrates phrases the question
                sokrates_input = f"""
                DIRECTIVE FROM DIRECTOR:
                {directive}

                USER ANSWER: {prompt}
                """

                full_response, new_id = get_interaction_response(
                    user_input=sokrates_input,
                    previous_interaction_id=st.session_state.sokrates_interaction_id
                )

                # Fallback for empty response
                if not full_response or not full_response.strip():
                    full_response = "..."

            # Write response after spinner completes
            response_placeholder.write(full_response)
            
            # update the ID (though it usually stays the same for the same session, good practice to update)
            if new_id:
                st.session_state.sokrates_interaction_id = new_id
            
            if "[ANALYSIS COMPLETE]" in full_response:
                st.session_state.step = "generating"
                st.rerun()
            else:
                # response_placeholder.write(full_response) # Removed duplicate write
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# step 3: the anti-portfolio reveal
elif st.session_state.step == "generating":
    # Show the conversation history in a subtle way during analysis
    st.markdown("### 💭 Analyzing Your Responses")

    with st.expander("Your Interview Transcript", expanded=False):
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**You**: {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"*Sokrates*: {msg['content']}")

    # Progress bar for analysis
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Compile transcript from history
    transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages if m['role'] != 'system'])

    progress_bar.progress(10)
    status_text.text("Analyzing interview patterns...")

    # Analyze GitHub data if available
    github_analysis_text = ""
    if st.session_state.github_data:
        progress_bar.progress(30)
        status_text.text("Analyzing GitHub learning velocity...")
        github_prompt = get_github_analysis_prompt(st.session_state.github_data)
        github_analysis, _ = get_interaction_response(
            user_input=github_prompt,
            system_instruction="You are a data analyst. Extract learning patterns from GitHub data and return valid JSON only."
        )
        st.session_state.github_analysis = github_analysis
        github_analysis_text = f"\n\nGITHUB LEARNING VELOCITY ANALYSIS:\n{github_analysis}\n"

    # Analyze multi-source data (CVs, portfolios, etc.)
    multi_source_analysis_text = ""
    if st.session_state.multi_source_data:
        progress_bar.progress(50)
        status_text.text("Analyzing professional background patterns...")
        multi_source_prompt = get_multi_source_analysis_prompt(st.session_state.multi_source_data)
        multi_source_analysis, _ = get_interaction_response(
            user_input=multi_source_prompt,
            system_instruction="You are a data analyst. Extract learning patterns from professional background data and return valid JSON only."
        )
        st.session_state.multi_source_analysis = multi_source_analysis
        multi_source_analysis_text = f"\n\nPROFESSIONAL BACKGROUND ANALYSIS:\n{multi_source_analysis}\n"

    # Combine ALL data sources for comprehensive extraction
    progress_bar.progress(70)
    status_text.text("Extracting cognitive patterns and predictions...")

    full_context = f"""Here is the interview transcript:

{transcript}
{github_analysis_text}
{multi_source_analysis_text}

INSTRUCTIONS:
- Extract cognitive patterns from the interview
- If GitHub analysis is present, integrate those learning velocity insights
- If professional background analysis is present, integrate those career trajectory insights
- Combine ALL available evidence for the most accurate predictions
- Predict future growth trajectory based on ALL available evidence
- Be specific with time estimates for learning new skills
- Identify the high-leverage gap that would unlock next-level growth
- Cross-reference insights from different data sources to validate patterns
"""

    # Start FRESH interaction for analysis (disconnecting from Sokrates persona)
    extraction, _ = get_interaction_response(
        user_input=full_context,
        system_instruction=SYSTEM_PROMPT_EXTRACTOR
    )

    progress_bar.progress(90)
    status_text.text("Finalizing analysis...")

    # clean JSON (mocking a parser for stability)
    try:
        # Use regex to find the JSON object within the text
        json_match = re.search(r'\{.*\}', extraction, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            # Apply additional cleaning/repair
            clean_json = clean_json_string(clean_json)

            data = json.loads(clean_json)
            st.session_state.patterns = data

            progress_bar.progress(100)
            status_text.text("Complete!")

            st.session_state.step = "complete"
            st.rerun()
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Complex pattern detected. Raw output (Error: {str(e)}):")
        st.write(extraction)

# step 4: final display (the deliverable) - ULTRA MINIMAL
elif st.session_state.step == "complete":
    data = st.session_state.patterns

    st.balloons()

    # Absolute minimal presentation - just download
    st.markdown("<div style='text-align: center; padding: 4rem 0;'>", unsafe_allow_html=True)

    st.title("✨ Analysis Complete")
    st.markdown("### Your Anti-Portfolio is ready")
    st.markdown("---")

    # Single centered download button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        html_content = generate_anti_portfolio_html(data)
        st.download_button(
            "📥 Download Your Anti-Portfolio",
            data=html_content,
            file_name="anti_portfolio.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )

        st.markdown("")
        st.caption("Open the HTML file in your browser to view your complete analysis")

        st.markdown("---")

        if st.button("🔄 Start New Analysis", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)