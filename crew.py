from crewai import Crew, Process
from agents import create_research_agent, create_writer_agent, create_review_agent
from tasks import (
    create_research_company_culture_task,
    create_research_role_requirements_task,
    create_draft_job_posting_task,
    create_review_and_edit_job_posting_task,
    create_industry_analysis_task
)
from config import config

class JobPostingCrew:
    """JobPosting crew"""
    
    def __init__(self):
        # Initialize agents
        self.research_agent = create_research_agent()
        self.writer_agent = create_writer_agent()
        self.review_agent = create_review_agent()
        
        # Initialize tasks
        self.research_company_culture_task = create_research_company_culture_task(self.research_agent)
        self.research_role_requirements_task = create_research_role_requirements_task(self.research_agent)
        self.draft_job_posting_task = create_draft_job_posting_task(self.writer_agent)
        self.review_and_edit_job_posting_task = create_review_and_edit_job_posting_task(self.review_agent)
        self.industry_analysis_task = create_industry_analysis_task(self.research_agent)

    def crew(self) -> Crew:
        """Creates the JobPostingCrew"""
        return Crew(
            agents=[
                self.research_agent,
                self.writer_agent,
                self.review_agent
            ],
            tasks=[
                self.research_company_culture_task,
                self.research_role_requirements_task,
                self.draft_job_posting_task,
                self.review_and_edit_job_posting_task,
                self.industry_analysis_task
            ],
            process=Process.sequential,
            verbose=config.CREW_VERBOSE,
        )