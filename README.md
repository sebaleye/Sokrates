# SOKRATES + PROOF
## An AI-Native Anti-Portfolio Generator

### What is this?

SOKRATES combines Socratic maieutics with AI-powered pattern analysis to create **predictive portfolios** that show "what you will become" instead of "what you've done."

This is not a CV generator. This is a trajectory analyzer.

---

## Features

### 🧠 Maieutic Interview Engine
- Adaptive Socratic questioning that extracts thinking patterns
- Multi-agent system (Archivist, Critic, Director, Sokrates)
- Designed to make dishonesty cognitively expensive through specific questioning

### 📊 Multi-Source Learning Velocity Analysis

**GitHub Analysis** (when available):
- Analyzes commit patterns to extract learning speed
- Tracks language adoption and project complexity evolution
- Calculates persistence metrics and exploration vs. build ratios
- Predicts time-to-competency for new skills

**Professional Background Analysis** (CVs, LinkedIn, Portfolios):
- Extracts timeline and career progression
- Identifies 100+ technologies across all domains
- Assesses project complexity with NLP
- Tracks formal education and certifications
- Detects learning signals (experimentation, mastery, teaching)
- Works for ALL professionals, not just developers

### 🎯 Predictive Trajectory Modeling
- Combines interview insights with GitHub data (when available)
- Generates specific predictions about future growth
- Identifies high-leverage gaps that unlock next-level performance
- Provides hiring intelligence with honest risk assessment

### 🎨 Anti-Portfolio Output
- Interactive HTML portfolio focused on potential, not credentials
- Cognitive patterns visualization
- Learning velocity metrics and predictions
- Growth trajectory with readiness indicators

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Sokr

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file:

```toml
# Using Google Gemini (Recommended)
LLM_PROVIDER = "google"
GEMINI_API_KEY = "your_gemini_api_key_here"

# OR using local LLM (LM Studio)
# LLM_PROVIDER = "local"
```

### Run the Application

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

---

## How It Works

### Phase 1: Data Collection
1. **Upload Documents**: CVs, LinkedIn PDFs, portfolios
2. **Provide URLs**: Personal websites, portfolio sites
3. **GitHub Username** (Optional): Enables code velocity analysis
4. **Free-form Input**: Brain dump, notes, context

**All input types are analyzed with equal rigor** - GitHub is optional, not required.

### Phase 2: Multi-Agent Analysis
- **Multi-Source Analyzer**: Extracts structured data (timeline, skills, projects, education)
- **Archivist**: Separates facts from narrative (enhanced with structured data)
- **Critic**: Identifies tensions and gaps (informed by data patterns)
- **Director**: Guides the interview strategy
- **Sokrates**: Conducts the maieutic interview

### Phase 3: Maieutic Interview
- 3 focused questions designed to extract:
  - Origins: Why they do what they do
  - Process: How they think and learn
  - Potential: Their growth edges and limits

### Phase 4: Pattern Extraction & Prediction
- AI synthesizes interview + ALL available data sources
- Combines insights from: interviews, GitHub (if provided), CVs/portfolios
- Extracts cognitive patterns and learning methodology
- Predicts learning velocity and growth trajectory
- Cross-validates patterns across multiple data sources
- Generates hiring intelligence with specific time estimates

### Phase 5: Anti-Portfolio Generation
- Interactive HTML portfolio
- JSON data export
- Shareable, professional output

---

## Architecture

```
Sokr/
├── app.py                          # Main Streamlit application
├── src/
│   ├── llm.py                      # LLM integration (Gemini/Local)
│   ├── prompts.py                  # System prompts for agents
│   ├── generator.py                # HTML portfolio generator
│   ├── utils.py                    # PDF/URL extraction utilities
│   ├── github_analyzer.py          # GitHub learning velocity analysis
│   ├── multi_source_analyzer.py    # CV/Portfolio/LinkedIn analysis
│   └── maieutic_questions.py       # Advanced question templates
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── MULTI_SOURCE_ANALYSIS.md        # Multi-source analysis documentation
```

---

## Key Innovations

### 1. Maieutic Questioning
Unlike traditional interviews that allow easy claims, SOKRATES:
- Asks for **concrete examples**, not abstractions
- Uses **contrast and specifics** to prompt reflection
- Makes **dishonesty cognitively expensive**
- Focuses on **thinking patterns**, not achievements

### 2. Learning Velocity Tracking
When GitHub data is available:
- Calculates time from first commit to competent use
- Identifies acceleration patterns (slow-start vs fast-plateau)
- Measures consistency and persistence
- Predicts transfer learning capability

### 3. Predictive Analysis
Rather than describing past performance:
- Estimates **specific timeframes** for learning new skills
- Identifies the **one high-leverage gap** for growth
- Provides **readiness indicators** showing growth capacity
- Offers **honest risk assessment** for credibility

### 4. Anti-Portfolio Philosophy
- Reframes "gaps" as **growth vectors**, not weaknesses
- Distinguishes "lack of exposure" from "lack of ability"
- Focuses on **potential in specific contexts**
- Answers: "How fast will this person become your best asset?"

---

## Advanced Configuration

### Using Different LLM Providers

#### Google Gemini (Default)
```toml
LLM_PROVIDER = "google"
GEMINI_API_KEY = "your_api_key"
```

#### Local LLM (LM Studio)
```toml
LLM_PROVIDER = "local"
# Make sure LM Studio is running on http://localhost:1234
```

### GitHub API Rate Limits
- Public API: 60 requests/hour (unauthenticated)
- With token: 5000 requests/hour

To add GitHub token support, modify `src/github_analyzer.py`:
```python
analyzer = GitHubAnalyzer(github_token="your_github_token")
```

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

## Use Cases

### For Job Seekers
- Stand out with trajectory-focused portfolios
- Demonstrate learning velocity with data
- Show potential, not just credentials

### For Hiring Managers
- Assess growth potential, not just experience
- Get honest risk assessments
- Understand cognitive patterns and learning styles
- Predict time-to-productivity

### For Career Coaches
- Help clients articulate their thinking patterns
- Identify high-leverage development areas
- Create compelling, evidence-based narratives

---

## Example Output

```json
{
  "cognitive_style": "The Systematic Explorer",
  "tagline": "First-principles thinker building from axioms",
  "learning_velocity": {
    "timeToCompetency": "6-8 weeks for technical skills, 3-4 months for new domains",
    "accelerationPattern": "slow-start-then-rapid",
    "transferLearning": "high"
  },
  "growth_trajectory": {
    "currentPhase": "Transitioning from implementation to architecture",
    "naturalDirection": "Systems design and distributed thinking",
    "highLeverageGap": "Moving from solo execution to collaborative technical leadership",
    "readinessIndicators": [
      "Already questions architectural assumptions",
      "Shows meta-cognitive awareness of own learning process",
      "Seeks patterns across domains"
    ]
  },
  "hiring_insight": {
    "bestFitRole": "Technical lead on greenfield projects requiring architectural decisions",
    "potentialRisks": "May over-engineer early-stage MVPs; needs guidance on pragmatic shortcuts",
    "investmentThesis": "Fast learner with proven transfer capability. Will become your architecture expert within 6 months."
  }
}
```

---

## Contributing

This project was built for the AI Works Challenge. Contributions welcome!

### Areas for Enhancement
- Add more data sources (LinkedIn API, Twitter, etc.)
- Implement trajectory visualization charts
- Add multi-language support
- Create example portfolios dataset
- Build comparison/benchmarking features

---

## Credits

**Concept**: SOKRATES Framework (Maieutic Portfolio Generation)
**Implementation**: Python/Streamlit with Google Gemini
**Philosophy**: Trajectory over credentials, potential over past

---

## License

MIT License - See LICENSE file for details

---

**Built with Claude Code**
Generated for the AI Works Challenge 2025
