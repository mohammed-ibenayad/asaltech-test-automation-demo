# automation_framework/src/ai_module/config/ai_settings.py
from pathlib import Path
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class AISettings:
    """
    Configuration settings for AI module components.
    Handles loading of API keys and model configurations.
    """
    
    # Model configurations
    MODEL_CONFIGS = {
        "openai": {
            "default_model": "gpt-3.5-turbo",
            "env_key": "OPENAI_API_KEY"
        },
        "deepseek": {
            "base_url": "https://api.deepseek.com/",
            "default_model": "deepseek-chat",
            "env_key": "DEEPSEEK_API_KEY"
        }
    }
    
    def __init__(self, env=None):
        """
        Initialize AI settings
        
        Args:
            env (str): Environment name ('dev', 'staging', 'prod')
        """
        self.env = env or os.getenv('ENV', 'dev')
        self.api_keys = {}
        self._load_api_keys()
    
    def _load_api_keys(self):
        """
        Load API keys from environment variables or .env files
        based on the current environment.
        """
        # Try to find .env file in framework directory structure
        env_paths = [
            Path.cwd() / '.env',
            Path.cwd().parent / '.env',
            Path(__file__).parents[3] / '.env',  # automation_framework directory
            Path(__file__).parents[4] / '.env',  # root project directory
        ]
        
        # Try environment-specific .env files
        env_file = f'.env.{self.env}'
        env_paths.extend([
            Path.cwd() / env_file,
            Path.cwd().parent / env_file,
            Path(__file__).parents[3] / env_file,
            Path(__file__).parents[4] / env_file,
        ])
        
        # Load first available .env file
        for env_path in env_paths:
            if env_path.exists():
                logger.info(f"Loading AI settings from {env_path}")
                load_dotenv(env_path)
                break
        
        # Load keys into dictionary
        for provider, config in self.MODEL_CONFIGS.items():
            key = os.getenv(config["env_key"])
            if key:
                self.api_keys[provider] = key
            else:
                logger.warning(f"API key for {provider} not found using env variable {config['env_key']}")
    
    def get_api_key(self, provider):
        """
        Get API key for the specified provider
        
        Args:
            provider (str): Provider name ('openai', 'deepseek')
            
        Returns:
            str: API key if available
            
        Raises:
            ValueError: If provider is not supported or key is not found
        """
        provider = provider.lower()
        if provider not in self.MODEL_CONFIGS:
            raise ValueError(f"Unsupported AI provider: {provider}. "
                           f"Supported providers: {list(self.MODEL_CONFIGS.keys())}")
        
        if provider not in self.api_keys:
            raise ValueError(f"API key not found for provider: {provider}. "
                           f"Please set {self.MODEL_CONFIGS[provider]['env_key']} environment variable")
        
        return self.api_keys[provider]
    
    def get_model_config(self, provider, model_name=None):
        """
        Get full configuration for a model including API key
        
        Args:
            provider (str): Provider name ('openai', 'deepseek')
            model_name (str, optional): Specific model name to use
            
        Returns:
            dict: Configuration dictionary with provider, api_key, model and optional base_url
        """
        provider = provider.lower()
        if provider not in self.MODEL_CONFIGS:
            raise ValueError(f"Unsupported AI provider: {provider}")
        
        provider_config = self.MODEL_CONFIGS[provider]
        
        config = {
            "provider": provider,
            "api_key": self.get_api_key(provider),
            "model": model_name or provider_config["default_model"]
        }
        
        # Only add base_url for providers that need it
        if "base_url" in provider_config:
            config["base_url"] = provider_config["base_url"]
        
        return config

# Create default settings instance
ai_settings = AISettings()