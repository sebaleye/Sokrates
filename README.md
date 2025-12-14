# SOKRATES

An AI-native anti-portfolio generator that reveals professional trajectory through Socratic dialogue.

---

## Overview

SOKRATES combines Socratic maieutics with AI-powered pattern analysis to create predictive portfolios focused on growth potential rather than past achievements.

This is not a CV generator. This is a trajectory analyzer.

Built with Google's latest **Interactions API**, enabling stateful, multi-turn conversations that maintain context throughout the maieutic interview process.

---

## Features

### Maieutic Interview Engine
- Adaptive Socratic questioning that extracts thinking patterns
- Multi-agent system (Archivist, Critic, Director, Sokrates)
- Designed to make dishonesty cognitively expensive through specific questioning

### Multi-Source Learning Velocity Analysis

**GitHub Analysis** (optional):
- Analyzes commit patterns to extract learning speed
- Tracks language adoption and project complexity evolution
- Calculates persistence metrics and exploration vs. build ratios
- Predicts time-to-competency for new skills

**Professional Background Analysis** (CVs, LinkedIn, Portfolios):
- Extracts timeline and career progression
- Identifies technologies across all domains
- Assesses project complexity
- Tracks formal education and certifications
- Detects learning signals (experimentation, mastery, teaching)

### Predictive Trajectory Modeling
- Combines interview insights with data analysis
- Generates specific predictions about future growth
- Identifies high-leverage gaps that unlock next-level performance
- Provides hiring intelligence with honest risk assessment

### Anti-Portfolio Output
- Interactive HTML portfolio focused on potential
- Cognitive patterns visualization
- Learning velocity metrics and predictions
- Growth trajectory with readiness indicators

---

## Quick Start

### Installation

```bash
git clone https://github.com/sebaleye/Sokrates.git
cd Sokrates

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file:

```toml
LLM_PROVIDER = "google"
GEMINI_API_KEY = "your_api_key_here"

# OR using local LLM
# LLM_PROVIDER = "local"
```

### Run

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

---

## How It Works

### Phase 1: Data Collection
- Upload documents (CVs, LinkedIn PDFs, portfolios)
- Provide URLs (personal websites, portfolio sites)
- GitHub username (optional)
- Free-form input (notes, context)

### Phase 2: Multi-Agent Analysis
- **Multi-Source Analyzer**: Extracts structured data (timeline, skills, projects, education)
- **Archivist**: Separates facts from narrative
- **Critic**: Identifies tensions and gaps
- **Director**: Guides the interview strategy
- **Sokrates**: Conducts the maieutic interview

### Phase 3: Maieutic Interview
Three focused questions designed to extract:
- Origins: Why they do what they do
- Process: How they think and learn
- Potential: Their growth edges and limits

### Phase 4: Pattern Extraction
- Synthesizes interview responses with all available data
- Extracts cognitive patterns and learning methodology
- Predicts learning velocity and growth trajectory
- Generates hiring intelligence with specific time estimates

### Phase 5: Portfolio Generation
- Interactive HTML portfolio
- JSON data export
- Professional, shareable output

---

## Architecture

```
Sokrates/
├── app.py                          # Main Streamlit application
├── src/
│   ├── llm.py                      # LLM integration
│   ├── prompts.py                  # System prompts for agents
│   ├── generator.py                # HTML portfolio generator
│   ├── utils.py                    # PDF/URL extraction utilities
│   ├── github_analyzer.py          # GitHub learning velocity analysis
│   ├── multi_source_analyzer.py    # CV/Portfolio/LinkedIn analysis
│   └── maieutic_questions.py       # Question templates
├── requirements.txt
└── README.md
```

---

## Key Innovations

### Maieutic Questioning
Unlike traditional interviews that allow easy claims, SOKRATES:
- Asks for concrete examples, not abstractions
- Uses contrast and specifics to prompt reflection
- Makes dishonesty cognitively expensive
- Focuses on thinking patterns, not achievements

### Learning Velocity Tracking
When GitHub data is available:
- Calculates time from first commit to competent use
- Identifies acceleration patterns
- Measures consistency and persistence
- Predicts transfer learning capability

### Predictive Analysis
Rather than describing past performance:
- Estimates specific timeframes for learning new skills
- Identifies high-leverage gaps for growth
- Provides readiness indicators showing growth capacity
- Offers honest risk assessment

### Anti-Portfolio Philosophy
- Reframes gaps as growth vectors
- Distinguishes lack of exposure from lack of ability
- Focuses on potential in specific contexts
- Answers: "How fast will this person become valuable?"

---

## Advanced Configuration

### LLM Providers

**Cloud Provider (Default)**
```toml
LLM_PROVIDER = "google"
GEMINI_API_KEY = "your_api_key"
```

**Local LLM**
```toml
LLM_PROVIDER = "local"
# Requires local LLM server running on http://localhost:1234
```

### GitHub API Rate Limits
- Public API: 60 requests/hour (unauthenticated)
- With token: 5000 requests/hour

---

## Use Cases

**Job Seekers**: Stand out with trajectory-focused portfolios that demonstrate learning velocity and growth potential.

**Hiring Managers**: Assess growth potential beyond experience, understand cognitive patterns, and predict time-to-productivity.

**Career Coaches**: Help clients articulate thinking patterns and identify high-leverage development areas.

---

## License

MIT License

---

Built for AI Works Challenge 2025
