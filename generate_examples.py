"""
Script to generate 3 example anti-portfolios for demonstration
"""
import os
from src.generator import generate_anti_portfolio_html

# Example 1: Developer (Builder profile)
developer_data = {
    "profile_type": "builder",
    "cognitive_style": "Systems Architect",
    "tagline": "Builds scalable solutions from first principles",
    "core_patterns": [
        {
            "title": "Bottom-Up Problem Solving",
            "description": "Starts with fundamentals, builds understanding layer by layer. Prefers to understand the 'why' before implementing the 'how'."
        },
        {
            "title": "Systematic Debugging",
            "description": "Approaches bugs methodically - isolates variables, forms hypotheses, tests incrementally. Rarely guesses."
        },
        {
            "title": "Documentation-Driven Development",
            "description": "Writes documentation before code to clarify thinking. Uses writing as a design tool."
        }
    ],
    "anti_patterns": [
        {
            "title": "Premature Optimization",
            "description": "Actively resists optimizing before measuring. Prefers working code over perfect code."
        },
        {
            "title": "Cargo Cult Programming",
            "description": "Refuses to copy-paste solutions without understanding. Will spend extra time to learn fundamentals."
        }
    ],
    "skills_matrix": {
        "Python": 92,
        "System Design": 85,
        "API Architecture": 88,
        "Problem Decomposition": 90,
        "Technical Writing": 78,
        "Code Review": 82
    },
    "growth_focus": "Moving from individual contributor to technical leadership - learning to multiply impact through others",
    "the_bet": "Marco has demonstrated consistent ability to take ambiguous problems and deliver clean, maintainable solutions. His systematic approach means he rarely introduces bugs that waste team time. In 6 months, he could own your most critical technical decisions.",
    "visual_metaphor": "A well-organized workshop where every tool has its place, blueprints cover the walls, and half-finished prototypes show iterative progress.",
    "learning_velocity": {
        "timeToCompetency": "4-6 weeks for new frameworks, 2-3 months for new domains",
        "accelerationPattern": "slow-start-then-rapid",
        "transferLearning": "high"
    },
    "growth_trajectory": {
        "currentPhase": "Senior IC transitioning toward architecture roles",
        "naturalDirection": "Platform engineering and developer experience",
        "highLeverageGap": "Stakeholder communication - translating technical concepts for non-technical audiences",
        "readinessIndicators": [
            "Already mentoring junior developers informally",
            "Proactively documents architectural decisions",
            "Asks 'who else needs to know?' before implementing"
        ]
    },
    "hiring_insight": {
        "bestFitRole": "Staff Engineer or Tech Lead on infrastructure/platform teams",
        "potentialRisks": "May over-engineer early-stage products. Needs guidance on when 'good enough' is actually good enough.",
        "investmentThesis": "Strong fundamentals + systematic learning approach = reliable growth trajectory. Will become your go-to person for critical technical decisions within a year."
    }
}

# Example 2: Designer (Creator profile)
designer_data = {
    "profile_type": "creator",
    "cognitive_style": "Empathy-Driven Craftsperson",
    "tagline": "Designs for humans, not interfaces",
    "core_patterns": [
        {
            "title": "User Story Immersion",
            "description": "Spends significant time understanding user context before touching design tools. Interviews, observes, synthesizes."
        },
        {
            "title": "Iterative Refinement",
            "description": "Works in rapid cycles - sketch, test, refine. Comfortable throwing away work that doesn't serve users."
        },
        {
            "title": "Systems Thinking in Design",
            "description": "Sees individual screens as part of larger flows. Designs components that work across contexts."
        }
    ],
    "anti_patterns": [
        {
            "title": "Aesthetic-First Design",
            "description": "Actively resists making things 'pretty' before they're usable. Function shapes form."
        },
        {
            "title": "Design by Committee",
            "description": "Pushes back on feedback that lacks user evidence. Advocates for research over opinions."
        }
    ],
    "skills_matrix": {
        "User Research": 88,
        "Interaction Design": 91,
        "Design Systems": 85,
        "Prototyping": 87,
        "Visual Design": 80,
        "Stakeholder Management": 75
    },
    "growth_focus": "Developing quantitative skills - learning to measure design impact with data, not just qualitative feedback",
    "the_bet": "Elena brings rare combination: strong craft skills AND genuine user empathy. She doesn't just make things look good - she makes them work for real people. Her designs consistently test well because she validates before polishing.",
    "visual_metaphor": "A design studio with user personas on the walls, prototype sketches everywhere, and a well-worn notebook full of interview notes.",
    "learning_velocity": {
        "timeToCompetency": "2-3 weeks for new design tools, 6-8 weeks for new product domains",
        "accelerationPattern": "fast-plateau",
        "transferLearning": "high"
    },
    "growth_trajectory": {
        "currentPhase": "Senior Designer ready for product ownership",
        "naturalDirection": "Design leadership or product design management",
        "highLeverageGap": "Data literacy - connecting design decisions to business metrics",
        "readinessIndicators": [
            "Already influences product roadmap through research insights",
            "Mentors junior designers on research methods",
            "Builds relationships across engineering and product"
        ]
    },
    "hiring_insight": {
        "bestFitRole": "Lead Product Designer on user-facing products with complex workflows",
        "potentialRisks": "May push back strongly on tight deadlines that skip research. Needs buy-in on research investment.",
        "investmentThesis": "User-centered designers reduce costly pivots. Elena's research-first approach means fewer redesigns and higher user satisfaction scores."
    }
}

# Example 3: Marketing Strategist (Strategist profile)
marketer_data = {
    "profile_type": "strategist",
    "cognitive_style": "Data-Informed Storyteller",
    "tagline": "Finds the story the numbers are trying to tell",
    "core_patterns": [
        {
            "title": "Hypothesis-Driven Marketing",
            "description": "Treats campaigns as experiments. Always has a clear hypothesis, measurement plan, and learning objective."
        },
        {
            "title": "Audience Segmentation Obsession",
            "description": "Never thinks about 'users' generically. Constantly segments, profiles, and personalizes messaging."
        },
        {
            "title": "Cross-Channel Orchestration",
            "description": "Sees marketing as a system. Understands how channels interact and optimizes for journey, not touchpoints."
        }
    ],
    "anti_patterns": [
        {
            "title": "Vanity Metrics",
            "description": "Actively avoids metrics that don't connect to business outcomes. Questions any KPI that can't trace to revenue."
        },
        {
            "title": "Copy-Cat Campaigns",
            "description": "Resists 'best practices' without local validation. What worked elsewhere may not work here."
        }
    ],
    "skills_matrix": {
        "Marketing Analytics": 89,
        "Campaign Strategy": 86,
        "Copywriting": 82,
        "A/B Testing": 91,
        "Stakeholder Reporting": 84,
        "Budget Optimization": 80
    },
    "growth_focus": "Building technical skills in marketing automation and data pipelines to reduce dependency on engineering",
    "the_bet": "Giulia combines analytical rigor with creative intuition. She doesn't just run campaigns - she builds systems that learn. Her test-and-iterate approach means marketing spend gets more efficient over time.",
    "visual_metaphor": "A war room with dashboards on every screen, campaign calendars covering the walls, and a whiteboard full of customer journey maps.",
    "learning_velocity": {
        "timeToCompetency": "3-4 weeks for new marketing platforms, 2 months for new industry verticals",
        "accelerationPattern": "steady-linear",
        "transferLearning": "medium"
    },
    "growth_trajectory": {
        "currentPhase": "Senior Marketer ready for team leadership",
        "naturalDirection": "Head of Growth or VP Marketing",
        "highLeverageGap": "People management - transitioning from individual execution to team multiplication",
        "readinessIndicators": [
            "Already owns significant budget with proven ROI",
            "Cross-functional relationships with product and sales",
            "Has trained contractors and junior team members"
        ]
    },
    "hiring_insight": {
        "bestFitRole": "Growth Marketing Lead or Head of Demand Generation",
        "potentialRisks": "May struggle in environments that prioritize brand over performance. Needs clear metrics to stay motivated.",
        "investmentThesis": "Data-driven marketers compound results. Giulia's systematic approach means every campaign teaches something, and marketing efficiency improves quarter over quarter."
    }
}

# Generate the HTML files
os.makedirs("examples", exist_ok=True)

html_developer = generate_anti_portfolio_html(developer_data, "Marco Ferretti")
html_designer = generate_anti_portfolio_html(designer_data, "Elena Marchetti")
html_marketer = generate_anti_portfolio_html(marketer_data, "Giulia Benedetti")

with open("examples/developer_portfolio.html", "w", encoding="utf-8") as f:
    f.write(html_developer)

with open("examples/designer_portfolio.html", "w", encoding="utf-8") as f:
    f.write(html_designer)

with open("examples/marketer_portfolio.html", "w", encoding="utf-8") as f:
    f.write(html_marketer)

print("Generated 3 example portfolios in /examples folder:")
print("  - developer_portfolio.html (Marco Ferretti - Builder profile)")
print("  - designer_portfolio.html (Elena Marchetti - Creator profile)")
print("  - marketer_portfolio.html (Giulia Benedetti - Strategist profile)")
