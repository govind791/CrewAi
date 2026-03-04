from crewai import Agent, LLM
from textwrap import dedent

llm = LLM(
    model="groq/llama-3.1-8b-instant"
)
class EmailFilterAgents():
    def __init__(self):
        pass

    def email_filter_agent(self):
        return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like newsletters and promotional content',
            backstory=dedent("""\
                You analyze emails and determine which ones are important."""),
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    def email_action_agent(self):
        return Agent(
            role='Email Action Specialist',
            goal='Identify action-required emails and compile a list of their IDs',
            backstory=dedent("""\
                You identify which emails require immediate action."""),
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )

    def email_response_writer(self):
        return Agent(
            role='Email Response Writer',
            goal='Draft responses to action-required emails',
            backstory=dedent("""\
                You draft clear and professional email responses."""),
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )