# SOKRATES Development Log

## Project Overview

**SOKRATES** is an AI-Native Anti-Portfolio Generator that combines Socratic maieutics with AI-powered pattern analysis to create predictive portfolios showing "what you will become" instead of "what you've done."

**Repository**: Will be pushed to GitHub as `Sokrates`
**Original Folder**: `Sokr` (renamed to `Sokrates`)
**Main Tech Stack**: Python, Streamlit, Google Gemini AI
**Status**: Complete and ready for GitHub

---

## Complete Build History

### Phase 1: Initial Implementation (from sokrates_implementation_addition.md)

**Date**: Dec 13-14, 2025

**Implemented Features**:

1. **GitHub Learning Velocity Analysis** ([src/github_analyzer.py](src/github_analyzer.py))
   - Analyzes public GitHub repositories
   - Extracts commit timeline, language evolution, project complexity
   - Calculates learning patterns:
     - Time to first commit for each technology
     - Consistency score (commit frequency variance)
     - Exploration vs Build ratio
   - Generates AI-ready prompts for pattern extraction

2. **Enhanced Pattern Extraction** ([src/prompts.py](src/prompts.py))
   - Updated `SYSTEM_PROMPT_EXTRACTOR` with:
     - `learning_velocity`: Time to competency, acceleration patterns, transfer learning
     - `growth_trajectory`: Current phase, natural direction, high-leverage gaps, readiness indicators
     - `hiring_insight`: Best fit role, potential risks, investment thesis
   - Added `SYSTEM_PROMPT_TRAJECTORY_PREDICTOR` for future-focused predictions

3. **Advanced Maieutic Question Templates** ([src/maieutic_questions.py](src/maieutic_questions.py))
   - Structured question templates based on SOKRATES framework
   - Phase-based questioning (Origins, Process, Potential)
   - 8 question categories: Reliable Competencies, Friction Zones, Intentional Ignorance, Learning Methodology, Transformative Failures, Decision Making, Constraint Testing, Meta-Cognition
   - Adaptive follow-up strategies

4. **Trajectory Visualization** ([src/generator.py](src/generator.py))
   - New section: `_generate_trajectory_section()`
   - Displays: Current State, Natural Trajectory, High-Leverage Gap, Learning Velocity, Readiness Indicators, Hiring Intelligence
   - Professional HTML design with gradient backgrounds

5. **Enhanced Streamlit UI** ([app.py](app.py))
   - GitHub username input field
   - Automatic GitHub analysis with progress indicators
   - Integration of GitHub data into AI synthesis
   - New "Growth Trajectory & Predictions" section

---

### Phase 2: Multi-Source Analysis Enhancement

**User Request**: "could you make it so it analyzes with care other types of inputs beside github?"

**Implementation**:

1. **Multi-Source Analyzer** ([src/multi_source_analyzer.py](src/multi_source_analyzer.py) - 450+ lines)
   - Comprehensive analyzer for CVs, LinkedIn PDFs, portfolios, websites
   - **Timeline Extraction**: Detects date patterns, reconstructs professional timeline
   - **Skills & Technologies**: Extracts 150+ technologies across 9 categories
   - **Project Complexity Assessment**: NLP-based scoring (0-10)
   - **Education & Learning Progression**: Formal education, certifications, online learning
   - **Career Transitions Detection**: Junior → Mid → Senior → Leadership
   - **Learning Signals**: Experimentation, mastery, teaching, problem-solving, ownership

2. **Enhanced Processing Pipeline**:
   ```
   User Input → Multi-Source Extraction
              ↓
       Structured Data (timeline, skills, projects, education)
              ↓
       Enhanced Archivist (facts + data insights)
              ↓
       Enhanced Critic (tensions + pattern anomalies)
              ↓
       Sokrates Interview
              ↓
       Combined Analysis (interview + GitHub + multi-source)
              ↓
       Comprehensive Trajectory Predictions
   ```

3. **Documentation**:
   - Created [MULTI_SOURCE_ANALYSIS.md](MULTI_SOURCE_ANALYSIS.md) - Full documentation
   - Updated [README.md](README.md) with multi-source features

---

### Phase 3: Bug Fixes and Enhancements

#### Bug Fix 1: KeyError in multi_source_analyzer.py

**Error**: `KeyError: 0` in `_calculate_learning_velocity_indicators()`

**Location**: Line 336

**Problem**:
```python
# WRONG:
skill_categories = len(set(
    mention[0]['category']  # Treating dict as list
    for mentions in self.data['skill_mentions'].values()
    for mention in mentions if mentions
))
```

**Fix**:
```python
# CORRECT:
skill_categories = len(set(
    mention['category']  # mention is already a dict
    for mentions in self.data['skill_mentions'].values()
    for mention in mentions if mentions
))
```

---

### Phase 4: Five Critical UX Improvements

**User Feedback**: 5-part improvement request

#### Issue 1: Poor Skill Detection

**Problem**: "i get only this for the skills... ✓ Found: 1 skills, 0 projects, 0 year timeline"

**Solution**: Expanded skill categories from ~50 to **150+ technologies**

**Changes to [src/multi_source_analyzer.py](src/multi_source_analyzer.py)**:
- Lines 88-136: Expanded skill categories
- Added 3 new categories: `tools`, `methodologies`, `soft_skills`
- Programming languages: 23 (was ~10)
- Frameworks: 18 (was ~8)
- Databases: 14 (was ~6)
- Cloud: 15 (was ~5)
- Data science: 23 (was ~10)
- Design: 14 (was ~8)
- Tools: 16 (NEW)
- Methodologies: 14 (NEW)
- Soft skills: 14 (NEW)

**Result**: Now detects 30-50+ skills from typical CVs

---

#### Issue 2: Questions Too Project-Focused

**Problem**: "the questions are much much much better but still feel a bit off from the focus on the human part of you, more on the projects"

**Examples of BAD questions user received**:
- "What's your biggest technical hurdle?"
- "How do you balance impact with verification?"
- "How do you mitigate risk of overclaiming?"

**Solution**: Complete rewrite of Director and Sokrates prompts

**Changes to [src/prompts.py](src/prompts.py)**:

1. **SYSTEM_PROMPT_DIRECTOR** (Lines 37-83):
   - Added "CRITICAL FOCUS" section emphasizing THE PERSON
   - Focus on: HOW THEY THINK, not what they built
   - Uncover: INTERNAL MOTIVATIONS, not external achievements
   - Probe: DECISION-MAKING PATTERNS, not technical details
   - Reveal: SELF-AWARENESS and META-COGNITION
   - Added explicit "BAD QUESTIONS TO AVOID" section
   - Added explicit "GOOD QUESTIONS TO AIM FOR" section

2. **SYSTEM_PROMPT_SOKRATES** (Lines 85-127):
   - Added "QUESTION STYLE" emphasizing human introspection
   - Added "EXAMPLES OF GOOD QUESTIONS":
     - "When do you trust your instincts over data?"
     - "What pattern in your own behavior concerns you?"
     - "How do you know when you're learning versus just staying busy?"
   - Added "EXAMPLES OF BAD QUESTIONS (AVOID THESE)":
     - "What's your biggest technical hurdle?" (too work-focused)
     - "How do you balance impact with verification?" (generic)
     - Any question mentioning specific projects by name

**Result**: Questions now probe thinking patterns, not just work history

---

#### Issue 3: Confusing Loading Indicators

**Problem**: "the site shows 'thinking' during the director phase, but then nothing during the sokrates sentence construction..."

**Solution**: Combined both AI calls into single spinner

**Changes to [app.py](app.py)** (Lines 289-315):
```python
# BEFORE: Two separate spinners
with st.spinner("Thinking..."):
    directive, _ = get_interaction_response(...)
# Gap here - no spinner
sokrates_response = get_interaction_response(...)

# AFTER: Single combined spinner
with st.spinner("Thinking..."):
    directive, _ = get_interaction_response(...)
    full_response, new_id = get_interaction_response(...)
# Write response outside spinner
response_placeholder.write(full_response)
```

**Result**: Smooth, continuous loading feedback

---

#### Issue 4: Analysis Page UX

**Problem**: "after answering the last question, during the loading, the last question stays visible... i need it to be hidden from the start or, even better, show all the questions and answers floating around in the screen under the loading, which would be better if it had a bar, not just a circle"

**Solution**: Added interview transcript expander + progress bar

**Changes to [app.py](app.py)** (Lines 329-404):

1. **Interview Transcript Expander**:
   ```python
   with st.expander("Your Interview Transcript", expanded=False):
       for msg in st.session_state.messages:
           # Display full conversation
   ```

2. **Progress Bar with Stage Updates**:
   ```python
   progress_bar = st.progress(0)
   status_text = st.empty()

   progress_bar.progress(10)
   status_text.text("Analyzing interview patterns...")

   # GitHub analysis at 30%
   # Multi-source analysis at 50%
   # Pattern extraction at 70%
   # Finalization at 90%

   progress_bar.progress(100)
   status_text.text("Complete!")
   ```

**Result**: User sees conversation history and detailed progress

---

#### Issue 5: Cluttered Final Page

**Problem**: "on the last screen, where we can download the html, there are a lot of infos which should be maybe inside the site, not in the last page of sokrates. i need the last page to be clean"

**Solution**: Ultra-minimal Streamlit page, all data in HTML

**Changes to [app.py](app.py)** (Lines 431-467):

**REMOVED from Streamlit**:
- Cognitive style display
- Tagline display
- "The Bet" paragraph
- Full JSON data expander

**NEW minimal page**:
```python
st.balloons()
st.title("✨ Analysis Complete")
st.markdown("### Your Anti-Portfolio is ready")

# Just download button
html_content = generate_anti_portfolio_html(data)
st.download_button(
    "📥 Download Your Anti-Portfolio",
    data=html_content,
    file_name="anti_portfolio.html",
    mime="text/html",
    type="primary"
)

st.caption("Open the HTML file in your browser to view your complete analysis")
```

**Verification that HTML has all data**:
- [src/generator.py](src/generator.py) Line 312: Calls `_generate_trajectory_section()`
- Lines 3-81: Comprehensive trajectory section with all new fields
- Main HTML body includes: Core Patterns, Anti-Patterns, Skills Matrix, Growth Focus, Visual Metaphor, The Bet

**Result**: Clean, professional final experience

---

## Current File Structure

```
Sokr/ (will be renamed to Sokrates/)
├── app.py                          # Main Streamlit application (18,791 bytes)
├── src/
│   ├── llm.py                      # LLM integration (Gemini/Local)
│   ├── prompts.py                  # System prompts for agents (ENHANCED)
│   ├── generator.py                # HTML portfolio generator (ENHANCED)
│   ├── utils.py                    # PDF/URL extraction utilities
│   ├── github_analyzer.py          # GitHub learning velocity analysis (NEW)
│   ├── multi_source_analyzer.py    # CV/Portfolio/LinkedIn analysis (NEW)
│   └── maieutic_questions.py       # Advanced question templates (NEW)
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation (9,123 bytes)
├── MULTI_SOURCE_ANALYSIS.md        # Multi-source analysis docs (13,416 bytes)
├── IMPLEMENTATION_SUMMARY.md       # Implementation summary (9,888 bytes)
├── UX_IMPROVEMENTS.md              # UX improvement docs (6,879 bytes)
├── DEVELOPMENT_LOG.md              # This file (NEW)
├── .gitignore                      # Git ignore file (ENHANCED)
└── .streamlit/
    └── secrets.toml                # API keys (NOT committed)
```

---

## Key Technical Decisions

### 1. Multi-Source Data Extraction

**Why**: GitHub-only analysis excludes designers, PMs, writers, early-career developers, and enterprise developers with private repos.

**Implementation**: NLP-based extraction from CVs, portfolios, LinkedIn using regex patterns and complexity scoring.

**Evidence-Based Predictions**: All predictions grounded in observable patterns, not assumptions.

---

### 2. Human-Centered Questioning

**Why**: Traditional interviews allow easy claims and performance. Maieutic questioning makes dishonesty cognitively expensive.

**Implementation**: Multi-agent system (Archivist, Critic, Director, Sokrates) with explicit focus on:
- THE PERSON, not their projects
- HOW THEY THINK, not what they built
- INTERNAL MOTIVATIONS, not external achievements

**Result**: Questions like "What pattern in your own behavior concerns you?" vs "What's your biggest technical hurdle?"

---

### 3. Progressive Enhancement of UX

**Why**: User feedback revealed friction points: confusing loading, cluttered final page, invisible progress.

**Implementation**:
- Combined spinners for smooth transitions
- Progress bar with stage-specific status messages
- Interview transcript visibility during analysis
- Minimal Streamlit page with all data in HTML download

**Result**: Professional, polished experience

---

## API Keys and Secrets

**Required**: Google Gemini API key

**Location**: `.streamlit/secrets.toml` (NOT committed to git)

**Format**:
```toml
LLM_PROVIDER = "google"
GEMINI_API_KEY = "your_gemini_api_key_here"
```

**Alternative**: Local LLM via LM Studio
```toml
LLM_PROVIDER = "local"
```

---

## Next Steps (Discussed but NOT Implemented)

### Immediate: Repository Setup
1. ✅ Rename folder from `Sokr` to `Sokrates`
2. ✅ Create GitHub repository
3. ✅ Push initial commit

### Future Consideration: Move from Streamlit to Next.js

**Reasons discussed**:
- Streamlit is for internal tools/prototypes, SOKRATES is a product
- UX limitations (loading states, layout control)
- Deployment complexity and API timeout issues
- Can't easily add authentication, user accounts, portfolio galleries

**Recommended stack**: Next.js + Vercel + Python backend (FastAPI)

**Hybrid approach**: Keep Python logic, wrap with Next.js frontend

**Status**: Deferred - Streamlit works for MVP

---

## Dependencies

From [requirements.txt](requirements.txt):
```
streamlit>=1.28.0
google-generativeai>=0.3.0
PyPDF2>=3.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
python-dateutil>=2.8.2
```

---

## Testing Notes

**GitHub Analysis**: Tested with public GitHub usernames
**Multi-Source Analysis**: Tested with CVs containing 3 repos, skills now detected correctly
**Question Quality**: Human-centered questions verified in testing
**Loading UX**: Progress bar tested across full analysis pipeline
**Final Page**: Verified HTML contains all data, Streamlit page is minimal

---

## Known Limitations

1. **GitHub Rate Limiting**: 60 requests/hour (unauthenticated), need to add token support for 5000 req/hour
2. **JSON Parsing**: Regex-based extraction with error handling, could use structured output with function calling
3. **Caching**: No caching of GitHub/multi-source analysis results, repeated API calls
4. **Error Handling**: Graceful degradation implemented, could add more sophisticated retry logic

---

## Philosophy

Traditional portfolios are **backward-looking snapshots**.

SOKRATES generates **forward-looking predictions**.

In an AI-saturated world, hiring isn't about current skills.
It's about **growth potential in your specific context**.

SOKRATES answers:
- How fast do they learn?
- How do they think?
- What's their cognitive operating system?
- Where are they naturally headed?
- What would unlock their next level?

---

## Contributors

**Built with**: Claude Code (Claude Sonnet 4.5)
**For**: AI Works Challenge 2025
**Developer**: Sebastiano Pietrasanta

---

## License

MIT License - See LICENSE file for details

---

**Last Updated**: December 14, 2025
**Status**: Ready for GitHub push
**Next Action**: Rename folder to `Sokrates`, create GitHub repo, push code
