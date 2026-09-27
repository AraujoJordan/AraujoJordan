"""Refresh the public GitHub numbers used by the profile cards."""

from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess


query = '''query {
  user(login: "AraujoJordan") {
    repositories(privacy: PUBLIC, first: 100, ownerAffiliations: OWNER) {
      totalCount
      nodes { isFork stargazerCount }
    }
    followers { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}'''
response = subprocess.run(
    ['gh', 'api', 'graphql', '-f', f'query={query}'],
    check=True, capture_output=True, text=True,
)
user = json.loads(response.stdout)['data']['user']
stats = {
    'as_of': datetime.now(timezone.utc).date().isoformat(),
    'public_repos': user['repositories']['totalCount'],
    'earned_stars': sum(r['stargazerCount'] for r in user['repositories']['nodes'] if not r['isFork']),
    'followers': user['followers']['totalCount'],
    'year_contributions': user['contributionsCollection']['contributionCalendar']['totalContributions'],
}
(Path(__file__).parent / 'stats.json').write_text(json.dumps(stats, indent=2) + '\n')
calendar = user['contributionsCollection']['contributionCalendar']
(Path(__file__).parent / 'contributions.json').write_text(json.dumps(calendar, indent=2) + '\n')
