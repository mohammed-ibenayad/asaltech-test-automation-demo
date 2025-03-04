# automation_framework/src/ai_module/run_analysis.py
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Import framework components
from .analyzers.failure_analyzer import FailureAnalyzer
from .config.ai_settings import ai_settings
from .reporters.ai_report_generator import AIReportGenerator
from ..reporters.html_reporter import HTMLReporter

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run AI analysis on test failures')
    parser.add_argument('--failures-file', 
                      default="test_results/failures.json",
                      help='Path to the failures JSON file')
    parser.add_argument('--output-dir',
                      default="reports",
                      help='Directory for output reports')
    parser.add_argument('--ai-provider', 
                      default="openai",
                      help='AI provider to use (openai/deepseek)')
    parser.add_argument('--model-name',
                      help='Specific model name to use (optional)')
    parser.add_argument('--report-only',
                      action='store_true',
                      help='Generate reports from existing analysis without running new analysis')
    return parser.parse_args()

def run_analysis():
    """Run AI analysis on test failures and generate reports"""
    args = parse_args()
    
    # Initialize logging
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    failures_file = Path(args.failures_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    if not failures_file.exists():
        logger.error(f"Failures file not found: {failures_file}")
        return 1
    
    # Read failures
    try:
        failures = []
        with open(failures_file) as f:
            for line in f:
                if line.strip():
                    failures.append(json.loads(line))
    except Exception as e:
        logger.error(f"Error reading failures file: {e}")
        return 1
    
    if not failures:
        logger.info("No failures found to analyze")
        return 0
    
    # Output file for analysis results
    analysis_file = Path("test_results") / "analysis.json"
    
    if not args.report_only:
        # Configure AI analyzer
        config = ai_settings.get_model_config(args.ai_provider, args.model_name)
        analyzer = FailureAnalyzer(config)
        
        # Run analysis
        logger.info(f"Analyzing {len(failures)} failures using {config['provider']}/{config['model']}...")
        results = analyzer.analyze_failures(failures)
        
        # Save analysis results
        with open(analysis_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Analysis complete. Results saved to: {analysis_file}")
    else:
        # Load existing analysis
        if not analysis_file.exists():
            logger.error(f"No analysis file found at {analysis_file} for report generation")
            return 1
            
        try:
            with open(analysis_file, 'r') as f:
                results = json.load(f)
            logger.info(f"Loaded existing analysis from {analysis_file}")
        except Exception as e:
            logger.error(f"Error loading analysis results: {e}")
            return 1
    
    # Generate reports
    ai_reporter = AIReportGenerator(output_dir=str(output_dir))
    report_path = ai_reporter.generate_analysis_report(results)
    
    logger.info(f"AI analysis report generated: {report_path}")
    
    return 0

if __name__ == "__main__":
    exit(run_analysis())