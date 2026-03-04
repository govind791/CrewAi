from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END

from .state import EmailsState
from .nodes import Nodes
from .crew.crew import EmailFilterCrew

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("draft_responses", EmailFilterCrew().kickoff)
        workflow.add_node("wait_next_run", nodes.wait_next_run)

        workflow.set_entry_point("check_new_emails")

        workflow.add_conditional_edges(
            "check_new_emails",
            nodes.new_emails,
            {
                "continue": "draft_responses",
                "end": "wait_next_run"
            }
        )

        # After drafting → go to wait
        workflow.add_edge("draft_responses", "wait_next_run")

        # 🔥 IMPORTANT: Stop graph here
        workflow.add_edge("wait_next_run", END)

        self.app = workflow.compile()