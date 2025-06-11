from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class ResearchRoleRequirements(BaseModel):
    """Research role requirements model"""
    skills: List[str] = Field(..., description="List of recommended skills for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    experience: List[str] = Field(..., description="List of recommended experience for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    qualities: List[str] = Field(..., description="List of recommended qualities for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")

def create_research_company_culture_task(agent):
    """Create and return the research company culture task"""
    return Task(
        description="""
        Analyze the provided company website and the hiring manager's company's domain {company_domain},
        description {company_description}. Focus on understanding the company's culture, values, and mission.
        Identify unique selling points and specific projects or achievements highlighted on the site.
        Compile a report summarizing these insights, specifically how they can be leveraged in a job posting
        to attract the right candidates.
        """,
        expected_output="""
        A comprehensive report detailing the company's culture, values, and mission, along with specific selling
        points relevant to the job role. Suggestions on incorporating these insights into the job posting should be included.
        """,
        agent=agent
    )

def create_research_role_requirements_task(agent):
    """Create and return the research role requirements task"""
    return Task(
        description="""
        Based on the hiring manager's needs: {hiring_needs}, identify the key skills, experiences,
        and qualities the ideal candidate should possess for the role. Consider the company's current projects,
        its competitive landscape, and industry trends. Prepare a list of recommended job requirements
        and qualifications that align with the company's needs and values.
        """,
        expected_output="""
        A list of recommended skills, experiences, and qualities for the ideal candidate, aligned with
        the company's culture, ongoing projects, and the specific role's requirements.
        """,
        agent=agent,
        output_json=ResearchRoleRequirements
    )

def create_draft_job_posting_task(agent):
    """Create and return the draft job posting task"""
    return Task(
        description="""
        Draft a job posting for the role described by the hiring manager: {hiring_needs}.
        Use the insights on {company_description} to start with a compelling introduction,
        followed by a detailed role description, responsibilities, and required skills and qualifications.
        Ensure the tone aligns with the company's culture and incorporate any unique benefits or
        opportunities offered by the company. Specific benefits: {specific_benefits}.
        """,
        expected_output="""
        A detailed, engaging job posting that includes an introduction, role description, responsibilities,
        requirements, and unique company benefits. The tone should resonate with the company's culture
        and values, aimed at attracting the right candidates.
        """,
        agent=agent
    )

def create_review_and_edit_job_posting_task(agent):
    """Create and return the review and edit job posting task"""
    return Task(
        description="""
        Review the draft job posting for the role {hiring_needs}. Check for clarity, engagement, grammatical accuracy,
        and alignment with the company's culture and values. Edit and refine the content, ensuring it speaks directly
        to the desired candidates and accurately reflects the role's unique benefits and opportunities. Provide
        feedback for any necessary revisions.
        """,
        expected_output="""
        A polished, error-free job posting that is clear, engaging, and perfectly aligned with the company's culture and values.
        Feedback on potential improvements and final approval for publishing. Formatted in markdown.
        """,
        agent=agent
    )

def create_industry_analysis_task(agent):
    """Create and return the industry analysis task"""
    return Task(
        description="""
        Conduct an in-depth analysis of the industry related to the company's domain {company_domain}.
        Investigate current trends, challenges, and opportunities within the industry, utilizing market reports,
        recent developments, and expert opinions. Assess how these factors could impact the role being hired
        for and the overall attractiveness of the position to potential candidates.
        Consider how the company's position within this industry and its response to these trends could be leveraged to attract top talent.
        Include in your report how the role contributes to addressing industry challenges or seizing opportunities.
        """,
        expected_output="""
        A detailed analysis report that identifies major industry trends, challenges, and opportunities relevant
        to the company's domain and the specific job role. This report should provide strategic insights on positioning
        the job role and the company as an attractive choice for potential candidates.
        """,
        agent=agent
    )