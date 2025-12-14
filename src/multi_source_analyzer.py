"""
Multi-Source Data Analyzer for SOKRATES
Analyzes portfolios, CVs, LinkedIn, personal sites with the same rigor as GitHub
"""

import re
from datetime import datetime
from collections import defaultdict
import json


class MultiSourceAnalyzer:
    """
    Analyzes various data sources to extract learning velocity patterns
    Works with: CVs, LinkedIn PDFs, Portfolio sites, Project descriptions
    """

    def __init__(self):
        self.data = {
            'timeline_events': [],
            'skill_mentions': defaultdict(list),
            'project_complexity': [],
            'role_transitions': [],
            'education_progression': [],
            'learning_signals': []
        }

    def analyze_text(self, text, source_type="general"):
        """
        Main analysis entry point for text-based sources

        Args:
            text: Raw text from CV, LinkedIn, portfolio, etc.
            source_type: Type of source (cv, linkedin, portfolio, website)

        Returns:
            dict: Comprehensive analysis of learning patterns
        """
        # Extract timeline events
        self._extract_timeline(text)

        # Extract skills and technologies
        self._extract_skills(text)

        # Extract projects and complexity indicators
        self._extract_projects(text)

        # Extract education and certifications
        self._extract_education(text)

        # Detect role transitions and career pivots
        self._detect_transitions(text)

        # Identify learning signals
        self._identify_learning_signals(text)

        return self._compile_analysis()

    def _extract_timeline(self, text):
        """Extract dated events and create timeline"""
        # Date patterns: 2020-2023, Jan 2020, 2020-Present, etc.
        date_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|Present|present|Current|current)',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})',
            r'(\d{4})',
        ]

        lines = text.split('\n')
        for i, line in enumerate(lines):
            for pattern in date_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Get context (surrounding lines)
                    context_start = max(0, i - 1)
                    context_end = min(len(lines), i + 3)
                    context = ' '.join(lines[context_start:context_end])

                    self.data['timeline_events'].append({
                        'date_match': match.group(0),
                        'context': context.strip()[:300],  # Limit context length
                        'line': line.strip()
                    })

    def _extract_skills(self, text):
        """Extract technical and soft skills with context"""
        # Common skill categories and keywords
        skill_categories = {
            'programming_languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C\\+\\+', 'C#', 'C', 'Ruby',
                'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'Scala', 'R', 'MATLAB', 'Julia',
                'Perl', 'Bash', 'Shell', 'SQL', 'HTML', 'CSS'
            ],
            'frameworks': [
                'React', 'Vue', 'Angular', 'Node', 'Django', 'Flask', 'FastAPI',
                'Spring', 'Rails', '.NET', 'Express', 'Next\\.js', 'Svelte', 'Laravel',
                'ASP\\.NET', 'Bootstrap', 'Tailwind', 'jQuery'
            ],
            'databases': [
                'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
                'DynamoDB', 'Cassandra', 'Oracle', 'SQL Server', 'SQLite', 'MariaDB',
                'Neo4j', 'InfluxDB', 'CouchDB'
            ],
            'cloud': [
                'AWS', 'Azure', 'GCP', 'Google Cloud', 'Heroku', 'Vercel',
                'Docker', 'Kubernetes', 'Terraform', 'CloudFormation', 'Ansible',
                'Jenkins', 'GitLab', 'CircleCI', 'Travis'
            ],
            'data_science': [
                'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
                'scikit-learn', 'Pandas', 'NumPy', 'Data Analysis', 'Data Science',
                'AI', 'Artificial Intelligence', 'Neural Network', 'NLP', 'Computer Vision',
                'Keras', 'XGBoost', 'LightGBM', 'Jupyter', 'Matplotlib', 'Seaborn',
                'Statistics', 'Statistical Analysis', 'Predictive Modeling'
            ],
            'design': [
                'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator',
                'UI/UX', 'UX', 'UI', 'User Research', 'Prototyping', 'Wireframing',
                'Design Systems', 'User Experience', 'User Interface'
            ],
            'tools': [
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'JIRA', 'Confluence',
                'Slack', 'Trello', 'Asana', 'VS Code', 'IntelliJ', 'PyCharm',
                'Vim', 'Emacs', 'Postman', 'Insomnia'
            ],
            'methodologies': [
                'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD',
                'Test Driven Development', 'Continuous Integration', 'Continuous Deployment',
                'Microservices', 'REST', 'GraphQL', 'API', 'Serverless'
            ],
            'soft_skills': [
                'leadership', 'communication', 'collaboration', 'mentoring',
                'problem solving', 'strategic thinking', 'project management',
                'team work', 'teamwork', 'analytical', 'critical thinking',
                'time management', 'adaptability', 'creativity'
            ]
        }

        # Convert text to lowercase for case-insensitive matching, but keep original for context
        text_lower = text.lower()

        for category, skills in skill_categories.items():
            for skill in skills:
                # Create flexible pattern (case insensitive, word boundary)
                pattern = r'\b' + skill.replace('.', r'\.') + r'\b'
                matches = re.finditer(pattern, text, re.IGNORECASE)

                found_match = False
                for match in matches:
                    found_match = True
                    # Get surrounding context
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end]

                    # Store with normalized skill name
                    skill_key = skill.lower().replace(r'\.', '.')
                    self.data['skill_mentions'][skill_key].append({
                        'category': category,
                        'context': context.strip(),
                        'position': match.start()
                    })

    def _extract_projects(self, text):
        """Extract project descriptions and complexity indicators"""
        # Keywords that often indicate project descriptions
        project_indicators = [
            r'(?:built|developed|created|designed|implemented|launched|shipped|delivered|engineered|architected)\s+(?:a|an|the)?\s*[\w\s]{10,150}',
            r'project:?\s*.{20,200}',
            r'(?:led|managed|coordinated|supervised|directed)\s+.{20,150}',
            r'(?:worked on|contributed to|participated in)\s+.{20,150}',
            r'(?:responsible for|in charge of)\s+.{20,150}',
        ]

        seen_descriptions = set()  # Avoid duplicates

        for pattern in project_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                description = match.group(0).strip()[:200]

                # Skip if too short or already seen
                if len(description) < 20 or description in seen_descriptions:
                    continue

                seen_descriptions.add(description)

                # Extract complexity signals
                complexity_signals = self._assess_project_complexity(description)

                self.data['project_complexity'].append({
                    'description': description,
                    'complexity_score': complexity_signals['score'],
                    'signals': complexity_signals['indicators']
                })

    def _assess_project_complexity(self, text):
        """Assess project complexity based on keywords and patterns"""
        complexity_indicators = {
            'scale': ['scalable', 'distributed', 'microservices', 'large-scale', 'enterprise'],
            'technical': ['architecture', 'infrastructure', 'optimization', 'performance', 'security'],
            'impact': ['users', 'customers', 'revenue', 'growth', 'adoption'],
            'innovation': ['novel', 'innovative', 'first', 'pioneering', 'breakthrough'],
            'collaboration': ['team', 'cross-functional', 'stakeholders', 'collaborated', 'led']
        }

        score = 0
        found_indicators = []

        for category, keywords in complexity_indicators.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                    score += 1
                    found_indicators.append(f"{category}:{keyword}")

        return {
            'score': min(score, 10),  # Normalize to 0-10
            'indicators': found_indicators
        }

    def _extract_education(self, text):
        """Extract education and learning timeline"""
        # Education keywords
        education_patterns = [
            r'(Bachelor|Master|PhD|Doctorate|BSc|MSc|BA|MA)(?:\s+(?:of|in))?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(University|College|Institute)\s+of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(Certified|Certification)\s+(?:in\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(Coursera|Udemy|edX|Pluralsight):\s*(.{10,100})',
        ]

        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.data['education_progression'].append({
                    'type': match.group(1),
                    'subject': match.group(2) if len(match.groups()) > 1 else 'Unknown',
                    'full_match': match.group(0)
                })

    def _detect_transitions(self, text):
        """Detect career transitions and pivots"""
        # Role progression keywords
        role_levels = {
            'junior': ['junior', 'associate', 'intern', 'trainee', 'assistant'],
            'mid': ['developer', 'engineer', 'designer', 'analyst', 'specialist'],
            'senior': ['senior', 'lead', 'principal', 'staff'],
            'leadership': ['manager', 'director', 'head of', 'vp', 'chief', 'founder', 'co-founder']
        }

        # Look for role mentions with dates
        lines = text.split('\n')
        for line in lines:
            for level, keywords in role_levels.items():
                for keyword in keywords:
                    if re.search(r'\b' + keyword + r'\b', line, re.IGNORECASE):
                        # Try to extract date from same line or nearby
                        date_match = re.search(r'\d{4}', line)
                        self.data['role_transitions'].append({
                            'level': level,
                            'keyword': keyword,
                            'line': line.strip()[:200],
                            'year': date_match.group(0) if date_match else None
                        })

    def _identify_learning_signals(self, text):
        """Identify implicit learning and growth signals"""
        learning_signal_patterns = {
            'experimentation': [
                r'experimented with', r'explored', r'tried', r'prototyped',
                r'proof of concept', r'side project', r'hackathon'
            ],
            'mastery': [
                r'deep dive', r'expertise in', r'specialized in', r'mastered',
                r'comprehensive understanding', r'advanced'
            ],
            'teaching': [
                r'mentored', r'taught', r'trained', r'documented', r'presented',
                r'wrote about', r'blogged', r'spoke at'
            ],
            'problem_solving': [
                r'solved', r'debugged', r'optimized', r'improved', r'reduced',
                r'increased', r'fixed', r'resolved'
            ],
            'ownership': [
                r'owned', r'responsible for', r'drove', r'initiated', r'founded',
                r'launched', r'shipped', r'delivered'
            ]
        }

        for signal_type, patterns in learning_signal_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Get context
                    start = max(0, match.start() - 80)
                    end = min(len(text), match.end() + 80)
                    context = text[start:end]

                    self.data['learning_signals'].append({
                        'type': signal_type,
                        'pattern': pattern,
                        'context': context.strip()
                    })

    def _compile_analysis(self):
        """Compile all extracted data into structured analysis"""
        # Calculate timeline span
        years = set()
        for event in self.data['timeline_events']:
            year_matches = re.findall(r'\d{4}', event['date_match'])
            years.update(year_matches)

        timeline_span = {
            'earliest_year': min(years) if years else None,
            'latest_year': max(years) if years else None,
            'total_years': int(max(years)) - int(min(years)) if len(years) > 1 else 0
        }

        # Aggregate skills by category
        skills_by_category = defaultdict(list)
        for skill, mentions in self.data['skill_mentions'].items():
            if mentions:  # Only include skills that were actually found
                category = mentions[0]['category']
                skills_by_category[category].append({
                    'skill': skill,
                    'mention_count': len(mentions)
                })

        # Calculate learning velocity indicators
        learning_velocity = self._calculate_learning_velocity_indicators()

        return {
            'timeline': {
                'span': timeline_span,
                'events': self.data['timeline_events'][:20],  # Limit to recent events
            },
            'skills': {
                'by_category': dict(skills_by_category),
                'total_unique_skills': len(self.data['skill_mentions']),
                'most_mentioned': sorted(
                    [{'skill': k, 'count': len(v)} for k, v in self.data['skill_mentions'].items()],
                    key=lambda x: x['count'],
                    reverse=True
                )[:10]
            },
            'projects': {
                'total': len(self.data['project_complexity']),
                'complexity_distribution': self._get_complexity_distribution(),
                'top_projects': sorted(
                    self.data['project_complexity'],
                    key=lambda x: x['complexity_score'],
                    reverse=True
                )[:5]
            },
            'education': {
                'formal': [e for e in self.data['education_progression'] if e['type'] in ['Bachelor', 'Master', 'PhD']],
                'certifications': [e for e in self.data['education_progression'] if 'Certified' in e['type']],
                'online_learning': [e for e in self.data['education_progression'] if e['type'] in ['Coursera', 'Udemy', 'edX']]
            },
            'career_progression': {
                'transitions': self.data['role_transitions'],
                'progression_detected': self._detect_progression_pattern()
            },
            'learning_signals': {
                'by_type': self._group_learning_signals(),
                'total': len(self.data['learning_signals'])
            },
            'learning_velocity_indicators': learning_velocity
        }

    def _calculate_learning_velocity_indicators(self):
        """Calculate learning velocity based on extracted patterns"""
        indicators = {}

        # Skill diversity (breadth vs depth)
        total_skills = len(self.data['skill_mentions'])
        skill_categories = len(set(
            mention['category']
            for mentions in self.data['skill_mentions'].values()
            for mention in mentions if mentions
        ))

        indicators['skill_diversity'] = {
            'total_skills': total_skills,
            'categories_touched': skill_categories,
            'breadth_score': min(skill_categories * 10, 100)  # 0-100 scale
        }

        # Complexity trajectory
        if self.data['project_complexity']:
            avg_complexity = sum(p['complexity_score'] for p in self.data['project_complexity']) / len(self.data['project_complexity'])
            indicators['complexity_trajectory'] = {
                'average_complexity': round(avg_complexity, 2),
                'trend': 'increasing' if len(self.data['project_complexity']) > 3 else 'insufficient_data'
            }

        # Learning signal intensity
        signal_counts = defaultdict(int)
        for signal in self.data['learning_signals']:
            signal_counts[signal['type']] += 1

        indicators['learning_intensity'] = {
            'experimentation_rate': signal_counts.get('experimentation', 0),
            'mastery_signals': signal_counts.get('mastery', 0),
            'teaching_signals': signal_counts.get('teaching', 0),
            'ownership_signals': signal_counts.get('ownership', 0)
        }

        # Career velocity (how fast they progress)
        role_transitions = self.data['role_transitions']
        if role_transitions:
            levels = ['junior', 'mid', 'senior', 'leadership']
            highest_level = 'junior'
            for transition in role_transitions:
                if levels.index(transition['level']) > levels.index(highest_level):
                    highest_level = transition['level']

            indicators['career_velocity'] = {
                'highest_level_reached': highest_level,
                'total_transitions': len(role_transitions)
            }

        return indicators

    def _get_complexity_distribution(self):
        """Get distribution of project complexity scores"""
        if not self.data['project_complexity']:
            return {}

        scores = [p['complexity_score'] for p in self.data['project_complexity']]
        return {
            'low_complexity': len([s for s in scores if s < 3]),
            'medium_complexity': len([s for s in scores if 3 <= s < 7]),
            'high_complexity': len([s for s in scores if s >= 7]),
            'average': sum(scores) / len(scores)
        }

    def _detect_progression_pattern(self):
        """Detect if there's clear career progression"""
        levels = ['junior', 'mid', 'senior', 'leadership']
        role_levels = []

        for transition in sorted(self.data['role_transitions'], key=lambda x: x.get('year') or '0'):
            role_levels.append(transition['level'])

        if len(role_levels) < 2:
            return 'insufficient_data'

        # Check if generally increasing
        level_indices = [levels.index(level) for level in role_levels if level in levels]
        if not level_indices:
            return 'unclear'

        increasing = sum(1 for i in range(1, len(level_indices)) if level_indices[i] > level_indices[i-1])
        total_transitions = len(level_indices) - 1

        if total_transitions == 0:
            return 'single_level'
        if increasing / total_transitions > 0.6:
            return 'upward_progression'
        else:
            return 'lateral_or_mixed'

    def _group_learning_signals(self):
        """Group learning signals by type with counts"""
        grouped = defaultdict(int)
        for signal in self.data['learning_signals']:
            grouped[signal['type']] += 1
        return dict(grouped)


def get_multi_source_analysis_prompt(analysis_data):
    """
    Generate AI prompt for analyzing multi-source data
    Returns prompt to send to LLM for pattern extraction
    """
    return f"""
You are analyzing professional background data to extract learning velocity patterns.

Data has been extracted from: CV, LinkedIn, Portfolio, or other professional sources.

Given this analysis:
{json.dumps(analysis_data, indent=2)}

Extract and return JSON with:

1. **learningVelocity**: How fast does this person learn and adapt?
   - Look at skill diversity and category breadth
   - Analyze complexity trajectory of projects
   - Consider education progression (formal + self-taught)

2. **careerTrajectory**: How has their career evolved?
   - Analyze role transitions and progression pattern
   - Identify pivots or domain changes
   - Assess velocity of advancement

3. **learningStyle**: depth-first (master one thing) vs breadth-first (explore many)?
   - Analyze skill distribution across categories
   - Look at project complexity vs quantity
   - Consider teaching/mentoring signals (indicator of depth)

4. **persistenceMetric**: Evidence of sustained effort vs quick experiments
   - Look at ownership and delivery signals
   - Consider project completion indicators
   - Assess follow-through patterns

5. **growthIndicators**: Signals of continuous learning
   - Experimentation signals
   - Mastery signals (deep dives, expertise claims)
   - Teaching signals (mentoring, writing, presenting)

Base your analysis ONLY on observable patterns from the data, not assumptions.
Return valid JSON only, no markdown.

Expected format:
{{
    "learningVelocity": {{
        "assessment": "fast/medium/slow",
        "evidence": "specific data points from analysis",
        "timeToCompetency": "estimated based on skill adoption patterns"
    }},
    "careerTrajectory": {{
        "pattern": "upward/lateral/pivot/early-career",
        "progressionSpeed": "rapid/steady/gradual",
        "evidence": "role transitions and timeline"
    }},
    "learningStyle": {{
        "style": "depth-first/breadth-first/balanced",
        "skillDiversity": "high/medium/low",
        "evidence": "skill categories and project complexity"
    }},
    "persistenceMetric": {{
        "score": 0-100,
        "ownershipSignals": number,
        "evidence": "specific examples"
    }},
    "growthIndicators": {{
        "experimentationRate": "high/medium/low",
        "masterySignals": number,
        "teachingSignals": number,
        "continuousLearning": true/false
    }}
}}
"""
