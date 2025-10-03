"""
Marine Health AI Letter Generator
Automatically generates advocacy letters for marine conservation organizations
Using OpenRouter API (x-ai/grok-4-fast:free)
"""

import os
import json
import requests
from datetime import datetime
import random
from typing import Dict, List
from dataclasses import dataclass
import time
from dotenv import load_dotenv

# Load .env
load_dotenv()


@dataclass
class OrganizationProfile:
    name: str
    target_audience: str
    tone: str
    focus_areas: List[str]
    call_to_action: str
    contact_info: str


@dataclass
class MarineHealthData:
    current_index: float
    region: str
    coordinates: str
    severity_level: str
    urgency: str
    recent_changes: str
    key_issues: List[str]


class MarineHealthAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Marine Health AI"
        }

        # Define your organizations
        self.organizations = {
            "policy_makers": OrganizationProfile(
                name="Ocean Policy Institute",
                target_audience="Government Officials, Policy Makers, Environmental Agencies",
                tone="formal, evidence-based, diplomatic",
                focus_areas=["policy reform", "international cooperation", "regulatory frameworks", "funding allocation"],
                call_to_action="implement stronger marine protection policies and increase funding",
                contact_info="dheunsac@gmail.com"
            ),
            "industry_leaders": OrganizationProfile(
                name="Sustainable Marine Industries Coalition",
                target_audience="Corporate Leaders, Manufacturing, Shipping, Energy Companies",
                tone="business-focused, solution-oriented, collaborative",
                focus_areas=["sustainable practices", "green technology", "corporate responsibility", "economic benefits"],
                call_to_action="adopt sustainable practices and invest in clean marine technologies",
                contact_info="dheunsac@gmail.com"
            ),
            "communities": OrganizationProfile(
                name="Coastal Communities Alliance",
                target_audience="Local Communities, Volunteers, Community Leaders, Residents",
                tone="passionate, community-focused, inspiring",
                focus_areas=["grassroots action", "local impact", "community engagement", "educational programs"],
                call_to_action="join local conservation efforts and engage in community marine protection",
                contact_info="dheunsac@gmail.com"
            )
        }

    def get_current_marine_data(self) -> MarineHealthData:
        """Simulate getting current marine health data"""
        base_index = 78.4
        variation = random.uniform(-5, 5)
        current_index = max(0, min(100, base_index + variation))

        if current_index >= 80:
            severity = "Excellent"
            urgency = "CONTINUE EXCELLENT PRACTICES"
        elif current_index >= 60:
            severity = "Good"
            urgency = "MAINTAIN CURRENT EFFORTS"
        elif current_index >= 40:
            severity = "Fair"
            urgency = "IMPROVEMENT NEEDED"
        elif current_index >= 20:
            severity = "Poor"
            urgency = "URGENT ACTION REQUIRED"
        else:
            severity = "Critical"
            urgency = "IMMEDIATE INTERVENTION"

        issues = [
            "microplastic contamination increasing by 12%",
            "coral bleaching events in 34% of monitored reefs",
            "fish population decline in commercial zones",
            "coastal water quality improvements in urban areas",
            "successful marine protected area expansions",
            "renewable energy adoption in shipping industry"
        ]

        return MarineHealthData(
            current_index=current_index,
            region="Bay of Bengal",
            coordinates="21.0000° N, 90.0000° E",
            severity_level=severity,
            urgency=urgency,
            recent_changes=f"Index changed by {variation:+.1f} points in the last 30 days",
            key_issues=random.sample(issues, 3)
        )

    def generate_letter_with_grok(self, org_key: str, marine_data: MarineHealthData) -> str:
        """Generate letter using OpenRouter Grok"""
        org = self.organizations[org_key]

        prompt_text = f"""
Write a professional advocacy letter for marine conservation from {org.name} to {org.target_audience}. 
Don't use any personal names or positions. After "Sincerely yours," just write SARgonauts and their email address.

CURRENT MARINE HEALTH DATA:
- SARgonauts Index: {marine_data.current_index:.1f}/100
- Status: {marine_data.severity_level}
- Region: {marine_data.region} ({marine_data.coordinates})
- Urgency Level: {marine_data.urgency}
- Recent Changes: {marine_data.recent_changes}
- Key Issues: {', '.join(marine_data.key_issues)}

ORGANIZATION PROFILE:
- Name: {org.name}
- Target Audience: {org.target_audience}
- Tone: {org.tone}
- Focus Areas: {', '.join(org.focus_areas)}
- Main Call to Action: {org.call_to_action}
- Contact: {org.contact_info}

Make it compelling, data-driven, professional, 400-600 words. Prepend the current date at the top of the letter programmatically. No need to add the word count here.
"""

        payload = {
            "model": "x-ai/grok-4-fast:free",
            "messages": [
                {"role": "system", "content": "You are an expert marine conservation advocate and professional letter writer."},
                {"role": "user", "content": [{"type": "text", "text": prompt_text}]}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return self._fallback_letter(org_key, marine_data)

    def _fallback_letter(self, org_key: str, marine_data: MarineHealthData) -> str:
        """Fallback letter template if API fails"""
        org = self.organizations[org_key]
        date = datetime.now().strftime("%B %d, %Y")
        return f"""
Date: {date}
{org.name}
Marine Conservation Advocacy Division

Dear {org.target_audience},

Subject: Urgent Action Required - Marine Health Status Update for {marine_data.region}

Our latest marine health assessment reveals a SARgonauts Index of {marine_data.current_index:.1f}/100 for the {marine_data.region} region, indicating {marine_data.severity_level.lower()} conditions.

KEY ISSUES:
{chr(10).join(f'• {issue.title()}' for issue in marine_data.key_issues)}

RECOMMENDED IMMEDIATE ACTIONS:
1. {org.focus_areas[0].title()} - Implement enhanced monitoring systems
2. {org.focus_areas[1].title()} - Increase resource allocation
3. {org.focus_areas[2].title()} - Establish new partnerships

We urge you to {org.call_to_action} within the next 30 days.

Sincerely yours,
SARgonauts
{org.contact_info}
"""

    def generate_all_letters(self) -> Dict[str, str]:
        marine_data = self.get_current_marine_data()
        letters = {}

        print(f"Current Marine Health Data:")
        print(f"   Index: {marine_data.current_index:.1f}/100 ({marine_data.severity_level})")
        print(f"   Region: {marine_data.region}")
        print(f"   Status: {marine_data.urgency}")
        print(f"   Recent: {marine_data.recent_changes}")
        print()

        os.makedirs("output", exist_ok=True)

        for org_key, org in self.organizations.items():
            print(f"Generating letter for {org.name}...")
            letter = self.generate_letter_with_grok(org_key, marine_data)

            # Prepend current date
            today_date = datetime.now().strftime("%B %d, %Y")
            letter = f"Date: {today_date}\n\n{letter}"

            letters[org_key] = letter
            filename = f"output/letter_{org_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(letter)
            print(f"   Saved to {filename}")
            time.sleep(1)

        return letters

    def save_daily_report(self, letters: Dict[str, str]):
        os.makedirs("output", exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_filename = f"output/daily_report_{date_str}.json"
        report = {
            "generated_date": datetime.now().isoformat(),
            "letters": letters,
            "organizations": {k: v.__dict__ for k, v in self.organizations.items()}
        }
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Daily report saved to {report_filename}")


def main():
    print("Marine Health AI Letter Generator Starting...")
    print("=" * 50)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in .env")
        return

    ai_agent = MarineHealthAI(api_key)
    letters = ai_agent.generate_all_letters()
    ai_agent.save_daily_report(letters)
    print("All letters generated successfully!")
    print("Check the 'output' folder for generated files")
    print("=" * 50)


if __name__ == "__main__":
    main()
