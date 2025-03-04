# automation_framework/src/ai_module/analyzers/failure_analyzer.py
import json
import httpx
from datetime import datetime
from pathlib import Path
import logging
from openai import OpenAI
from ..config.ai_settings import ai_settings

# Set up logger
logger = logging.getLogger(__name__)

class FailureAnalyzer:
    """
    AI-powered test failure analyzer.
    Uses LLM models to analyze test failures and provide insights.
    """
    
    def __init__(self, config=None):
        """
        Initialize the failure analyzer with the given configuration
        
        Args:
            config (dict, optional): Configuration dictionary with provider, api_key, model
                                     If None, uses default config from ai_settings
        """
        # Use provided config or get default from ai_settings
        if config is None:
            self.config = ai_settings.get_model_config("openai")
        else:
            self.config = config
            
        # Initialize OpenAI client
        client_kwargs = {
            "api_key": self.config["api_key"],
            "http_client": httpx.Client(
                timeout=60.0,
                follow_redirects=True
            )
        }
        
        # Add base_url for non-OpenAI providers
        if "base_url" in self.config:
            client_kwargs["base_url"] = self.config["base_url"]
            
        self.client = OpenAI(**client_kwargs)
        self.model = self.config["model"]
        self.provider = self.config["provider"]
        
        logger.info(f"Initialized FailureAnalyzer with provider: {self.provider}, model: {self.model}")
    
    def analyze_failure(self, failure_data):
        """
        Analyze a test failure using the configured AI provider
        
        Args:
            failure_data (dict): Test failure data including test_name, error_message, etc.
            
        Returns:
            dict: Analysis result with classification, confidence scores, and reasoning
        """
        try:
            prompt = self._build_prompt(failure_data)
            
            logger.debug(f"Sending analysis request to {self.provider} with model {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a test failure analysis expert. 
                    Analyze the provided test failure and return a JSON response with exactly these fields:
                    {
                        "probability_true_bug": float,  // between 0 and 1
                        "category": string,  // determine the most appropriate category based on the failure
                        "subcategory": string,  // more specific classification
                        "confidence": float,  // between 0 and 1
                        "reasoning": string,  // brief explanation
                        "suggested_fix": string  // brief suggestion for fixing the issue
                    }"""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={'type': 'json_object'}, 
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Add metadata to analysis result
            analysis["timestamp"] = datetime.now().isoformat()
            analysis["model"] = self.model
            analysis["provider"] = self.provider
            
            logger.info(f"Analysis completed for test: {failure_data.get('test_name')}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error during failure analysis: {str(e)}", exc_info=True)
            return {
                "error": f"Analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "provider": self.provider
            }
    
    def _build_prompt(self, failure_data):
        """
        Build prompt for LLM analysis
        
        Args:
            failure_data (dict): Test failure data
            
        Returns:
            str: Formatted prompt for the LLM
        """
        return f"""Please analyze this test failure:

Test Name: {failure_data.get('test_name', 'Unknown')}
Error Message: {failure_data.get('error_message', 'Unknown')}
Error Type: {failure_data.get('error_type', 'Unknown')}
Stack Trace: {failure_data.get('stack_trace', 'Not available')}
Environment: {failure_data.get('environment', 'Unknown')}
Test Duration: {failure_data.get('test_duration', 0)}s

Consider:
1. Is this likely a true bug or an environmental/timing issue?
2. What specific category best describes this issue? Be descriptive and specific.
3. Are there any patterns in the stack trace that indicate the root cause?
4. What is a possible fix for this issue?

Provide your analysis in JSON format with accurate probability and confidence scores."""

    def analyze_failures(self, failures):
        """
        Analyze multiple test failures
        
        Args:
            failures (list): List of failure data dictionaries
            
        Returns:
            dict: Analysis results with metadata
        """
        try:
            analysis_start_time = datetime.now()
            
            # Analyze each failure
            analysis_results = []
            for failure in failures:
                logger.info(f"Analyzing failure: {failure.get('test_name', 'Unknown')}")
                analysis = self.analyze_failure(failure)
                analysis_results.append({
                    "test_name": failure.get("test_name", "Unknown"),
                    "failure_data": failure,
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Calculate total analysis time
            analysis_end_time = datetime.now()
            analysis_duration = (analysis_end_time - analysis_start_time).total_seconds()
            
            # Compile results with metadata
            results = {
                "metadata": {
                    "timestamp": analysis_end_time.isoformat(),
                    "provider": self.provider,
                    "model": self.model,
                    "version": "1.0",
                    "analysis_duration_seconds": analysis_duration,
                    "failures_analyzed": len(analysis_results)
                },
                "results": analysis_results
            }
            
            # Log summary
            true_bugs = sum(1 for r in analysis_results 
                        if r["analysis"].get("probability_true_bug", 0) > 0.5)
            
            logger.info(f"Analysis Summary: {len(analysis_results)} failures analyzed")
            logger.info(f"Likely true bugs: {true_bugs}")
            logger.info(f"Likely false positives: {len(analysis_results) - true_bugs}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during batch analysis: {str(e)}", exc_info=True)
            return {
                "error": f"Batch analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }