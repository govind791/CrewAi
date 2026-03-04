import os

# Stub mode disables Gmail API calls and returns a fake message.
# It can be triggered explicitly via USE_STUB_EMAILS=1
# or automatically when the Google credentials file is missing.
use_stub = (
    os.environ.get("USE_STUB_EMAILS") == "1"
    or not os.path.exists("credentials.json")
)

print(
    "[nodes] credentials present?",
    os.path.exists("credentials.json"),
    "USE_STUB_EMAILS=",
    os.environ.get("USE_STUB_EMAILS"),
    "-> use_stub=",
    use_stub,
)

if not use_stub:
    from langchain_community.agent_toolkits import GmailToolkit
    from langchain_community.tools.gmail.search import GmailSearch


class Nodes:
    def __init__(self):
        # Only initialize Gmail when not in stub mode
        if not use_stub:
            self.gmail = GmailToolkit()

    def check_email(self, state):
        print("# Checking for new emails")

        try:
            if use_stub:
                emails = [
                    {
                        "id": "stub1",
                        "threadId": "stub-thread",
                        "snippet": "This is a stub message.",
                        "sender": "example@example.com",
                    }
                ]
            else:
                search = GmailSearch(api_resource=self.gmail.api_resource)
                emails = search.run("after:newer_than:1d")

        except Exception as e:
            print("❌ Gmail fetch error:", e)
            return {**state, "emails": []}

        checked_emails = state.get("checked_emails_ids", [])
        seen_threads = []
        new_emails = []

        for email in emails:
            if (
                email["id"] not in checked_emails
                and email["threadId"] not in seen_threads
                and (
                    use_stub
                    or os.environ.get("MY_EMAIL", "")
                    not in email.get("sender", "")
                )
            ):
                seen_threads.append(email["threadId"])
                new_emails.append(
                    {
                        "id": email["id"],
                        "threadId": email["threadId"],
                        "snippet": email.get("snippet", ""),
                        "sender": email.get("sender", ""),
                    }
                )

        checked_emails.extend([email["id"] for email in emails])

        return {
            **state,
            "emails": new_emails,
            "checked_emails_ids": checked_emails,
        }

    def wait_next_run(self, state):
        # Sleep removed — handled in main.py
        return state

    def new_emails(self, state):
        if len(state.get("emails", [])) == 0:
            print("## No new emails")
            return "end"
        else:
            print("## New emails")
            return "continue"