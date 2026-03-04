from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

# ─────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────

researcher = Agent(
    role='AI Market Researcher',
    goal='Gather comprehensive data on the AI & Technology market landscape',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        'You are an expert market researcher with 15 years of experience analyzing '
        'the AI and technology sector. You have a talent for identifying emerging trends, '
        'key players, and market opportunities before they become mainstream.'
    )
)

competitor_analyst = Agent(
    role='Competitor Analyst',
    goal='Analyze top competitors in the AI & Technology space and identify their strengths and weaknesses',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        'You are a sharp competitive intelligence analyst who specializes in the AI industry. '
        'You have deep knowledge of companies like OpenAI, Google DeepMind, Anthropic, Meta AI, '
        'and Microsoft, and can break down their strategies, products, and market positioning.'
    )
)

strategist = Agent(
    role='Business Strategist',
    goal='Develop actionable business strategies and opportunities based on market research and competitor analysis',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        'You are a seasoned business strategist who turns market data into clear, '
        'actionable recommendations. You specialize in helping companies find their '
        'competitive edge in the fast-moving AI & Technology industry.'
    )
)

report_writer = Agent(
    role='Market Report Writer',
    goal='Compile all findings into a professional, well-structured market analysis report',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        'You are a professional business writer who specializes in creating clear, '
        'compelling market reports for executives and investors. Your reports are '
        'known for being insightful, concise, and easy to act upon.'
    )
)

# ─────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────

research_task = Task(
    description=(
        'Research the current state of the AI & Technology market. Cover: '
        '1) Market size and growth rate, '
        '2) Key trends shaping the industry in 2024-2025, '
        '3) Major investment areas and funding activity, '
        '4) Emerging technologies to watch.'
    ),
    expected_output=(
        'A detailed research summary covering market size, top trends, '
        'investment activity, and emerging technologies in AI & Technology.'
    ),
    agent=researcher
)

competitor_task = Task(
    description=(
        'Analyze the top 5 competitors in the AI & Technology space. For each company cover: '
        '1) Core products and services, '
        '2) Key strengths, '
        '3) Key weaknesses or gaps, '
        '4) Recent strategic moves. '
        'Focus on: OpenAI, Google DeepMind, Anthropic, Meta AI, and Microsoft AI.'
    ),
    expected_output=(
        'A competitor analysis covering the top 5 AI companies with their '
        'strengths, weaknesses, products, and recent strategic moves.'
    ),
    agent=competitor_analyst
)

strategy_task = Task(
    description=(
        'Based on the market research and competitor analysis, identify: '
        '1) Top 3 market opportunities in AI & Technology, '
        '2) Potential threats and risks to watch, '
        '3) Recommended strategic moves for a new or growing AI company, '
        '4) Key success factors in this market.'
    ),
    expected_output=(
        'A strategic recommendations report with market opportunities, risks, '
        'and actionable advice for competing in the AI & Technology space.'
    ),
    agent=strategist
)

report_task = Task(
    description=(
        'Compile all previous research, competitor analysis, and strategic recommendations '
        'into a single, professional Market Analysis Report. Structure it with: '
        '1) Executive Summary, '
        '2) Market Overview, '
        '3) Competitor Landscape, '
        '4) Opportunities & Risks, '
        '5) Strategic Recommendations, '
        '6) Conclusion.'
    ),
    expected_output=(
        'A complete, well-structured Market Analysis Report on the AI & Technology '
        'industry, ready to present to executives or investors.'
    ),
    agent=report_writer
)

# ─────────────────────────────────────────
# CREW
# ─────────────────────────────────────────

market_crew = Crew(
    agents=[researcher, competitor_analyst, strategist, report_writer],
    tasks=[research_task, competitor_task, strategy_task, report_task],
    process=Process.sequential,
    verbose=True
)

# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

print("\n" + "="*60)
print("   AI & TECHNOLOGY MARKET ANALYSIS - STARTING")
print("="*60 + "\n")

result = market_crew.kickoff()

print("\n" + "="*60)
print("   FINAL MARKET ANALYSIS REPORT")
print("="*60)
print(result)