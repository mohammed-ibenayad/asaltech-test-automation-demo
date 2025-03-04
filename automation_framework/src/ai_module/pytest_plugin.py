# automation_framework/src/ai_module/pytest_plugin.py
import pytest
import json
from pathlib import Path
import traceback
from datetime import datetime
import logging

from .analyzers.failure_analyzer import FailureAnalyzer
from .config.ai_settings import ai_settings

logger = logging.getLogger(__name__)

# Constants
OUTPUT_DIR = Path("test_results")
FAILURES_FILE = OUTPUT_DIR / "failures.json"

def pytest_addoption(parser):
    """Add command-line options for AI configuration"""
    group = parser.getgroup("ai_analysis", "AI-powered test analysis")
    group.addoption(
        "--ai-provider",
        action="store",
        default="openai",
        help="AI provider to use for analysis (openai/deepseek)"
    )
    group.addoption(
        "--model-name",
        action="store",
        help="Specific model name to use for analysis (optional)"
    )
    group.addoption(
        "--analyze-failures",
        action="store_true",
        help="Automatically analyze failures after test run"
    )

@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Set up test environment and ensure output directories exist"""
    if not config.option.analyze_failures:
        return

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Initialize failures file for this test run
    with open(FAILURES_FILE, "w") as f:
        f.write("")
    
    logger.info("AI failure analysis enabled")

def _format_traceback(excinfo):
    """Format traceback in a readable way"""
    return ''.join(traceback.format_exception(
        excinfo.type,
        excinfo.value,
        excinfo.tb
    ))

@pytest.hookimpl(trylast=True)
def pytest_runtest_makereport(item, call):
    """Collect test failures during the call phase"""
    if not item.config.option.analyze_failures:
        return
        
    if call.when == "call" and call.excinfo is not None:
        # Ensure directory exists
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Get formatted traceback
        trace = _format_traceback(call.excinfo)
        error_type = call.excinfo.type.__name__
        error_message = str(call.excinfo.value)

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
            "test_phase": "call",
            "timestamp": datetime.now().isoformat()
        }
        
        # Write failure to file
        with open(FAILURES_FILE, "a", encoding='utf-8') as f:
            json.dump(failure_data, f, ensure_ascii=False)
            f.write("\n")
        
        logger.info(f"Test failure recorded: {item.nodeid}")

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Run analysis on failures at the end of test execution if enabled"""
    if not config.option.analyze_failures or exitstatus == 0:
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
        # Get provider and model from options
        provider = config.getoption("--ai-provider", default="openai")
        model_name = config.getoption("--model-name", default=None)
        
        # Create configuration
        ai_config = ai_settings.get_model_config(provider, model_name)
        
        # Create analyzer
        analyzer = FailureAnalyzer(ai_config)
        
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
        results_list = results.get("results", [])
        true_bugs = sum(1 for r in results_list 
                    if r.get("analysis", {}).get("probability_true_bug", 0) > 0.5)
        
        terminalreporter.write_line(f"Likely true bugs: {true_bugs}")
        terminalreporter.write_line(f"Likely false positives: {len(failures) - true_bugs}")
        terminalreporter.write_line(f"Analysis results saved in {analysis_file}")
        
    except Exception as e:
        logger.error(f"Error during failure analysis: {str(e)}", exc_info=True)
        terminalreporter.write_line(f"Error during failure analysis: {str(e)}", red=True)