import json

def _generate_trajectory_section(learning_velocity, growth_trajectory, hiring_insight):
    """Generate HTML for the trajectory and prediction section"""

    # Extract trajectory data
    current_phase = growth_trajectory.get('currentPhase', 'Analyzing...')
    natural_direction = growth_trajectory.get('naturalDirection', 'TBD')
    high_leverage_gap = growth_trajectory.get('highLeverageGap', 'Under analysis')
    readiness_indicators = growth_trajectory.get('readinessIndicators', [])

    # Extract hiring insights
    best_fit_role = hiring_insight.get('bestFitRole', 'TBD')
    potential_risks = hiring_insight.get('potentialRisks', 'Under evaluation')
    investment_thesis = hiring_insight.get('investmentThesis', 'Analyzing growth potential...')

    # Extract learning velocity
    time_to_competency = learning_velocity.get('timeToCompetency', 'Analyzing...')
    acceleration_pattern = learning_velocity.get('accelerationPattern', 'unknown')
    transfer_learning = learning_velocity.get('transferLearning', 'medium')

    # Format readiness indicators
    indicators_html = ""
    if isinstance(readiness_indicators, list) and readiness_indicators:
        indicators_html = "<ul style='margin-top: 1rem; padding-left: 1.5rem;'>"
        for indicator in readiness_indicators:
            indicators_html += f"<li>{indicator}</li>"
        indicators_html += "</ul>"

    return f"""
        <section style="margin-top: 4rem; border-top: 2px solid var(--accent-color); padding-top: 3rem;">
            <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;">
                Growth Trajectory & Predictions
            </h2>

            <div class="grid">
                <div class="item" style="background: linear-gradient(135deg, #1a1a1a, #111);">
                    <span class="meta-label">CURRENT STATE</span>
                    <h3>Where They Are Now</h3>
                    <p>{current_phase}</p>
                </div>

                <div class="item" style="background: linear-gradient(135deg, #1a1a1a, #111);">
                    <span class="meta-label">NATURAL TRAJECTORY</span>
                    <h3>Where They're Headed</h3>
                    <p>{natural_direction}</p>
                </div>
            </div>

            <div class="grid" style="margin-top: 2rem;">
                <div class="item" style="border-color: var(--accent-color);">
                    <span class="meta-label">HIGH-LEVERAGE GAP</span>
                    <h3>Unlock Next Level</h3>
                    <p>{high_leverage_gap}</p>
                </div>

                <div class="item">
                    <span class="meta-label">LEARNING VELOCITY</span>
                    <h3>Speed to Competency</h3>
                    <p><strong>Time to Mastery:</strong> {time_to_competency}</p>
                    <p><strong>Pattern:</strong> {acceleration_pattern}</p>
                    <p><strong>Transfer Learning:</strong> {transfer_learning.upper()}</p>
                </div>
            </div>

            <div style="margin-top: 2rem; padding: 2rem; background: var(--card-bg); border-left: 4px solid var(--accent-color);">
                <span class="meta-label">READINESS INDICATORS</span>
                <h3>Signals of Growth Capacity</h3>
                {indicators_html if indicators_html else '<p>Analyzing behavioral patterns...</p>'}
            </div>

            <div style="margin-top: 2rem;">
                <div class="item" style="background: linear-gradient(135deg, #0a0a0a, #1a1a1a);">
                    <span class="meta-label">HIRING INTELLIGENCE</span>
                    <h3>Best Fit: {best_fit_role}</h3>
                    <p><strong>Investment Thesis:</strong> {investment_thesis}</p>
                    <p style="margin-top: 1rem; color: #ff6666;"><strong>Potential Risks:</strong> {potential_risks}</p>
                </div>
            </div>
        </section>
    """

def generate_anti_portfolio_html(data):
    """
    Generates a rich, interactive HTML file for the Anti-Portfolio.
    """
    
    # Extract data with defaults
    cognitive_style = data.get('cognitive_style', 'Unknown Archetype')
    tagline = data.get('tagline', 'Defining the undefined.')
    patterns = data.get('core_patterns', []) # List of {title, desc} or strings
    anti_patterns = data.get('anti_patterns', [])
    skills = data.get('skills_matrix', {})
    growth = data.get('growth_focus', 'TBD')
    the_bet = data.get('the_bet', 'No analysis available.')
    visual_metaphor = data.get('visual_metaphor', 'Abstract void')

    # NEW: Learning velocity and trajectory data
    learning_velocity = data.get('learning_velocity', {})
    growth_trajectory = data.get('growth_trajectory', {})
    hiring_insight = data.get('hiring_insight', {})

    # Prepare Skills Data for Chart.js
    skill_labels = list(skills.keys()) if isinstance(skills, dict) else []
    skill_values = list(skills.values()) if isinstance(skills, dict) else []
    
    # Helper to format list items (handling both strings and objects if LLM messes up)
    def format_list(items):
        html = ""
        for item in items:
            if isinstance(item, dict):
                title = item.get('title', list(item.keys())[0] if item else 'Point')
                desc = item.get('description', list(item.values())[0] if item else '')
                html += f'<div class="item"><h3>{title}</h3><p>{desc}</p></div>'
            else:
                html += f'<div class="item"><p>{item}</p></div>'
        return html

    patterns_html = format_list(patterns)
    anti_patterns_html = format_list(anti_patterns)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anti-Portfolio | {cognitive_style}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #050505;
            --card-bg: #111;
            --text-color: #e0e0e0;
            --accent-color: #ff3333; /* Red for Anti-Portfolio vibe */
            --secondary-color: #444;
            --font-display: 'Helvetica Neue', sans-serif;
            --font-mono: 'Courier New', monospace;
        }}
        
        * {{ box_sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: var(--font-display);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* HERO SECTION */
        header {{
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-bottom: 1px solid var(--secondary-color);
            position: relative;
        }}
        
        .meta-label {{
            font-family: var(--font-mono);
            color: var(--accent-color);
            font-size: 0.9rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 5rem;
            line-height: 1;
            font-weight: 800;
            letter-spacing: -3px;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #fff, #666);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .tagline {{
            font-size: 1.5rem;
            color: #888;
            max-width: 600px;
        }}
        
        /* GRID LAYOUT */
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            margin-top: 4rem;
        }}
        
        section {{ margin-bottom: 6rem; }}
        
        h2 {{
            font-size: 2rem;
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-color);
            padding-left: 1rem;
        }}
        
        /* PATTERNS */
        .item {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: var(--card-bg);
            border: 1px solid #222;
            transition: transform 0.2s;
        }}
        
        .item:hover {{
            transform: translateX(10px);
            border-color: var(--accent-color);
        }}
        
        .item h3 {{
            font-family: var(--font-mono);
            color: #fff;
            margin-bottom: 0.5rem;
        }}
        
        /* CHART SECTION */
        .chart-container {{
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 10px;
        }}
        
        /* THE BET */
        .bet-section {{
            background: linear-gradient(45deg, #111, #1a1a1a);
            padding: 4rem;
            border: 1px solid var(--accent-color);
            text-align: center;
        }}
        
        .bet-text {{
            font-size: 1.8rem;
            font-weight: 300;
            color: #fff;
        }}
        
        /* VISUAL METAPHOR */
        .metaphor {{
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: #555;
            margin-top: 2rem;
            text-align: center;
        }}

        @media (max-width: 768px) {{
            h1 {{ font-size: 3rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <div class="container">
        <header>
            <span class="meta-label">Professional Fingerprint // ID: {str(hash(cognitive_style))[:8]}</span>
            <h1>{cognitive_style}</h1>
            <p class="tagline">{tagline}</p>
        </header>

        <div class="grid">
            <section>
                <h2>Core Patterns</h2>
                {patterns_html}
            </section>
            
            <section>
                <h2>Anti-Patterns (The "No")</h2>
                {anti_patterns_html}
            </section>
        </div>

        <div class="grid">
            <section>
                <h2>Competency Matrix</h2>
                <div class="chart-container">
                    <canvas id="skillsChart"></canvas>
                </div>
            </section>
            
            <section>
                <h2>Growth Focus</h2>
                <div class="item" style="border-color: var(--accent-color);">
                    <h3>Current Frontier</h3>
                    <p>{growth}</p>
                </div>
                <div class="metaphor">
                    VISUAL METAPHOR: "{visual_metaphor}"
                </div>
            </section>
        </div>

        <section class="bet-section">
            <span class="meta-label">THE ALPHA</span>
            <h2>Why Invest?</h2>
            <p class="bet-text">"{the_bet}"</p>
        </section>

        {_generate_trajectory_section(learning_velocity, growth_trajectory, hiring_insight)}

        <footer>
            GENERATED BY SOKRATES // 2025
        </footer>
    </div>

    <script>
        const ctx = document.getElementById('skillsChart').getContext('2d');
        new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(skill_labels)},
                datasets: [{{
                    label: 'Proficiency / Intensity',
                    data: {json.dumps(skill_values)},
                    backgroundColor: 'rgba(255, 51, 51, 0.2)',
                    borderColor: 'rgba(255, 51, 51, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#fff'
                }}]
            }},
            options: {{
                scales: {{
                    r: {{
                        angleLines: {{ color: '#333' }},
                        grid: {{ color: '#333' }},
                        pointLabels: {{
                            color: '#fff',
                            font: {{ size: 12, family: 'Courier New' }}
                        }},
                        ticks: {{ display: false, backdropColor: 'transparent' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html_content
