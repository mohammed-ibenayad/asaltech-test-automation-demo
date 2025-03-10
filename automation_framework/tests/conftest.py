# automation_framework/tests/conftest.py
import pytest
import json
import traceback
from pathlib import Path
import logging
from datetime import datetime

# Import AI module components
from automation_framework.src.ai_module.config.ai_settings import ai_settings
from automation_framework.src.ai_module.analyzers.failure_analyzer import FailureAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

# Define output directory for test results
OUTPUT_DIR = Path("test_results")
FAILURES_FILE = OUTPUT_DIR / "failures.json"

def pytest_addoption(parser):
    """Add command-line options for browser and AI configuration"""
    # Existing browser options
    parser.addoption("--browser", default="chrome", help="Browser to run tests on")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    
    # New AI analysis options
    parser.addoption(
        "--ai-provider",
        action="store",
        default="openai",
        help="AI provider to use for analysis (openai/deepseek)"
    )
    parser.addoption(
        "--model-name",
        action="store",
        help="Specific model name to use for analysis (optional)"
    )
    parser.addoption(
        "--analyze-failures",
        action="store_true",
        help="Automatically analyze failures after test run"
    )

@pytest.fixture(scope="session")
def ai_config(request):
    """Fixture to provide AI configuration for test analysis"""
    provider = request.config.getoption("--ai-provider")
    model_name = request.config.getoption("--model-name")
    
    try:
        return ai_settings.get_model_config(provider, model_name)
    except ValueError as e:
        logger.warning(f"AI configuration error: {str(e)}")
        logger.warning("Falling back to default OpenAI configuration")
        return ai_settings.get_model_config("openai")

@pytest.fixture(scope="session")
def failure_analyzer(ai_config):
    """Fixture to provide a configured FailureAnalyzer instance"""
    return FailureAnalyzer(ai_config)

def pytest_configure(config):
    """Set up test environment and ensure output directories exist"""
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Initialize failures file for this test run
    if config.getoption("--analyze-failures"):
        # Create an empty failures file
        with open(FAILURES_FILE, "w") as f:
            f.write("")

def format_traceback(excinfo):
    """Format traceback in a readable way"""
    return ''.join(traceback.format_exception(
        excinfo.type,
        excinfo.value,
        excinfo.tb
    ))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect test failures during the call phase"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Ensure directory exists
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Get formatted traceback if available
        if call.excinfo:
            trace = format_traceback(call.excinfo)
            error_type = call.excinfo.type.__name__
            error_message = str(call.excinfo.value)
        else:
            trace = "No traceback available"
            error_type = "Unknown"
            error_message = "Test failed without exception"

        # Create failure data
        failure_data = {
            "test_name": item.nodeid,
            "test_class": item.cls.__name__ if hasattr(item, 'cls') and item.cls else None,
            "test_module": item.module.__name__ if hasattr(item, 'module') else None,
            "error_type": error_type,
            "error_message": error_message,
            "stack_trace": trace,
            "environment": item.config.getoption("--env", default="test"),
            "test_duration": call.duration if hasattr(call, 'duration') else 0.0,
            "test_phase": report.when,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write failure to file
        with open(FAILURES_FILE, "a", encoding='utf-8') as f:
            json.dump(failure_data, f, ensure_ascii=False)
            f.write("\n")
        
        logger.info(f"Test failure recorded: {item.nodeid}")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Run analysis on failures at the end of test execution if enabled"""
    if not config.getoption("--analyze-failures") or exitstatus == 0:
        # Skip analysis if not enabled or all tests passed
        return
    
    if not FAILURES_FILE.exists() or FAILURES_FILE.stat().st_size == 0:
        logger.info("No failures recorded to analyze")
        return
    
    # Read and parse failures
    failures = []
    try:
        with open(FAILURES_FILE) as f:
            for line in f:
                if line.strip():
                    failures.append(json.loads(line))
    except Exception as e:
        logger.error(f"Error reading failures file: {e}")
        return
    
    if not failures:
        logger.info("No failures found in failures file")
        return
    
    try:
        # Create analyzer with configured AI provider
        analyzer = FailureAnalyzer(ai_config(config))
        
        # Analyze failures
        logger.info(f"Analyzing {len(failures)} test failures...")
        results = analyzer.analyze_failures(failures)
        
        # Save analysis results
        analysis_file = OUTPUT_DIR / "analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Analysis results saved to {analysis_file}")
        
        # Print summary to terminal
        terminalreporter.write_sep("=", "AI Analysis Summary")
        
        metadata = results.get("metadata", {})
        terminalreporter.write_line(f"Provider: {metadata.get('provider')}")
        terminalreporter.write_line(f"Model: {metadata.get('model')}")
        
        # Count true bugs vs false positives
        true_bugs = sum(1 for r in results.get("results", []) 
                    if r.get("analysis", {}).get("probability_true_bug", 0) > 0.5)
        
        terminalreporter.write_line(f"Likely true bugs: {true_bugs}")
        terminalreporter.write_line(f"Likely false positives: {len(failures) - true_bugs}")
        terminalreporter.write_line(f"Analysis results saved in {analysis_file}")
        
    except Exception as e:
        logger.error(f"Error during failure analysis: {str(e)}", exc_info=True)
        terminalreporter.write_line(f"Error during failure analysis: {str(e)}", red=True)