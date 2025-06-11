# Job Posting Crew 🚀

An intelligent AI-powered job posting generator that uses CrewAI's multi-agent system to create compelling, tailored job descriptions. The system analyzes company culture, researches role requirements, and generates professional job postings that attract the right candidates.

## 🎯 Features

- **Multi-Agent AI System**: Utilizes specialized AI agents for research, writing, and editing
- **Company Culture Analysis**: Automatically scrapes and analyzes company websites for culture insights
- **Industry Research**: Conducts market analysis to position roles competitively
- **Interactive Input Collection**: User-friendly interface for gathering job requirements
- **Rate Limit Management**: Built-in API quota management and retry logic
- **File Management**: Automatic saving with organized output structure
- **Multiple Operation Modes**: Interactive, quick-start, and training modes

## 🏗️ Architecture

The system consists of three specialized AI agents:

### 1. Research Analyst Agent
- Analyzes company websites and descriptions
- Extracts culture, values, and mission insights
- Researches industry trends and requirements
- Identifies key selling points for job postings

### 2. Job Description Writer Agent
- Creates compelling job posting drafts
- Incorporates company culture insights
- Aligns content with hiring needs and benefits
- Ensures engaging and attractive language

### 3. Review and Editing Specialist Agent
- Reviews drafts for clarity and engagement
- Checks grammatical accuracy and alignment
- Refines content for maximum impact
- Provides final polished job postings

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Serper API key (for web search)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/naakaarafr/Job-Posting-Crew.git
   cd Job-Posting-Crew
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

4. **Get API Keys**
   - **Google Gemini API**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - **Serper API**: Visit [Serper.dev](https://serper.dev/) for web search capabilities

## 🚀 Usage

### Interactive Mode (Default)
```bash
python main.py
```
Provides a guided interface for entering all job posting details.

### Quick Start Mode
```bash
python main.py quick
```
Streamlined input collection for rapid job posting generation.

### Training Mode
```bash
python main.py train <number_of_iterations>
```
Train the AI agents with your specific data patterns.

### File Management
```bash
# List recent job postings
python main.py list

# Clean up old files (default: 30 days)
python main.py cleanup [days]

# Show help
python main.py help
```

## 📋 Input Requirements

### Required Inputs
- **Company Domain**: Website URL for analysis
- **Company Description**: Mission, values, and what the company does
- **Hiring Needs**: Role title, location, start date, key requirements
- **Specific Benefits**: Salary range, healthcare, perks, etc.

### Optional Inputs
- Additional requirements or preferences
- Company culture information
- Remote work policy details

## 📁 Output Structure

Generated files are saved in the `job_postings_output/` directory:

```
job_postings_output/
├── CompanyName_RoleName_20240611_143022.md    # Job posting
├── CompanyName_RoleName_20240611_143022.json  # Metadata
└── ...
```

### Output Features
- **Markdown Format**: Easy to read and edit
- **Metadata Tracking**: JSON files with generation details
- **Timestamp Organization**: Chronological file naming
- **Content Preservation**: Full input parameters saved

## ⚙️ Configuration

### Rate Limiting
The system includes intelligent rate limiting for API quota management:
- Exponential backoff with jitter
- Configurable retry attempts
- Automatic quota detection and handling

### LLM Settings
- **Model**: Gemini 1.5 Flash (optimized for quota efficiency)
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 800 (quota-conscious)

## 🔧 Customization

### Modifying Agents
Edit `agents.py` to customize agent roles, goals, and behaviors:
```python
def create_research_agent():
    return Agent(
        role="Research Analyst",
        goal="Your custom goal here",
        backstory="Your custom backstory here",
        # ... other parameters
    )
```

### Adjusting Tasks
Modify `tasks.py` to change task descriptions and expected outputs:
```python
def create_research_company_culture_task(agent):
    return Task(
        description="Your custom task description",
        expected_output="Your expected output format",
        agent=agent
    )
```

### Configuration Options
Update `config.py` for system-wide settings:
```python
# Rate limiting
BASE_REQUEST_DELAY = 5.0
MAX_RETRIES = 5

# LLM parameters
max_tokens = 800
temperature = 0.7
```

## 📊 Example Output

The system generates comprehensive job postings including:
- Compelling company introduction
- Detailed role descriptions
- Clear responsibilities and requirements
- Attractive benefits and perks
- Company culture alignment
- Industry-specific insights

## 🔍 Troubleshooting

### Common Issues

**API Key Errors**
- Ensure API keys are set in `.env` file
- Verify keys are active and have sufficient quota

**Rate Limiting**
- The system automatically handles rate limits
- Consider upgrading API plans for higher limits
- Use training mode sparingly to conserve quota

**Output Quality**
- Provide detailed, specific inputs for better results
- Use the edit feature to refine inputs before generation
- Consider multiple iterations for optimal output

### Error Messages
- `ResourceExhausted`: API quota exceeded - wait or upgrade plan
- `Missing API Key`: Check environment variable setup
- `Invalid Domain`: Ensure company domain is accessible

## 🧪 Development

### Project Structure
```
Job-Posting-Crew/
├── agents.py          # AI agent definitions
├── config.py          # Configuration and rate limiting
├── crew.py           # CrewAI crew orchestration
├── main.py           # Main application entry point
├── tasks.py          # Task definitions for agents
├── tools.py          # Tool management and initialization
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this)
└── job_postings_output/  # Generated output directory
```

### Adding New Features
1. **New Agent**: Add to `agents.py` and update `crew.py`
2. **New Task**: Add to `tasks.py` and link to appropriate agent
3. **New Tool**: Add to `tools.py` and assign to relevant agents
4. **New Config**: Add to `config.py` with proper validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent AI framework
- **Google Gemini**: Large language model
- **Serper**: Web search API
- **LangChain**: AI application framework

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation for Gemini and Serper
3. Open an issue on the project repository
4. Ensure API keys have sufficient quota

---

**Made with ❤️ by the Job Posting Crew Team**
