"""
GitHub Analysis Module for SOKRATES
Extracts learning velocity patterns from GitHub commit history
"""

import requests
from datetime import datetime
from collections import defaultdict
import json


class GitHubAnalyzer:
    """Analyzes GitHub activity to extract learning velocity patterns"""

    def __init__(self, github_token=None):
        self.github_token = github_token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'

    def analyze_user(self, username):
        """
        Main entry point for GitHub analysis

        Args:
            username: GitHub username

        Returns:
            dict: Comprehensive analysis of learning patterns
        """
        try:
            # Fetch user repos
            repos = self._fetch_user_repos(username)
            if not repos:
                return None

            # Extract commit data from repos
            commit_timeline = []
            language_usage = defaultdict(lambda: {
                'first_use': None,
                'last_use': None,
                'commit_count': 0,
                'repos': []
            })
            project_complexity = []

            for repo in repos[:20]:  # Limit to 20 most recent repos to avoid rate limiting
                repo_name = repo['name']

                # Get commits for this repo
                commits = self._fetch_repo_commits(username, repo_name)

                # Track languages
                if repo.get('language'):
                    lang = repo['language']
                    language_usage[lang]['commit_count'] += len(commits)
                    language_usage[lang]['repos'].append(repo_name)

                    repo_created = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    repo_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')

                    if not language_usage[lang]['first_use'] or repo_created < language_usage[lang]['first_use']:
                        language_usage[lang]['first_use'] = repo_created
                    if not language_usage[lang]['last_use'] or repo_updated > language_usage[lang]['last_use']:
                        language_usage[lang]['last_use'] = repo_updated

                # Analyze commits
                for commit in commits:
                    commit_date = commit['commit']['author']['date']
                    commit_timeline.append({
                        'date': commit_date,
                        'repo': repo_name,
                        'message': commit['commit']['message']
                    })

                # Track project complexity
                project_complexity.append({
                    'repo_name': repo_name,
                    'created': repo['created_at'],
                    'last_update': repo['updated_at'],
                    'language': repo.get('language', 'Unknown'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'size': repo.get('size', 0)
                })

            # Calculate learning patterns
            learning_patterns = self._calculate_learning_patterns(
                commit_timeline,
                language_usage,
                project_complexity
            )

            return {
                'commit_timeline': self._aggregate_commit_timeline(commit_timeline),
                'language_evolution': self._format_language_evolution(language_usage),
                'project_complexity': project_complexity,
                'learning_patterns': learning_patterns
            }

        except Exception as e:
            print(f"Error analyzing GitHub user {username}: {str(e)}")
            return None

    def _fetch_user_repos(self, username):
        """Fetch all public repositories for a user"""
        try:
            url = f'https://api.github.com/users/{username}/repos'
            response = requests.get(url, headers=self.headers, params={'per_page': 100, 'sort': 'updated'})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching repos: {str(e)}")
            return []

    def _fetch_repo_commits(self, username, repo_name, max_commits=100):
        """Fetch commits for a specific repository"""
        try:
            url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
            response = requests.get(url, headers=self.headers, params={'per_page': max_commits})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching commits for {repo_name}: {str(e)}")
            return []

    def _aggregate_commit_timeline(self, commits):
        """Aggregate commits by date"""
        daily_commits = defaultdict(int)
        for commit in commits:
            date = commit['date'].split('T')[0]
            daily_commits[date] += 1

        timeline = [
            {'date': date, 'count': count}
            for date, count in sorted(daily_commits.items())
        ]
        return timeline

    def _format_language_evolution(self, language_usage):
        """Format language usage data"""
        evolution = []
        for lang, data in language_usage.items():
            evolution.append({
                'language': lang,
                'first_use': data['first_use'].isoformat() if data['first_use'] else None,
                'last_use': data['last_use'].isoformat() if data['last_use'] else None,
                'commit_count': data['commit_count'],
                'repo_count': len(data['repos'])
            })
        return sorted(evolution, key=lambda x: x['commit_count'], reverse=True)

    def _calculate_learning_patterns(self, commit_timeline, language_usage, projects):
        """Calculate learning velocity and patterns"""
        patterns = {}

        # Calculate time to first commit for each language
        time_to_first_commit = {}
        for lang, data in language_usage.items():
            if data['first_use'] and data['last_use']:
                days = (data['last_use'] - data['first_use']).days
                time_to_first_commit[lang] = days

        patterns['time_to_first_commit'] = time_to_first_commit

        # Calculate consistency score (commit frequency variance)
        if commit_timeline:
            dates = [datetime.strptime(c['date'].split('T')[0], '%Y-%m-%d') for c in commit_timeline]
            if len(dates) > 1:
                dates_sorted = sorted(dates)
                gaps = [(dates_sorted[i+1] - dates_sorted[i]).days for i in range(len(dates_sorted)-1)]
                avg_gap = sum(gaps) / len(gaps) if gaps else 0
                variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps) if gaps else 0
                patterns['consistency_score'] = 100 - min(variance / 10, 100)  # Normalize to 0-100
            else:
                patterns['consistency_score'] = 50
        else:
            patterns['consistency_score'] = 0

        # Exploration vs Build ratio
        total_repos = len(projects)
        total_commits = len(commit_timeline)
        patterns['exploration_vs_build'] = total_repos / max(total_commits / 10, 1)

        return patterns


def get_github_analysis_prompt(github_data):
    """
    Generate AI prompt for analyzing GitHub patterns
    Returns prompt to send to LLM for pattern extraction
    """
    return f"""
You are analyzing GitHub commit data to extract learning velocity patterns.

Given this commit history:
{json.dumps(github_data, indent=2)}

Extract and return JSON with:

1. **learningVelocity**: How fast does this person go from "first commit" to "competent implementation" for new technologies?
   - Look at language adoption patterns
   - Identify time between first use and sustained usage

2. **complexityTrajectory**: Is project complexity increasing over time?
   - Compare early projects vs recent projects
   - Look at stars, forks, project size metrics

3. **learningStyle**: depth-first (master one thing) vs breadth-first (try many things)?
   - Analyze language diversity vs specialization
   - Look at commit patterns across repos

4. **persistenceMetric**: Ratio of completed projects vs abandoned experiments
   - Check for projects with sustained commits vs one-off experiments
   - Recent activity indicates persistence

5. **independenceRate**: Tutorial copying vs original implementation ratio
   - Infer from commit message patterns
   - Look for evidence of exploration vs following guides

Base your analysis ONLY on observable commit patterns, not assumptions.
Return valid JSON only, no markdown.

Expected format:
{{
    "learningVelocity": {{
        "assessment": "fast/medium/slow",
        "evidence": "specific data points",
        "timeToCompetency": "estimated weeks/months"
    }},
    "complexityTrajectory": {{
        "trend": "increasing/stable/decreasing",
        "evidence": "specific examples"
    }},
    "learningStyle": {{
        "style": "depth-first/breadth-first/balanced",
        "evidence": "language patterns and commit distribution"
    }},
    "persistenceMetric": {{
        "score": 0-100,
        "completedProjects": number,
        "abandonedProjects": number
    }},
    "independenceRate": {{
        "score": 0-100,
        "evidence": "commit message analysis"
    }}
}}
"""
