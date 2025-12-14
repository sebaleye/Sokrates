"""
Advanced Maieutic Question Templates for SOKRATES
Based on the SOKRATES framework - questions designed to extract thinking patterns
"""

MAIEUTIC_QUESTIONS = {
    "reliable_competencies": {
        "primary": "Which activities do you perform better than average without excessive effort?",
        "constraints": [
            "Maximum 3-5 areas",
            "No job titles allowed",
            "Must provide concrete example for each"
        ],
        "follow_up_prompt": """
Remove buzzwords and translate to operational capabilities.
If user says 'strategic thinking', ask for specific decision they made.
If user says 'problem solving', ask for specific problem solved.
Push for CONCRETE examples, not abstractions.
        """
    },

    "friction_zones": {
        "primary": "In which situations do you feel competent, but not excellent?",
        "constraints": [
            "Must describe specific situation, not general weakness",
            "Focus on recurring patterns, not one-off events"
        ],
        "follow_up_prompt": """
Cluster recurring frictions. Identify implicit tensions.
Example: If they mention 'documentation feels tedious', probe whether
it's writing itself or switching from building to explaining.
        """
    },

    "intentional_ignorance": {
        "primary": "What do you clearly know you do not yet understand?",
        "follow_ups": [
            "Why is this gap worth exploring?",
            "What would change if you resolved it?"
        ],
        "ai_processing_prompt": """
Reframe each gap as a growth hypothesis, not a weakness.
Connect ignorance to prior experience.
Example: 'I don't understand distributed systems' + background in APIs →
'Ready to bridge API design into distributed architecture'
        """
    },

    "learning_methodology": {
        "questions": [
            "What is the first thing you do when you don't understand something?",
            "How do you recognize that learning is happening?"
        ],
        "extraction_prompt": """
Extract an implicit learning methodology. Formalize a 'cognitive operating system'.
Identify: research-first vs experiment-first, community-driven vs solo exploration,
theory-before-practice vs practice-before-theory.
        """
    },

    "transformative_failures": {
        "primary": "When did you realize you were pursuing the wrong answer?",
        "ai_processing": """
Strip away justification. Highlight the mental pivot.
Find the moment of realization, not the recovery story.
Look for: What changed in their thinking process? What pattern did they notice?
        """
    },

    "decision_making": {
        "primary": "Across many projects you moved quickly to implementation. When did you consciously choose NOT to implement, and why?",
        "variants": [
            "Your work shows continuity. When was the last time you realized you were solving the wrong problem?",
            "You've explored multiple domains. What made you stop pursuing one path to focus on another?"
        ]
    },

    "constraint_testing": {
        "primary": "Describe a time when a constraint you thought was fixed turned out to be negotiable.",
        "follow_ups": [
            "How did you discover it was negotiable?",
            "What constraints are you currently treating as fixed that might not be?"
        ]
    },

    "meta_cognition": {
        "questions": [
            "How do you know when you're wrong?",
            "What signals tell you that you need to change approach?",
            "When do you trust your instincts vs when do you seek data?"
        ]
    }
}


def get_phase_questions(phase, history, tensions):
    """
    Generate appropriate questions based on the interview phase

    Args:
        phase: Interview phase (1-3)
        history: Previous conversation context
        tensions: Identified tensions from analysis

    Returns:
        dict with question guidance for the director
    """
    if phase == 1:
        # PHASE 1: ORIGINS - Why they do what they do
        return {
            "focus": "Origins and Motivation",
            "goal": "Understand WHY they do what they do, not just WHAT they do",
            "question_types": [
                MAIEUTIC_QUESTIONS["reliable_competencies"],
                MAIEUTIC_QUESTIONS["decision_making"]
            ],
            "directive": "Ask about their origins. What drew them to this work? Don't accept 'I was interested' - push for the specific moment or realization."
        }

    elif phase == 2:
        # PHASE 2: PROCESS - How they work
        return {
            "focus": "Process and Learning Methodology",
            "goal": "Reveal their cognitive operating system - how they think and learn",
            "question_types": [
                MAIEUTIC_QUESTIONS["learning_methodology"],
                MAIEUTIC_QUESTIONS["friction_zones"]
            ],
            "directive": "Ask about HOW they work. What's their process when facing the unknown? Look for chaos vs structure, intuition vs analysis."
        }

    else:
        # PHASE 3: POTENTIAL - Test limits with hypotheticals
        return {
            "focus": "Potential and Future Direction",
            "goal": "Test their limits with hypothetical scenarios, reveal growth edges",
            "question_types": [
                MAIEUTIC_QUESTIONS["intentional_ignorance"],
                MAIEUTIC_QUESTIONS["constraint_testing"]
            ],
            "directive": "Present a hypothetical scenario that tests their thinking. Force them to reason through unknowns."
        }


def generate_adaptive_question(user_answer, phase, tensions):
    """
    Generate adaptive follow-up based on user's answer quality

    Args:
        user_answer: The user's most recent response
        phase: Current interview phase
        tensions: Known tensions from analysis

    Returns:
        str: Guidance for next question
    """
    answer_length = len(user_answer.split())

    # Short/dismissive answer - PIVOT
    if answer_length < 20:
        return """
User gave a short answer. This topic may not be productive.
PIVOT to a completely different angle from the tensions list.
Ask something unexpected that requires concrete thinking.
        """

    # Detailed but abstract answer - PROBE DEEPER
    elif "I think" in user_answer or "I believe" in user_answer or "usually" in user_answer:
        return """
User gave abstract/theoretical answer. Need concrete examples.
Ask for a SPECIFIC instance: "Can you walk me through the last time that happened?"
Push from theory to observable behavior.
        """

    # Detailed and concrete - CHALLENGE
    else:
        return """
User gave detailed, concrete answer. Good signal.
Now CHALLENGE the assumption or constraint they revealed.
Use "What if" scenarios to test edge of their thinking.
Example: "What if you couldn't use that approach - what would you do?"
        """


SOKRATES_QUESTION_EXAMPLES = {
    "good": [
        "When you debug a complex problem, what's the first assumption you question?",
        "You've built projects in multiple languages. Which transition taught you the most about your own learning process?",
        "Describe a moment when you realized the problem you were solving wasn't the real problem.",
        "What aspect of your work do others find easy but you find genuinely hard?",
        "If you had to explain your decision-making process to an AI, what would be the hardest part to articulate?"
    ],
    "bad": [
        "What are your strengths?",  # Too generic
        "Are you a fast learner?",  # Allows easy claims
        "What would you improve about yourself?",  # Invites clichés
        "Tell me about a time you faced a challenge.",  # Standard interview question
        "Where do you see yourself in 5 years?"  # Future speculation, not thinking pattern
    ]
}
