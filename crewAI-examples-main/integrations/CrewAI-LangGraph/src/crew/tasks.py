from crewai import Task
from textwrap import dedent


class EmailFilterTasks:

    def filter_emails_task(self, agent, emails):
        return Task(
            description=dedent(f"""\
                Analyze a batch of emails and filter out
                non-essential ones such as newsletters, promotional content and notifications.

                EMAILS
                -------
                {emails}

                Return only relevant thread_ids and sender using bullet points.
            """),
            expected_output="A bullet point list containing relevant thread_ids and sender emails.",
            agent=agent
        )

    def action_required_emails_task(self, agent):
        return Task(
            description=dedent("""\
                For each email thread, analyze the conversation.

                Provide:
                - thread_id
                - summary
                - key points
                - communication style
                - sender email address
            """),
            expected_output="A structured list with thread_id, summary, key points, communication style, and sender email.",
            agent=agent
        )

    def draft_responses_task(self, agent):
        return Task(
            description=dedent("""\
                Draft professional responses for each action-required email.
                Mimic the communication style of the thread.
            """),
            expected_output="A confirmation that all email drafts have been created.",
            agent=agent
        )