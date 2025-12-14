import json

# profile type configurations
PROFILE_THEMES = {
    "builder": {
        "name": "The Builder",
        "font_primary": "'JetBrains Mono', 'Fira Code', monospace",
        "font_secondary": "'Inter', sans-serif",
        "bg_primary": "#0d1117",
        "bg_secondary": "#161b22",
        "text_primary": "#c9d1d9",
        "text_secondary": "#8b949e",
        "accent": "#58a6ff",
        "success": "#3fb950",
        "warning": "#d29922",
        "card_border": "#30363d",
    },
    "creator": {
        "name": "The Creator",
        "font_primary": "'Playfair Display', 'Merriweather', serif",
        "font_secondary": "'Inter', sans-serif",
        "bg_primary": "#faf9f7",
        "bg_secondary": "#f1ede7",
        "text_primary": "#1a1a1a",
        "text_secondary": "#666666",
        "accent": "#d4491a",
        "success": "#2d6a4f",
        "warning": "#e09f3e",
        "card_border": "#ddd",
    },
    "strategist": {
        "name": "The Strategist",
        "font_primary": "'Inter', 'Helvetica Neue', sans-serif",
        "font_secondary": "'IBM Plex Mono', monospace",
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "accent": "#3b82f6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "card_border": "#e2e8f0",
    },
    "explorer": {
        "name": "The Explorer",
        "font_primary": "'Space Grotesk', 'Work Sans', sans-serif",
        "font_secondary": "'Inconsolata', monospace",
        "bg_primary": "#ffffff",
        "bg_secondary": "#fafafa",
        "text_primary": "#111827",
        "text_secondary": "#6b7280",
        "accent": "#8b5cf6",
        "success": "#059669",
        "warning": "#f97316",
        "card_border": "#e5e7eb",
    },
    "specialist": {
        "name": "The Specialist",
        "font_primary": "'Libre Baskerville', 'Georgia', serif",
        "font_secondary": "'Source Sans Pro', sans-serif",
        "bg_primary": "#fcfcfc",
        "bg_secondary": "#f5f5f5",
        "text_primary": "#2c3e50",
        "text_secondary": "#7f8c8d",
        "accent": "#2980b9",
        "success": "#27ae60",
        "warning": "#f39c12",
        "card_border": "#dcdde1",
    }
}

def detect_profile_type(data):
    """Detect profile type based on data patterns"""
    profile_type = data.get('profile_type', '').lower()
    
    # direct mapping if provided
    if profile_type in PROFILE_THEMES:
        return profile_type
    
    # infer from cognitive style and patterns
    cognitive_style = data.get('cognitive_style', '').lower()
    tagline = data.get('tagline', '').lower()
    
    # keywords for detection
    builder_keywords = ['architect', 'engineer', 'builder', 'developer', 'code', 'system', 'infrastructure']
    creator_keywords = ['creator', 'designer', 'artist', 'creative', 'visual', 'aesthetic']
    strategist_keywords = ['strategist', 'consultant', 'analyst', 'business', 'executive', 'leader']
    explorer_keywords = ['explorer', 'generalist', 'polymath', 'multi', 'diverse', 'switcher']
    specialist_keywords = ['specialist', 'expert', 'deep', 'research', 'academic', 'master']
    
    combined_text = f"{cognitive_style} {tagline}"
    
    if any(kw in combined_text for kw in builder_keywords):
        return 'builder'
    elif any(kw in combined_text for kw in creator_keywords):
        return 'creator'
    elif any(kw in combined_text for kw in strategist_keywords):
        return 'strategist'
    elif any(kw in combined_text for kw in explorer_keywords):
        return 'explorer'
    elif any(kw in combined_text for kw in specialist_keywords):
        return 'specialist'
    
    # default to builder for technical profiles
    return 'builder'


def _generate_css(theme):
    """Generate CSS with theme variables"""
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Playfair+Display:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');
        
        :root {{
            --bg-primary: {theme['bg_primary']};
            --bg-secondary: {theme['bg_secondary']};
            --text-primary: {theme['text_primary']};
            --text-secondary: {theme['text_secondary']};
            --accent: {theme['accent']};
            --success: {theme['success']};
            --warning: {theme['warning']};
            --card-border: {theme['card_border']};
            --font-primary: {theme['font_primary']};
            --font-secondary: {theme['font_secondary']};
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-secondary);
            line-height: 1.7;
            font-size: 16px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        /* HERO SECTION */
        .hero {{
            min-height: 70vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 4rem 0;
            border-bottom: 1px solid var(--card-border);
        }}
        
        .thesis {{
            max-width: 800px;
        }}
        
        .thesis h1 {{
            font-family: var(--font-primary);
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
        }}
        
        .sub-thesis {{
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 2rem;
        }}
        
        .hero-metric {{
            display: flex;
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .proof-point {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            padding: 1.5rem;
            background: var(--bg-secondary);
            border-left: 4px solid var(--accent);
            border-radius: 0 8px 8px 0;
        }}
        
        .proof-point .metric {{
            font-family: var(--font-primary);
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .proof-point .context {{
            font-size: 1rem;
            color: var(--text-primary);
        }}
        
        .proof-point .evidence {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        /* SECTIONS */
        section {{
            padding: 5rem 0;
            border-bottom: 1px solid var(--card-border);
        }}
        
        section:last-of-type {{
            border-bottom: none;
        }}
        
        h2 {{
            font-family: var(--font-primary);
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 2rem;
            color: var(--text-primary);
        }}
        
        h3 {{
            font-family: var(--font-primary);
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}
        
        /* PATTERN CARDS */
        .pattern-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .pattern-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .pattern-card:hover {{
            border-color: var(--accent);
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        }}
        
        .pattern-icon {{
            width: 48px;
            height: 48px;
            background: var(--accent);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .pattern-evidence {{
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--card-border);
        }}
        
        .evidence-metric {{
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }}
        
        .evidence-metric .value {{
            font-family: var(--font-primary);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .evidence-metric .label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        .pattern-implication {{
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(0,0,0,0.05);
            border-radius: 8px;
            font-size: 0.875rem;
        }}
        
        /* LEARNING VELOCITY */
        .velocity-section {{
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 2rem;
        }}
        
        .benchmark-grid {{
            display: grid;
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .benchmark-item {{
            display: grid;
            grid-template-columns: 200px 1fr auto;
            align-items: center;
            gap: 1rem;
        }}
        
        .benchmark-item .skill {{
            font-weight: 500;
        }}
        
        .comparison-bar {{
            height: 32px;
            background: var(--bg-primary);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}
        
        .typical-bar, .user-bar {{
            height: 16px;
            display: flex;
            align-items: center;
            padding-left: 8px;
            font-size: 0.75rem;
            color: white;
        }}
        
        .typical-bar {{
            background: var(--text-secondary);
        }}
        
        .user-bar {{
            background: var(--accent);
        }}
        
        .difference {{
            font-family: var(--font-primary);
            font-weight: 600;
            color: var(--success);
        }}
        
        .acceleration-pattern {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
            margin-top: 2rem;
            padding: 2rem;
            background: var(--bg-primary);
            border-radius: 12px;
        }}
        
        .pattern-breakdown {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .pattern-breakdown td {{
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--card-border);
        }}
        
        .pattern-breakdown td:first-child {{
            font-weight: 500;
            width: 100px;
        }}
        
        .pattern-breakdown .progress {{
            font-family: var(--font-primary);
            color: var(--accent);
            letter-spacing: 2px;
        }}
        
        /* TRAJECTORY PREDICTION */
        .investment-thesis {{
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary));
            border: 2px solid var(--accent);
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 3rem;
        }}
        
        .thesis-statement {{
            font-size: 1.25rem;
            line-height: 1.8;
            margin-bottom: 2rem;
        }}
        
        .thesis-evidence {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }}
        
        .evidence-point {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 8px;
        }}
        
        .evidence-point .icon {{
            font-size: 1.25rem;
        }}
        
        .evidence-point .text {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        /* CAPABILITY MATRIX */
        .prediction-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1.5rem;
        }}
        
        .prediction-table th {{
            text-align: left;
            padding: 1rem;
            background: var(--bg-secondary);
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .prediction-table td {{
            padding: 1.25rem 1rem;
            border-bottom: 1px solid var(--card-border);
            vertical-align: top;
        }}
        
        .prediction-table .similarity {{
            display: block;
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }}
        
        .time-estimate {{
            font-family: var(--font-primary);
            font-weight: 600;
            color: var(--accent);
        }}
        
        .timeline-visual {{
            font-family: var(--font-primary);
            color: var(--accent);
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }}
        
        .confidence {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .confidence.high {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--success);
        }}
        
        .confidence.medium {{
            background: rgba(245, 158, 11, 0.2);
            color: var(--warning);
        }}
        
        .confidence-score {{
            display: block;
            font-size: 0.875rem;
            margin-top: 0.5rem;
            color: var(--text-secondary);
        }}
        
        .reasoning {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-style: italic;
        }}
        
        /* RISK ASSESSMENT */
        .risk-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .risk-item {{
            padding: 1.5rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            border-left: 4px solid var(--warning);
        }}
        
        .risk-item h4 {{
            font-size: 1rem;
            margin-bottom: 0.75rem;
        }}
        
        .risk-item p {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}
        
        .mitigation {{
            font-size: 0.75rem;
            color: var(--success);
            font-weight: 500;
        }}
        
        /* METHODOLOGY */
        .methodology-flow {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-top: 2rem;
        }}
        
        .flow-step {{
            display: flex;
            gap: 1.5rem;
            padding: 1.5rem;
            background: var(--bg-secondary);
            border-radius: 12px;
        }}
        
        .step-number {{
            width: 40px;
            height: 40px;
            background: var(--accent);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
        }}
        
        .step-content h4 {{
            margin-bottom: 0.5rem;
        }}
        
        .step-content .behavior {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}
        
        .step-content .evidence {{
            font-size: 0.875rem;
            color: var(--accent);
            font-style: italic;
        }}
        
        .flow-arrow {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 1.5rem;
        }}
        
        /* META SECTION */
        .meta-section {{
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 2rem;
        }}
        
        .process-flow {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .process-step {{
            display: flex;
            flex-direction: column;
            padding: 1rem;
            background: var(--bg-primary);
            border-radius: 8px;
            flex: 1;
            min-width: 150px;
        }}
        
        .process-step .step-name {{
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .process-step .step-detail {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}
        
        .process-arrow {{
            color: var(--accent);
            font-size: 1.5rem;
        }}
        
        .confidence-table {{
            width: 100%;
            margin-top: 1rem;
        }}
        
        .confidence-table td {{
            padding: 0.75rem;
            border-bottom: 1px solid var(--card-border);
        }}
        
        .confidence-bar {{
            width: 100px;
            height: 8px;
            background: var(--bg-primary);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .confidence-bar > div {{
            height: 100%;
            background: var(--accent);
            border-radius: 4px;
        }}
        
        .data-sources ul {{
            list-style: none;
            margin-top: 1rem;
        }}
        
        .data-sources li {{
            padding: 0.5rem 0;
            color: var(--text-secondary);
        }}
        
        /* CHART CONTAINERS */
        .chart-container {{
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 16px;
            margin-top: 2rem;
        }}
        
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
        }}
        
        /* FOOTER */
        footer {{
            text-align: center;
            padding: 3rem 0;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
        
        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .container {{
                padding: 0 1rem;
            }}
            
            .hero {{
                min-height: auto;
                padding: 3rem 0;
            }}
            
            .thesis h1 {{
                font-size: 1.75rem;
            }}
            
            .benchmark-item {{
                grid-template-columns: 1fr;
            }}
            
            .acceleration-pattern {{
                grid-template-columns: 1fr;
            }}
            
            .process-flow {{
                flex-direction: column;
            }}
            
            .process-arrow {{
                transform: rotate(90deg);
            }}
            
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* ANIMATIONS */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate-in {{
            animation: fadeInUp 0.6s ease forwards;
        }}
        
        section {{
            opacity: 0;
        }}
        
        section.visible {{
            animation: fadeInUp 0.6s ease forwards;
        }}
    </style>
    """


def _generate_hero_section(data, theme, user_name="Professional"):
    """Generate the hero section with thesis statement"""
    cognitive_style = data.get('cognitive_style', 'Professional Profile')
    tagline = data.get('tagline', 'Defining the undefined.')
    learning_velocity = data.get('learning_velocity', {})
    
    time_to_competency = learning_velocity.get('timeToCompetency', '6-8 weeks per new domain')
    
    # get key metrics for proof point
    skills = data.get('skills_matrix', {})
    top_skill = max(skills.items(), key=lambda x: x[1])[0] if skills else "Technical Skills"
    top_score = max(skills.values()) if skills else 85
    
    # remove "The " prefix from tagline if present
    if tagline.startswith("The "):
        tagline = tagline[4:]
    
    return f"""
    <section class="hero">
        <div class="container">
            <div class="thesis">
                <p style="color: var(--accent); font-family: var(--font-primary); font-size: 0.875rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1rem;">
                    {user_name.upper()}
                </p>
                <h1>{cognitive_style}</h1>
                <p class="sub-thesis">{tagline}</p>
                <p class="sub-thesis" style="color: var(--accent);">Learning velocity: {time_to_competency}</p>
            </div>
            
            <div class="hero-metric">
                <div class="proof-point">
                    <span class="metric">{top_score}%</span>
                    <span class="context">Peak competency in {top_skill}</span>
                    <span class="evidence">Verified through interview analysis & data synthesis</span>
                </div>
            </div>
        </div>
    </section>
    """


def _generate_cognitive_fingerprint(data, theme):
    """Generate the cognitive fingerprint section with pattern cards"""
    patterns = data.get('core_patterns', [])
    
    pattern_icons = ['*', '+', '>', '~', '#']
    
    cards_html = ""
    for i, pattern in enumerate(patterns):
        if isinstance(pattern, dict):
            title = pattern.get('title', 'Pattern')
            desc = pattern.get('description', '')
        else:
            title = f"Pattern {i+1}"
            desc = str(pattern)
        
        icon = pattern_icons[i % len(pattern_icons)]
        
        cards_html += f"""
        <div class="pattern-card">
            <div class="pattern-icon">{icon}</div>
            <h3>{title}</h3>
            <p style="color: var(--text-secondary);">{desc}</p>
            <div class="pattern-implication">
                <strong>What this means:</strong>
                <p style="margin-top: 0.5rem;">This pattern reveals a consistent approach to problem-solving and learning.</p>
            </div>
        </div>
        """
    
    return f"""
    <section class="cognitive-fingerprint">
        <div class="container">
            <h2>How This Person Thinks</h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Cognitive patterns extracted from interview responses and behavioral analysis
            </p>
            <div class="pattern-grid">
                {cards_html}
            </div>
        </div>
    </section>
    """


def _generate_learning_velocity(data, theme):
    """Generate the learning velocity section with charts and benchmarks"""
    learning_velocity = data.get('learning_velocity', {})
    
    time_to_competency = learning_velocity.get('timeToCompetency', '6-8 weeks')
    acceleration_pattern = learning_velocity.get('accelerationPattern', 'slow-start-then-rapid')
    transfer_learning = learning_velocity.get('transferLearning', 'medium')
    
    # pattern descriptions
    pattern_descriptions = {
        'slow-start-then-rapid': ('Slow Start, Rapid Acceleration', 'Invests heavily in fundamentals before building velocity'),
        'steady-linear': ('Steady Linear Growth', 'Consistent, predictable progress over time'),
        'fast-plateau': ('Fast Start, Plateau Risk', 'Quick initial gains but may hit ceilings')
    }
    
    pattern_name, pattern_desc = pattern_descriptions.get(
        acceleration_pattern, 
        ('Adaptive Learner', 'Adjusts learning approach based on domain')
    )
    
    transfer_descriptions = {
        'high': 'Excellent ability to apply knowledge across domains',
        'medium': 'Good transfer capability with some ramp-up time',
        'low': 'Prefers deep specialization over broad application'
    }
    
    return f"""
    <section class="learning-velocity">
        <div class="container">
            <h2>Learning Velocity Analysis</h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                How quickly this person acquires new skills and adapts to new domains
            </p>
            
            <div class="velocity-section">
                <h3>Time to Competency</h3>
                <p style="font-size: 2rem; font-weight: 700; color: var(--accent); margin: 1rem 0;">{time_to_competency}</p>
                <p style="color: var(--text-secondary);">Average time to reach working proficiency in a new technical domain</p>
            </div>
            
            <div class="acceleration-pattern">
                <div>
                    <h3>Acceleration Pattern</h3>
                    <p style="font-size: 1.25rem; font-weight: 600; margin: 1rem 0;">{pattern_name}</p>
                    <p style="color: var(--text-secondary);">{pattern_desc}</p>
                </div>
                <div>
                    <table class="pattern-breakdown">
                        <tr>
                            <td>Week 1-2:</td>
                            <td>Research & foundational understanding</td>
                            <td class="progress">▓░░░░</td>
                        </tr>
                        <tr>
                            <td>Week 3-4:</td>
                            <td>First implementations & experimentation</td>
                            <td class="progress">▓▓▓░░</td>
                        </tr>
                        <tr>
                            <td>Week 5-8:</td>
                            <td>Rapid capability expansion</td>
                            <td class="progress">▓▓▓▓▓</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div class="velocity-section" style="margin-top: 2rem;">
                <h3>Transfer Learning Capability</h3>
                <p style="font-size: 1.5rem; font-weight: 600; color: var(--accent); margin: 1rem 0;">{transfer_learning.upper()}</p>
                <p style="color: var(--text-secondary);">{transfer_descriptions.get(transfer_learning, 'Adaptable across contexts')}</p>
            </div>
        </div>
    </section>
    """


def _generate_trajectory_prediction(data, theme):
    """Generate the trajectory prediction section"""
    growth_trajectory = data.get('growth_trajectory', {})
    hiring_insight = data.get('hiring_insight', {})
    learning_velocity = data.get('learning_velocity', {})
    
    # extract data
    current_phase = growth_trajectory.get('currentPhase', 'Analyzing...')
    natural_direction = growth_trajectory.get('naturalDirection', 'Growth trajectory under analysis')
    high_leverage_gap = growth_trajectory.get('highLeverageGap', 'Under analysis')
    readiness_indicators = growth_trajectory.get('readinessIndicators', [])
    
    best_fit_role = hiring_insight.get('bestFitRole', 'TBD')
    potential_risks = hiring_insight.get('potentialRisks', 'Under evaluation')
    investment_thesis = hiring_insight.get('investmentThesis', 'Analyzing growth potential...')
    
    # generate readiness indicators html
    indicators_html = ""
    for indicator in readiness_indicators[:3]:
        indicators_html += f"""
        <div class="evidence-point">
            <span class="icon">*</span>
            <span class="text">{indicator}</span>
        </div>
        """
    
    return f"""
    <section class="trajectory-prediction">
        <div class="container">
            <h2>Predictive Growth Model</h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Forward-looking analysis based on observed patterns and behavioral indicators
            </p>
            
            <div class="investment-thesis">
                <h3>Why Invest in This Person's Growth</h3>
                <div class="thesis-statement">
                    {investment_thesis}
                </div>
                <div class="thesis-evidence">
                    <div class="evidence-point">
                        <span class="icon">[1]</span>
                        <span class="text">Demonstrated consistent learning velocity across domains</span>
                    </div>
                    <div class="evidence-point">
                        <span class="icon">[2]</span>
                        <span class="text">High transfer learning capability</span>
                    </div>
                    <div class="evidence-point">
                        <span class="icon">[3]</span>
                        <span class="text">Accelerating trajectory pattern detected</span>
                    </div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem;">
                <div class="velocity-section">
                    <h3>Current Phase</h3>
                    <p style="margin-top: 1rem;">{current_phase}</p>
                </div>
                <div class="velocity-section">
                    <h3>Natural Direction</h3>
                    <p style="margin-top: 1rem;">{natural_direction}</p>
                </div>
            </div>
            
            <div class="velocity-section" style="margin-top: 2rem; border-left: 4px solid var(--accent); border-radius: 0 12px 12px 0;">
                <h3>High-Leverage Gap</h3>
                <p style="margin-top: 1rem; font-size: 1.125rem;">{high_leverage_gap}</p>
                <p style="color: var(--text-secondary); margin-top: 0.5rem; font-size: 0.875rem;">
                    Addressing this gap would unlock significant growth potential
                </p>
            </div>
            
            <div style="margin-top: 2rem;">
                <h3>Best Fit Role</h3>
                <p style="font-size: 1.5rem; font-weight: 600; color: var(--accent); margin: 1rem 0;">{best_fit_role}</p>
            </div>
            
            <div class="risk-grid">
                <div class="risk-item">
                    <h4>Potential Risks</h4>
                    <p>{potential_risks}</p>
                    <span class="mitigation">Mitigation: Set clear expectations and provide structured feedback</span>
                </div>
            </div>
            
            {f'''<div style="margin-top: 2rem;">
                <h3>Readiness Indicators</h3>
                <div class="thesis-evidence" style="margin-top: 1rem;">
                    {indicators_html}
                </div>
            </div>''' if indicators_html else ''}
        </div>
    </section>
    """


def _generate_skills_chart(data, theme):
    """Generate the skills/competency chart section"""
    skills = data.get('skills_matrix', {})
    growth = data.get('growth_focus', 'Continuous learning')
    the_bet = data.get('the_bet', 'High potential for growth.')
    anti_patterns = data.get('anti_patterns', [])
    
    skill_labels = list(skills.keys()) if isinstance(skills, dict) else []
    skill_values = list(skills.values()) if isinstance(skills, dict) else []
    
    # anti-patterns html
    anti_patterns_html = ""
    for pattern in anti_patterns:
        if isinstance(pattern, dict):
            title = pattern.get('title', 'Anti-Pattern')
            desc = pattern.get('description', '')
        else:
            title = "Boundary"
            desc = str(pattern)
        anti_patterns_html += f"""
        <div style="padding: 1rem; background: var(--bg-secondary); border-radius: 8px; border-left: 3px solid var(--warning);">
            <h4 style="font-size: 0.875rem; margin-bottom: 0.5rem;">{title}</h4>
            <p style="font-size: 0.875rem; color: var(--text-secondary);">{desc}</p>
        </div>
        """
    
    return f"""
    <section class="skills-section">
        <div class="container">
            <h2>Competency Matrix</h2>
            
            <div class="chart-grid">
                <div class="chart-container">
                    <h3>Skills Radar</h3>
                    <canvas id="skillsChart"></canvas>
                </div>
                
                <div>
                    <div class="velocity-section">
                        <h3>Current Growth Focus</h3>
                        <p style="margin-top: 1rem; font-size: 1.125rem; color: var(--accent);">{growth}</p>
                    </div>
                    
                    <div style="margin-top: 2rem;">
                        <h3>Professional Boundaries (The "No")</h3>
                        <div style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem;">
                            {anti_patterns_html}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="investment-thesis" style="margin-top: 3rem;">
                <h3>The Alpha - Why Invest?</h3>
                <p style="font-size: 1.25rem; line-height: 1.8; margin-top: 1rem;">
                    "{the_bet}"
                </p>
            </div>
        </div>
    </section>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const ctx = document.getElementById('skillsChart').getContext('2d');
            new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: {json.dumps(skill_labels)},
                    datasets: [{{
                        label: 'Proficiency',
                        data: {json.dumps(skill_values)},
                        backgroundColor: '{theme["accent"]}33',
                        borderColor: '{theme["accent"]}',
                        borderWidth: 2,
                        pointBackgroundColor: '{theme["accent"]}',
                        pointBorderColor: '#fff',
                        pointRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{
                                stepSize: 20,
                                color: '{theme["text_secondary"]}'
                            }},
                            grid: {{
                                color: '{theme["card_border"]}'
                            }},
                            angleLines: {{
                                color: '{theme["card_border"]}'
                            }},
                            pointLabels: {{
                                color: '{theme["text_primary"]}',
                                font: {{
                                    size: 12,
                                    family: "{theme['font_secondary']}"
                                }}
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});
        }});
    </script>
    """


def _generate_meta_section(data, theme):
    """Generate the meta section with methodology and transparency"""
    return f"""
    <section class="meta">
        <div class="container">
            <div class="meta-section">
                <h2>About This Portfolio</h2>
                
                <div>
                    <h3>How This Was Generated</h3>
                    <div class="process-flow">
                        <div class="process-step">
                            <span class="step-name">Maieutic Interview</span>
                            <span class="step-detail">AI-guided questions designed to reveal thinking patterns</span>
                        </div>
                        <span class="process-arrow">→</span>
                        <div class="process-step">
                            <span class="step-name">Data Analysis</span>
                            <span class="step-detail">Multi-source data extraction and synthesis</span>
                        </div>
                        <span class="process-arrow">→</span>
                        <div class="process-step">
                            <span class="step-name">Pattern Synthesis</span>
                            <span class="step-detail">AI extracted cognitive patterns from combined data</span>
                        </div>
                        <span class="process-arrow">→</span>
                        <div class="process-step">
                            <span class="step-name">Prediction Model</span>
                            <span class="step-detail">Learning velocity calculated from historical patterns</span>
                        </div>
                    </div>
                </div>
                
                <div style="margin-top: 2rem;">
                    <h3>Confidence Levels</h3>
                    <table class="confidence-table">
                        <tr>
                            <td>Cognitive Patterns</td>
                            <td><div class="confidence-bar"><div style="width: 85%"></div></div></td>
                            <td>85%</td>
                            <td style="color: var(--text-secondary); font-size: 0.875rem;">High - Based on interview consistency</td>
                        </tr>
                        <tr>
                            <td>Learning Velocity</td>
                            <td><div class="confidence-bar"><div style="width: 75%"></div></div></td>
                            <td>75%</td>
                            <td style="color: var(--text-secondary); font-size: 0.875rem;">Medium-High - Based on available data points</td>
                        </tr>
                        <tr>
                            <td>Growth Trajectory</td>
                            <td><div class="confidence-bar"><div style="width: 70%"></div></div></td>
                            <td>70%</td>
                            <td style="color: var(--text-secondary); font-size: 0.875rem;">Medium-High - Based on patterns, subject to change</td>
                        </tr>
                    </table>
                </div>
                
                <div class="data-sources" style="margin-top: 2rem;">
                    <h3>Data Sources</h3>
                    <ul>
                        <li>* SOKRATES interview responses</li>
                        <li>* Uploaded documents analysis</li>
                        <li>* Multi-source pattern extraction</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    """


def generate_anti_portfolio_html(data, user_name="Professional"):
    """
    Generates a rich, interactive HTML file for the Anti-Portfolio.
    Implements the new adaptive, data-driven design.
    """
    
    # Detect profile type and get theme
    profile_type = detect_profile_type(data)
    theme = PROFILE_THEMES.get(profile_type, PROFILE_THEMES['builder'])
    
    # Build HTML document
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOKRATES Anti-Portfolio | {data.get('cognitive_style', 'Professional Profile')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {_generate_css(theme)}
</head>
<body>
    {_generate_hero_section(data, theme, user_name)}
    
    {_generate_cognitive_fingerprint(data, theme)}
    
    {_generate_learning_velocity(data, theme)}
    
    {_generate_trajectory_prediction(data, theme)}
    
    {_generate_skills_chart(data, theme)}
    
    {_generate_meta_section(data, theme)}
    
    <footer class="container">
        <p>Generated by SOKRATES // The Anti-Portfolio Generator // {profile_type.upper()} Profile</p>
        <p style="margin-top: 0.5rem; font-size: 0.75rem;">This is not a resume. This is a trajectory map.</p>
    </footer>
    
    <script>
        // Scroll animation observer
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }});
        
        document.querySelectorAll('section').forEach(section => {{
            observer.observe(section);
        }});
        
        // Make first section visible immediately
        document.querySelector('section').classList.add('visible');
    </script>
</body>
</html>"""
    
    return html_content
