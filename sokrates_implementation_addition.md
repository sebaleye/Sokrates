# SOKRATES + PROOF - Implementation Prompt for VS Code

## Project Context

You are implementing **SOKRATES + PROOF**, an AI-native anti-portfolio generator for the AI Works Challenge hackathon.

**Deadline:** December 14, 2025, 4:00 PM CET (approximately 12 hours from now)

**Challenge Requirements:**
1. A working portfolio generator tool (GitHub repo + README)
2. Three example portfolios (publicly accessible)
3. Framework document explaining the philosophy

---

## Core Concept

SOKRATES combines:
- **Maieutic questioning** (Socratic method) to extract how someone thinks
- **Data analysis** (GitHub commits, projects, timelines) to prove learning velocity
- **Predictive modeling** (AI reasoning) to forecast future growth

**Output:** An anti-portfolio that shows "what you will become" instead of "what you've done"

---

## Technical Architecture

### Stack Recommendation
- **Frontend:** Next.js 14+ with App Router
- **Styling:** Tailwind CSS
- **AI:** Anthropic Claude API (Sonnet 4.5)
- **Data Sources:** GitHub API, user input forms
- **Deployment:** Vercel (for quick deployment)
- **Alternative:** Streamlit + Python if you prefer backend-focused

### Project Structure
```
sokrates-portfolio/
├── app/
│   ├── page.tsx                 # Landing page
│   ├── interview/page.tsx       # SOKRATES maieutic interview
│   ├── analyze/page.tsx         # Data extraction & analysis
│   ├── portfolio/[id]/page.tsx  # Generated portfolio view
│   └── api/
│       ├── sokrates/route.ts    # Maieutic AI endpoint
│       ├── analyze/route.ts     # Data extraction endpoint
│       └── generate/route.ts    # Portfolio generation endpoint
├── lib/
│   ├── github-analyzer.ts       # GitHub commit pattern analysis
│   ├── sokrates-engine.ts       # Maieutic questioning logic
│   ├── pattern-extractor.ts     # AI pattern synthesis
│   └── portfolio-generator.ts   # Final output generation
├── components/
│   ├── InterviewFlow.tsx
│   ├── TrajectoryChart.tsx
│   └── PortfolioOutput.tsx
└── prompts/
    ├── maieutic-prompts.ts      # SOKRATES question templates
    ├── analysis-prompts.ts      # Data extraction prompts
    └── synthesis-prompts.ts     # Pattern & prediction prompts
```

---

## Implementation Tasks

### PHASE 1: Core Infrastructure (2-3 hours)

#### Task 1.1: Project Setup
```bash
# Initialize Next.js project
npx create-next-app@latest sokrates-portfolio --typescript --tailwind --app

# Install dependencies
npm install @anthropic-ai/sdk octokit zod date-fns recharts
```

#### Task 1.2: Environment Configuration
Create `.env.local`:
```
ANTHROPIC_API_KEY=your_api_key_here
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

#### Task 1.3: API Route Setup
Create basic API routes in `app/api/`:
- `sokrates/route.ts` - Handles maieutic interview
- `analyze/route.ts` - Handles GitHub/data analysis
- `generate/route.ts` - Generates final portfolio

---

### PHASE 2: GitHub Analysis Module (2-3 hours)

#### Task 2.1: GitHub Data Fetcher
Create `lib/github-analyzer.ts`:

**Requirements:**
- Fetch commit history from GitHub API (via username)
- Extract: commit timestamps, file changes, languages used, project evolution
- Handle rate limiting and errors gracefully
- Return structured data for AI analysis

**Key Metrics to Extract:**
```typescript
interface GitHubAnalysis {
  commitTimeline: {
    date: string;
    count: number;
    complexity: number; // lines changed
  }[];
  languageEvolution: {
    language: string;
    firstUse: string;
    lastUse: string;
    commitCount: number;
  }[];
  projectComplexity: {
    repoName: string;
    created: string;
    lastUpdate: string;
    technologies: string[];
    linesOfCode: number;
  }[];
  learningPatterns: {
    timeToFirstCommit: Record<string, number>; // days from first commit to first competent use
    consistencyScore: number; // commit frequency variance
    explorationVsBuild: number; // ratio of new repos vs commits to existing
  };
}
```

**Implementation Guidance:**
- Use Octokit library for GitHub API
- Paginate through all repos and commits
- Calculate "complexity" using lines changed, files modified
- Detect "learning moments": first use of new language, framework, pattern
- Handle users with no GitHub data gracefully (return null)

#### Task 2.2: Commit Pattern Analysis
Use Claude API to analyze extracted GitHub data:

**Prompt Template:**
```typescript
const analyzeGitHubPattern = `
You are analyzing GitHub commit data to extract learning velocity patterns.

Given this commit history:
${JSON.stringify(githubData)}

Extract and return JSON with:
1. learningVelocity: How fast does this person go from "first commit" to "competent implementation" for new technologies?
2. complexityTrajectory: Is project complexity increasing over time?
3. learningStyle: depth-first (master one thing) vs breadth-first (try many things)?
4. persistenceMetric: Ratio of completed projects vs abandoned experiments
5. independenceRate: Tutorial copying vs original implementation ratio

Base your analysis ONLY on observable commit patterns, not assumptions.
Return valid JSON only, no markdown.
`;
```

---

### PHASE 3: SOKRATES Maieutic Engine (3-4 hours)

#### Task 3.1: Interview Flow Component
Create `components/InterviewFlow.tsx`:

**Requirements:**
- Multi-step form with progress indicator
- Each question appears after previous is answered
- Adaptive questioning based on previous answers
- Store responses in state/database

**Interview Questions (from SOKRATES framework):**

**Step 1: Reliable Competencies**
```
Question: "Which activities do you perform better than average without excessive effort?"
Constraints:
- Maximum 3-5 areas
- No job titles allowed
- Must provide concrete example for each

AI Follow-up Prompt:
"Remove buzzwords and translate to operational capabilities. 
If user says 'strategic thinking', ask for specific decision they made.
If user says 'problem solving', ask for specific problem solved."
```

**Step 2: Friction Zones**
```
Question: "In which situations do you feel competent, but not excellent?"
Constraints:
- Must describe specific situation, not general weakness
- Focus on recurring patterns, not one-off events

AI Follow-up Prompt:
"Cluster recurring frictions. Identify implicit tensions.
Example: If they mention 'documentation feels tedious', probe whether 
it's writing itself or switching from building to explaining."
```

**Step 3: Intentional Ignorance** (CORE OF SOKRATES)
```
Question: "What do you clearly know you do not yet understand?"
Follow-ups:
- "Why is this gap worth exploring?"
- "What would change if you resolved it?"

AI Processing Prompt:
"Reframe each gap as a growth hypothesis, not a weakness.
Connect ignorance to prior experience.
Example: 'I don't understand distributed systems' + background in APIs → 
'Ready to bridge API design into distributed architecture'"
```

**Step 4: Learning Methodology**
```
Questions:
- "What is the first thing you do when you don't understand something?"
- "How do you recognize that learning is happening?"

AI Extraction Prompt:
"Extract an implicit learning methodology. Formalize a 'cognitive operating system'.
Identify: research-first vs experiment-first, community-driven vs solo exploration,
theory-before-practice vs practice-before-theory."
```

**Step 5: Transformative Failures**
```
Question: "When did you realize you were pursuing the wrong answer?"

AI Processing:
"Strip away justification. Highlight the mental pivot.
Find the moment of realization, not the recovery story."
```

#### Task 3.2: Maieutic AI Logic
Create `lib/sokrates-engine.ts`:

**Core Function:**
```typescript
async function askSocraticQuestion(
  previousAnswers: Record<string, string>,
  currentStep: number
): Promise<{
  question: string;
  followUps: string[];
  validationRules: string[];
}> {
  // Use Claude API to generate adaptive questions
  // Based on previous answers and SOKRATES framework
}
```

**Maieutic Prompt Engineering:**
```typescript
const socratesSystemPrompt = `
You are Sokrates, a maieutic interviewer.

Your role:
- Ask ONE question at a time
- Base questions on concrete facts from previous answers
- Never accuse or reassure
- Use contrast and specific events to prompt reflection
- Make dishonesty cognitively expensive by asking for specifics

Example good questions:
- "Across many projects you moved quickly to implementation. When did you consciously choose NOT to implement, and why?"
- "Your work shows continuity. When was the last time you realized you were solving the wrong problem?"

Example bad questions:
- "What are your strengths?" (too generic)
- "Are you a fast learner?" (allows easy claims)
- "What would you improve about yourself?" (invites clichés)

Given the user's previous answers, generate the next maieutic question.
`;
```

---

### PHASE 4: Pattern Synthesis & Prediction (2-3 hours)

#### Task 4.1: Pattern Extractor
Create `lib/pattern-extractor.ts`:

**Main Function:**
```typescript
async function synthesizePatterns(
  interviewData: SokratesAnswers,
  githubData: GitHubAnalysis | null
): Promise<{
  cognitivePatterns: string[];
  learningVelocity: VelocityMetrics;
  growthTrajectory: TrajectoryPrediction;
  hiringInsight: string;
}> {
  // Combine interview + GitHub data
  // Use Claude API to extract non-obvious patterns
}
```

**Synthesis Prompt:**
```typescript
const synthesisPrompt = `
You are analyzing a person's learning patterns from two sources:

1. SOKRATES Interview Data:
${JSON.stringify(interviewData)}

2. GitHub Activity Data (if available):
${githubData ? JSON.stringify(githubData) : "No GitHub data available"}

Extract and return JSON:

{
  "cognitivePatterns": [
    // 3-5 recurring patterns in how they think/learn
    // Example: "Depth-first learning: masters fundamentals before breadth"
    // Example: "Failure-driven refinement: uses errors as compass"
  ],
  
  "learningVelocity": {
    "timeToCompetency": {
      // Estimated weeks from zero to production-ready for new skills
      "technicalSkill": "6-8 weeks",
      "newDomain": "3-4 months",
      "reasoning": "Based on [specific evidence from data]"
    },
    "accelerationPattern": "slow-start-then-rapid | steady-linear | fast-plateau",
    "transferLearning": "high | medium | low" // ability to apply knowledge across domains
  },
  
  "growthTrajectory": {
    "currentPhase": "Description of where they are now",
    "naturalDirection": "Where they're likely headed based on patterns",
    "highLeverageGap": "The ONE tension that would unlock next level growth",
    "readinessIndicators": ["Signal 1", "Signal 2"]
  },
  
  "hiringInsight": {
    "bestFitRole": "Description based on patterns, not job titles",
    "potentialRisks": "Honest assessment of where they might struggle",
    "investmentThesis": "Why betting on this person's GROWTH is valuable"
  }
}

CRITICAL RULES:
- Base predictions ONLY on observable patterns, not assumptions
- Be specific: cite actual examples from the data
- Distinguish "lack of exposure" from "lack of ability"
- Frame gaps as growth vectors, not weaknesses
- Be honest about risks - this builds credibility
`;
```

#### Task 4.2: Trajectory Prediction Logic
**Prediction Algorithm:**
```typescript
// Use both interview + GitHub to predict learning speed

function predictLearningTime(
  targetSkill: string,
  historicalPatterns: LearningPattern[]
): {
  estimatedWeeks: number;
  confidenceLevel: 'high' | 'medium' | 'low';
  reasoning: string;
} {
  // If GitHub data exists:
  // - Find similar skill transitions (e.g., React → Vue is similar to Angular → Svelte)
  // - Calculate average time-to-competency
  // - Adjust for complexity difference
  
  // If only interview data:
  // - Use self-reported learning methodology
  // - Compare to typical learning curves
  // - Mark confidence as 'low' but still provide estimate
}
```

---

### PHASE 5: Portfolio Generator (2 hours)

#### Task 5.1: Anti-Portfolio Structure
Create `lib/portfolio-generator.ts`:

**Output Format:**
```typescript
interface AntiPortfolio {
  metadata: {
    generated: string;
    candidate: string;
  };
  
  sections: {
    // Section 1: Not who I am, but how I think
    thinkingStyle: {
      cognitivePatterns: string[];
      decisionMakingApproach: string;
      problemSolvingMethodology: string;
    };
    
    // Section 2: What I do reliably well
    reliableCompetencies: {
      area: string;
      evidence: string;
      operationalCapability: string;
    }[];
    
    // Section 3: Friction zones I am exploring
    frictionZones: {
      situation: string;
      currentApproach: string;
      explorationStrategy: string;
    }[];
    
    // Section 4: Intentional ignorance
    intentionalGaps: {
      gap: string;
      worthExploring: string;
      growthHypothesis: string;
    }[];
    
    // Section 5: How I learn when I don't know
    learningMethodology: {
      firstResponse: string;
      recognitionSignals: string[];
      metaCognition: string;
    };
    
    // Section 6: Failures that changed my direction
    transformativeFailures: {
      situation: string;
      realizationMoment: string;
      newDirection: string;
    }[];
    
    // Section 7: Growth trajectory (THE PROOF)
    trajectory: {
      learningVelocityMetrics: VelocityMetrics;
      predictedCapabilities: {
        skill: string;
        estimatedTime: string;
        confidence: string;
        reasoning: string;
      }[];
      naturalGrowthDirection: string;
      investmentThesis: string;
    };
  };
}
```

#### Task 5.2: Portfolio UI Component
Create `components/PortfolioOutput.tsx`:

**Design Requirements:**
- Clean, minimal aesthetic (anti-corporate)
- Typography-focused (no flashy graphics)
- Clear hierarchy: thinking → patterns → trajectory → prediction
- Interactive trajectory chart (use Recharts)
- Downloadable as PDF (optional but nice)
- Shareable link

**Key Visual Elements:**
1. **Cognitive Patterns Card** - Large, prominent, establishes "how they think"
2. **Learning Velocity Chart** - Timeline showing skill acquisition speed
3. **Trajectory Prediction** - Future-focused section with specific estimates
4. **Investment Thesis Box** - "Why hire this person" summary

---

### PHASE 6: Three Example Portfolios (1-2 hours)

#### Example 1: Developer with Rich GitHub Data
**Input:**
- GitHub: @username-with-good-history
- SOKRATES interview answers (you'll create fictional but realistic answers)

**Expected Output:**
- Shows clear commit pattern evolution
- Learning velocity: "Went from React basics to complex state management in 4 months"
- Prediction: "Could master Vue.js in 3-4 weeks based on transfer learning pattern"
- Cognitive pattern: "Documentation-driven development: writes tests and docs before code"

#### Example 2: Designer with Medium Data
**Input:**
- Portfolio timeline (fictional: 2020-2025)
- SOKRATES interview focusing on design thinking evolution

**Expected Output:**
- Shows design systems thinking emergence
- Learning velocity: "Transitioned from component design to systems thinking over 2 years"
- Prediction: "Ready for strategic design leadership role"
- Cognitive pattern: "Systematic abstraction: identifies patterns before optimizing"

#### Example 3: Career Switcher with Minimal Data
**Input:**
- SOKRATES interview only (no GitHub or portfolio)
- Background: law → tech transition

**Expected Output:**
- Shows meta-learning ability
- Learning velocity: "Fast adapter in new domains due to first-principles thinking"
- Prediction: "Could learn new technical domain in 4-6 months based on cross-domain transfer"
- Cognitive pattern: "First-principles reasoning: rebuilds understanding from axioms"

**Implementation:**
- Create JSON files with example data in `examples/` folder
- Build a demo mode that loads these examples
- Deploy each as separate route: `/portfolio/developer`, `/portfolio/designer`, `/portfolio/switcher`

---

### PHASE 7: Framework Document (1 hour)

Update the SOKRATES_Framework.md you already have by adding:

**New Section to Add:**
```markdown
## 9. HOW AI PREDICTS GROWTH FROM MAIEUTIC ANSWERS

Traditional portfolios show static snapshots.
SOKRATES generates dynamic predictions.

### Data Sources
1. **Maieutic Interview** - Reveals thinking patterns and learning methodology
2. **GitHub Analysis** (optional) - Proves learning velocity with commit data
3. **Project Timeline** (optional) - Shows complexity evolution

### Pattern Extraction Process
1. AI analyzes interview answers for recurring cognitive patterns
2. If GitHub data exists: extract time-to-competency metrics
3. Cross-reference self-reported learning style with actual behavior
4. Identify acceleration patterns (slow-start vs fast-plateau)

### Prediction Generation
Based on extracted patterns, AI estimates:
- Time needed to learn new technical skills
- Readiness for role complexity increases
- Transfer learning capability across domains

### Why Predictions Matter
Hiring isn't about current skills (AI can do most tasks).
Hiring is about growth potential in your specific context.

SOKRATES answers: "How fast will this person become your best asset?"
```

---

## Critical Implementation Notes

### For GitHub Analysis:
- **Handle missing data gracefully** - Most users won't have rich GitHub history
- **Don't require GitHub** - Make it optional but valuable when present
- **Respect rate limits** - Cache GitHub data, don't fetch on every request
- **Privacy first** - Only public repos, clear data usage consent

### For AI Prompts:
- **Temperature: 0.7** for maieutic questions (need creativity)
- **Temperature: 0.3** for pattern extraction (need consistency)
- **Max tokens: 2000-4000** for synthesis (need detailed analysis)
- **Streaming responses** for better UX during long AI calls

### For UX:
- **Progress indicators** - Interview takes 10-15 minutes
- **Save state** - Don't lose answers on refresh
- **Mobile responsive** - Judges might view on phone
- **Fast loading** - Optimize AI calls, show skeleton states

### For Deployment:
- **Environment variables** - Never commit API keys
- **Vercel deployment** - Quick, free, reliable
- **Public URLs** - Make examples immediately accessible
- **README quality** - Clear installation, usage, architecture explanation

---

## Testing Strategy

### Before Submission:
1. **Test complete flow** - Onboarding → Interview → Analysis → Portfolio
2. **Test with different data levels:**
   - Rich GitHub data
   - Medium data (just interview + basic info)
   - Minimal data (interview only)
3. **Test edge cases:**
   - Invalid GitHub username
   - Incomplete interview answers
   - API failures (show graceful errors)
4. **Test on mobile** - Responsive design check
5. **Test portfolio sharing** - Links work, look professional

---

## README.md Template

```markdown
# SOKRATES + PROOF
## An AI-Native Anti-Portfolio Generator

### What is this?
SOKRATES combines Socratic maieutics with AI-powered pattern analysis to create predictive portfolios that show "what you will become" instead of "what you've done."

### Quick Start
\`\`\`bash
git clone https://github.com/yourusername/sokrates-portfolio
cd sokrates-portfolio
npm install
echo "ANTHROPIC_API_KEY=your_key_here" > .env.local
npm run dev
\`\`\`

### How it works
1. **Maieutic Interview** - AI asks Socratic questions to reveal thinking patterns
2. **Data Analysis** - Optionally analyzes GitHub commits for learning velocity
3. **Pattern Synthesis** - AI extracts cognitive patterns and predicts growth trajectory
4. **Anti-Portfolio** - Generates forward-looking portfolio focused on potential

### Live Examples
- [Developer Example](/portfolio/developer)
- [Designer Example](/portfolio/designer)
- [Career Switcher Example](/portfolio/switcher)

### Architecture
- **Frontend:** Next.js 14 + Tailwind CSS
- **AI:** Claude Sonnet 4.5 via Anthropic API
- **Data:** GitHub API (optional), user interviews
- **Deploy:** Vercel

### Philosophy
See [SOKRATES_Framework.md](./SOKRATES_Framework.md) for full philosophy and methodology.
```

---

## Time Management (12 hours remaining)

**Hours 1-3:** Core infrastructure + API routes
**Hours 4-6:** GitHub analysis + SOKRATES interview engine
**Hours 7-9:** Pattern synthesis + portfolio generator
**Hours 10-11:** Three example portfolios + polish
**Hour 12:** Deploy, test, submit

---

## Success Criteria

✅ Tool actually works (not just a concept)
✅ Maieutic interview feels different from normal forms
✅ AI extracts non-obvious patterns (not just reformatting input)
✅ Predictions are specific and evidence-based
✅ Three examples show different data richness levels
✅ Framework document is clear and compelling
✅ Deployed with public URLs
✅ Submitted before 2:00 PM CET (2 hours before deadline)

---

## Emergency Simplifications (if running out of time)

If you're at Hour 10 and not done:

**Cut GitHub Analysis** - Make it interview-only, predictions based on self-reported learning patterns
**Simplify UI** - Basic HTML/CSS, no fancy charts
**Reduce Examples** - Two examples instead of three
**Keep Core:** Maieutic questioning + pattern extraction + predictive trajectory

The philosophy is the differentiator. Execution proves it works.

---

## Final Checklist Before Submission

- [ ] Tool runs locally without errors
- [ ] Deployed to Vercel with public URL
- [ ] Three example portfolios are publicly accessible
- [ ] GitHub README is complete with clear instructions
- [ ] SOKRATES_Framework.md is updated with prediction methodology
- [ ] All links in submission form work
- [ ] Tested on different screen sizes
- [ ] API keys are in .env, not committed to Git
- [ ] Submission form completed 2 hours before deadline

---

## You've Got This

This concept is strong. The philosophy is differentiated. The execution is feasible in 12 hours.

Focus on:
1. Making the maieutic interview feel DIFFERENT
2. Generating predictions that are SPECIFIC
3. Showing it works with REAL examples

The judges are looking for innovation + execution. You have both.

Now go build it. 🚀
