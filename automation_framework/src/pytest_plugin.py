# automation_framework/src/ai_module/pytest_plugin.py
import pytest
import json
from pathlib import Path
import traceback
from datetime import datetime
import logging
import sys
import os

logger = logging.getLogger(__name__)

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
    group.addoption(
        "--output-dir",
        action="store",
        help="Custom output directory for test results and reports (relative to project root)"
    )

def _get_app_name_from_path(paths):
    """Extract the app name from the test paths"""
    # Example path: examples/web_the_internet/tests/test_login.py
    if not paths:
        return None
        
    # Convert to Path objects if strings
    path_objs = [Path(p) if isinstance(p, str) else p for p in paths]
    
    # Try to extract the app name from the first path
    for path in path_objs:
        parts = path.parts
        # Look for 'examples' directory in the path
        if 'examples' in parts:
            idx = parts.index('examples')
            if idx + 1 < len(parts):  # Make sure there's a part after 'examples'
                return parts[idx + 1]  # Return the app name (e.g., 'web_the_internet')
    
    return None

@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Set up test environment and ensure output directories exist"""
    if not config.option.analyze_failures:
        return

    # Determine the output directory
    output_dir = _get_output_dir(config)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Store the output directory in config for later use
    config._asaltech_output_dir = output_dir
    
    # Initialize failures file for this test run
    failures_file = output_dir / "failures.json"
    with open(failures_file, "w") as f:
        f.write("")
    
    logger.info(f"AI failure analysis enabled. Output directory: {output_dir}")

def _get_output_dir(config):
    """Determine the output directory based on config and test paths"""
    # Check if a custom output directory was specified
    if hasattr(config.option, 'output_dir') and config.option.output_dir:
        return Path(config.option.output_dir)
    
    # Try to determine the app name from the test paths
    app_name = _get_app_name_from_path(config.args)
    
    if app_name:
        # Create app-specific output directory
        return Path("examples") / app_name / "test_results"
    else:
        # Fallback to default
        return Path("test_results")

def _format_traceback(excinfo):
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
    
    if not hasattr(item.config.option, 'analyze_failures') or not item.config.option.analyze_failures:
        return
        
    if report.when == "call" and report.outcome == "failed":
        # Get exception info from the report
        longrepr = getattr(report, 'longrepr', None)
        if longrepr is None:
            return
        
        # Get the output directory from config
        output_dir = getattr(item.config, '_asaltech_output_dir', Path("test_results"))
        failures_file = output_dir / "failures.json"
            
        # Try to extract error information
        try:
            if hasattr(call, 'excinfo') and call.excinfo is not None:
                error_type = call.excinfo.type.__name__
                error_message = str(call.excinfo.value)
                trace = _format_traceback(call.excinfo)
            else:
                # Fallback to using the report's representation
                if hasattr(longrepr, 'reprcrash'):
                    error_type = longrepr.reprcrash.message.split(':')[0]
                    error_message = longrepr.reprcrash.message
                    trace = str(longrepr)
                else:
                    error_type = "Unknown"
                    error_message = str(longrepr)
                    trace = str(longrepr)
                    
            # Create failure data
            failure_data = {
                "test_name": item.nodeid,
                "test_class": item.cls.__name__ if hasattr(item, 'cls') and item.cls else None,
                "test_module": item.module.__name__ if hasattr(item, 'module') else None,
                "error_type": error_type,
                "error_message": error_message,
                "stack_trace": trace,
                "environment": getattr(item.config.option, 'env', 'test'),
                "test_duration": call.duration if hasattr(call, 'duration') else 0.0,
                "test_phase": report.when,
                "timestamp": datetime.now().isoformat()
            }
            
            # Create output directory if it doesn't exist
            output_dir.mkdir(exist_ok=True, parents=True)
            
            # Write failure to file
            with open(failures_file, "a", encoding='utf-8') as f:
                json.dump(failure_data, f, ensure_ascii=False)
                f.write("\n")
            
            logger.info(f"Test failure recorded: {item.nodeid} in {failures_file}")
            
        except Exception as e:
            logger.error(f"Error recording test failure: {e}", exc_info=True)

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Run analysis on failures at the end of test execution if enabled"""
    if not hasattr(config.option, 'analyze_failures') or not config.option.analyze_failures:
        return
    
    if exitstatus == 0:
        logger.info("All tests passed, no analysis needed")
        return
    
    # Direct implementation that doesn't rely on complex pytest hooks
    analyze_failures(terminalreporter, config)

def analyze_failures(terminalreporter, config):
    """Analyze the failures file and generate a report"""
    try:
        # Import here to avoid circular imports
        from automation_framework.src.ai_module.analyzers.failure_analyzer import FailureAnalyzer
        from automation_framework.src.ai_module.config.ai_settings import ai_settings
        
        # Get the output directory from config
        output_dir = getattr(config, '_asaltech_output_dir', Path("test_results"))
        failures_file = output_dir / "failures.json"
        
        # Check if the failures file exists
        if not failures_file.exists():
            logger.warning(f"Failures file does not exist: {failures_file}")
            return
            
        # Check if the file is empty
        if failures_file.stat().st_size == 0:
            logger.info("No failures recorded to analyze (empty file)")
            return
            
        # Read failures from the file
        failures = []
        with open(failures_file) as f:
            for line in f:
                if line.strip():
                    failures.append(json.loads(line))
        
        if not failures:
            logger.info("No failures found in the failures file")
            return
            
        # Get provider and model from options
        provider = getattr(config.option, 'ai_provider', 'openai')
        model_name = getattr(config.option, 'model_name', None)
        
        # Create AI configuration
        ai_config = ai_settings.get_model_config(provider, model_name)
        
        # Create analyzer
        analyzer = FailureAnalyzer(ai_config)
        
        # Run analysis
        logger.info(f"Analyzing {len(failures)} test failures...")
        results = analyzer.analyze_failures(failures)
        
        # Save analysis results
        analysis_file = output_dir / "analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        terminalreporter.write_sep("=", "AI Analysis Summary")
        terminalreporter.write_line(f"Analysis results saved to {analysis_file}")
        
        metadata = results.get("metadata", {})
        terminalreporter.write_line(f"Provider: {metadata.get('provider')}")
        terminalreporter.write_line(f"Model: {metadata.get('model')}")
        
        # Count true bugs vs false positives
        true_bugs = sum(1 for r in results.get("results", []) 
                    if r.get("analysis", {}).get("probability_true_bug", 0) > 0.5)
        
        terminalreporter.write_line(f"Likely true bugs: {true_bugs}")
        terminalreporter.write_line(f"Likely false positives: {len(failures) - true_bugs}")
        
        # Generate HTML report
        try:
            # Correct import path for AIReportGenerator
            from automation_framework.src.reporters.ai_report_generator import AIReportGenerator
            
            # Create reports directory at the same level as the output directory
            reports_dir = output_dir.parent / "reports" 
            reports_dir.mkdir(exist_ok=True, parents=True)
            
            # Generate timestamp for unique report name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"ai_analysis_{timestamp}.html"
            
            # Create reporter and generate report
            reporter = AIReportGenerator(output_dir=str(reports_dir))
            report_path = reporter.generate_analysis_report(results, report_name)
            
            terminalreporter.write_line(f"AI analysis HTML report generated: {report_path}")
            
        except ImportError as e:
            # Log the import error with more details
            logger.error(f"Error importing AIReportGenerator: {e}")
            terminalreporter.write_line("Could not generate HTML report - AIReportGenerator not found", red=True)
        except Exception as e:
            # Handle other exceptions during report generation
            logger.error(f"Error generating HTML report: {e}", exc_info=True)
            terminalreporter.write_line(f"Error generating HTML report: {str(e)}", red=True)
            
    except Exception as e:
        logger.error(f"Error during failure analysis: {e}", exc_info=True)
        terminalreporter.write_line(f"Error during failure analysis: {str(e)}", red=True)