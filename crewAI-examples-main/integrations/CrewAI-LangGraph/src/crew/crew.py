from crewai import Crew

from .agents import EmailFilterAgents
from .tasks import EmailFilterTasks


class EmailFilterCrew():
    def __init__(self):
        agents = EmailFilterAgents()
        self.filter_agent = agents.email_filter_agent()
        self.action_agent = agents.email_action_agent()
        self.writer_agent = agents.email_response_writer()

    def kickoff(self, state):
        print("### Filtering emails")

        # 🔥 HARD FILTER BEFORE LLM (IMPORTANT)
        filtered_emails = []
        for email in state["emails"]:
            sender = email["sender"].lower()

            # Ignore job portals & automated alerts
            if any(domain in sender for domain in [
                "indeed.com",
                "linkedin.com",
                "naukri.com",
                "alert@",
                "no-reply",
                "newsletter"
            ]):
                continue

            filtered_emails.append(email)

        # If nothing valid → skip LLM completely
        if not filtered_emails:
            print("No human emails found. Skipping crew.")
            return {
                **state,
                "action_required_emails": [],
                "checked_emails_ids": [
                    *state.get("checked_emails_ids", []),
                    *[e["id"] for e in state["emails"]]
                ]
            }

        tasks = EmailFilterTasks()

        crew = Crew(
            agents=[self.filter_agent, self.action_agent, self.writer_agent],
            tasks=[
                tasks.filter_emails_task(
                    self.filter_agent,
                    self._format_emails(filtered_emails)
                ),
                tasks.action_required_emails_task(self.action_agent),
                tasks.draft_responses_task(self.writer_agent)
            ],
            verbose=True
        )

        result = crew.kickoff()

        # ✅ Properly update state
        return {
            **state,
            "action_required_emails": result,
            "checked_emails_ids": [
                *state.get("checked_emails_ids", []),
                *[e["id"] for e in state["emails"]]
            ]
        }

    def _format_emails(self, emails):
        emails_string = []
        for email in emails:
            print(email)
            arr = [
                f"ID: {email['id']}",
                f"- Thread ID: {email['threadId']}",
                f"- Snippet: {email['snippet']}",
                f"- From: {email['sender']}",
                f"--------"
            ]
            emails_string.append("\n".join(arr))
        return "\n".join(emails_string)