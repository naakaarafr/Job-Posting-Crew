import os
import time
import random
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """
    Enhanced Configuration class for the Job Posting Crew application.
    Manages all environment variables and settings with improved rate limiting.
    """
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    
    # Enhanced Rate limiting configuration
    BASE_REQUEST_DELAY = 5.0  # Increased base delay
    MAX_REQUEST_DELAY = 120.0  # Maximum delay for exponential backoff
    RATE_LIMIT_DELAY = 180.0  # 3 minutes when rate limited (increased)
    MAX_RETRIES = 5  # Increased max retries
    EXPONENTIAL_BACKOFF_MULTIPLIER = 2.0
    JITTER_MAX = 2.0  # Add randomness to avoid thundering herd
    
    # LLM Configuration with conservative settings
    @property
    def DEFAULT_LLM(self):
        """Initialize and return the default LLM with conservative settings"""
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required for Gemini LLM")
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.GOOGLE_API_KEY,
            temperature=0.7,
            max_tokens=800,  # Further reduced to minimize quota usage
            request_timeout=120,  # Increased timeout
            max_retries=0,  # Disable built-in retries to handle them manually
            # Add rate limiting parameters
            rate_limiter=None  # We'll handle rate limiting manually
        )
    
    # Agent Configuration - reduced verbosity to minimize API calls
    AGENT_VERBOSE = False  # Disabled to reduce API calls
    CREW_VERBOSE = 0  # Minimal verbosity
    
    @staticmethod
    def calculate_delay(attempt: int, base_delay: float = None) -> float:
        """Calculate delay with exponential backoff and jitter"""
        if base_delay is None:
            base_delay = Config.BASE_REQUEST_DELAY
            
        # Exponential backoff
        delay = min(
            base_delay * (Config.EXPONENTIAL_BACKOFF_MULTIPLIER ** attempt),
            Config.MAX_REQUEST_DELAY
        )
        
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0, Config.JITTER_MAX)
        return delay + jitter
    
    @staticmethod
    def wait_between_requests(attempt: int = 0):
        """Add intelligent delay between requests to avoid rate limits"""
        delay = Config.calculate_delay(attempt)
        logger.info(f"Waiting {delay:.2f} seconds to avoid rate limits (attempt {attempt + 1})...")
        time.sleep(delay)
    
    @staticmethod
    def handle_rate_limit(retry_delay_seconds: int = None):
        """Handle rate limit by waiting the specified time or default"""
        if retry_delay_seconds:
            # Use the delay suggested by the API
            delay = max(retry_delay_seconds, Config.RATE_LIMIT_DELAY)
        else:
            delay = Config.RATE_LIMIT_DELAY
            
        logger.warning(f"Rate limit detected. Waiting {delay} seconds...")
        time.sleep(delay)
    
    @staticmethod
    def extract_retry_delay(error_message: str) -> int:
        """Extract retry delay from error message if available"""
        try:
            # Look for retry_delay in the error message
            if "retry_delay" in error_message and "seconds" in error_message:
                # Extract the seconds value
                import re
                match = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', error_message)
                if match:
                    return int(match.group(1))
        except Exception:
            pass
        return None
    
    @staticmethod
    def execute_with_retry(func, *args, max_retries: int = None, **kwargs):
        """Execute a function with intelligent retry logic"""
        if max_retries is None:
            max_retries = Config.MAX_RETRIES
            
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    Config.wait_between_requests(attempt)
                
                return func(*args, **kwargs)
                
            except ResourceExhausted as e:
                last_exception = e
                error_message = str(e)
                logger.warning(f"Rate limit hit on attempt {attempt + 1}/{max_retries}: {error_message}")
                
                # Extract suggested retry delay from error
                suggested_delay = Config.extract_retry_delay(error_message)
                
                if attempt < max_retries - 1:  # Don't wait on the last attempt
                    Config.handle_rate_limit(suggested_delay)
                else:
                    logger.error(f"Max retries ({max_retries}) reached for rate limiting")
                    
            except Exception as e:
                last_exception = e
                logger.error(f"Non-rate-limit error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    Config.wait_between_requests(attempt)
                else:
                    break
        
        # If we get here, all retries failed
        if last_exception:
            raise last_exception
        else:
            raise Exception(f"Function failed after {max_retries} attempts")
    
    # Enhanced Validation
    @classmethod
    def validate_required_keys(cls):
        """Validate that required API keys are present and check quotas"""
        missing_keys = []
        
        if not cls.GOOGLE_API_KEY:
            missing_keys.append('GOOGLE_API_KEY')
        
        if not cls.SERPER_API_KEY:
            missing_keys.append('SERPER_API_KEY')
        
        if missing_keys:
            logger.error(f"Missing required environment variables: {', '.join(missing_keys)}")
            logger.info("Please set these in your .env file or environment variables.")
            return False
        
        # Test the Gemini API key with a minimal request
        try:
            logger.info("Testing Gemini API connection...")
            test_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=cls.GOOGLE_API_KEY,
                max_tokens=10,
                temperature=0
            )
            # Make a minimal test call
            test_response = test_llm.invoke("Hello")
            logger.info("✅ Gemini API connection successful")
        except ResourceExhausted as e:
            logger.error("❌ Gemini API quota exceeded. Please check your billing and quota limits.")
            logger.error(f"Error: {e}")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Gemini API test failed, but continuing: {e}")
        
        return True
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables for the application"""
        if cls.GOOGLE_API_KEY:
            os.environ['GOOGLE_API_KEY'] = cls.GOOGLE_API_KEY
        
        if cls.SERPER_API_KEY:
            os.environ['SERPER_API_KEY'] = cls.SERPER_API_KEY
        
        if cls.SERPAPI_API_KEY:
            os.environ['SERPAPI_API_KEY'] = cls.SERPAPI_API_KEY
    
    @classmethod
    def get_quota_friendly_settings(cls):
        """Return settings optimized for low quota usage"""
        return {
            'max_tokens': 500,  # Reduced for quota conservation
            'temperature': 0.5,  # Lower creativity for consistency
            'timeout': 180,  # Longer timeout for delayed responses
        }
    
    @classmethod
    def print_quota_tips(cls):
        """Print helpful tips for managing API quotas"""
        print("\n💡 QUOTA MANAGEMENT TIPS:")
        print("="*50)
        print("1. Check your Gemini API quota at: https://aistudio.google.com/app/apikey")
        print("2. Consider upgrading your plan for higher limits")
        print("3. Run tasks sequentially rather than in parallel")
        print("4. Reduce max_tokens to conserve quota")
        print("5. Use verbose=False to minimize unnecessary API calls")
        print("6. Test with smaller inputs first")
        print("="*50)

# Initialize configuration
config = Config()

# Setup environment on import
config.setup_environment()