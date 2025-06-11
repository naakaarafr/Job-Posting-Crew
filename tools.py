from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

class ToolsManager:
    """
    Manager class for all tools used in the job posting crew.
    Centralizes tool initialization and configuration.
    """
    
    def __init__(self):
        self._serper_dev_tool = None
        self._scrape_website_tool = None
    
    @property
    def serper_dev_tool(self):
        """Initialize and return SerperDevTool"""
        if self._serper_dev_tool is None:
            # Check if API key is available
            api_key = os.getenv('SERPER_API_KEY')
            if not api_key:
                print("Warning: SERPER_API_KEY not found in environment variables")
            self._serper_dev_tool = SerperDevTool()
        return self._serper_dev_tool
    
    @property
    def scrape_website_tool(self):
        """Initialize and return ScrapeWebsiteTool"""
        if self._scrape_website_tool is None:
            self._scrape_website_tool = ScrapeWebsiteTool()
        return self._scrape_website_tool
    
    def get_research_tools(self):
        """Get tools for research agent"""
        return [
            self.serper_dev_tool,
            self.scrape_website_tool
        ]
    
    def get_writer_tools(self):
        """Get tools for writer agent"""
        return [
            self.serper_dev_tool
        ]
    
    def get_review_tools(self):
        """Get tools for review agent"""
        return [
            self.serper_dev_tool
        ]

# Global instance for easy import
tools_manager = ToolsManager()

# Individual tool instances for backward compatibility
serper_dev_tool = tools_manager.serper_dev_tool
scrape_website_tool = tools_manager.scrape_website_tool