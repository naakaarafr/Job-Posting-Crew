from crewai import Agent
from tools import tools_manager
from config import config

def create_research_agent():
    """Create and return the Research Analyst agent"""
    return Agent(
        role="Research Analyst",
        goal="Analyze the company website and provided description to extract insights on culture, values, and specific needs.",
        backstory="Expert in analyzing company cultures and identifying key values and needs from various sources, including websites and brief descriptions.",
        tools=tools_manager.get_research_tools(),
        verbose=config.AGENT_VERBOSE,
        llm=config.DEFAULT_LLM
    )

def create_writer_agent():
    """Create and return the Job Description Writer agent"""
    return Agent(
        role="Job Description Writer",
        goal="Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.",
        backstory="Skilled in crafting compelling job descriptions that resonate with the company's values and attract the right candidates.",
        tools=tools_manager.get_writer_tools(),
        verbose=config.AGENT_VERBOSE,
        llm=config.DEFAULT_LLM
    )

def create_review_agent():
    """Create and return the Review and Editing Specialist agent"""
    return Agent(
        role="Review and Editing Specialist",
        goal="Review the job posting for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection.",
        backstory="A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect.",
        tools=tools_manager.get_review_tools(),
        verbose=config.AGENT_VERBOSE,
        llm=config.DEFAULT_LLM
    )