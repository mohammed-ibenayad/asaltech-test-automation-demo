# automation_framework/src/ai_module/reporters/ai_report_generator.py
import json
import os
from pathlib import Path
import datetime
import logging
from jinja2 import Environment, FileSystemLoader

# Import the existing HTML reporter to extend its functionality
from ....src.reporters.html_reporter import HTMLReporter

logger = logging.getLogger(__name__)

class AIReportGenerator:
    """
    Generates AI-specific analysis reports and extends the standard HTML reporter
    with AI insights when available.
    """
    
    def __init__(self, output_dir="reports"):
        """
        Initialize the AI report generator
        
        Args:
            output_dir (str): Directory to save reports (should match main reporter)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up Jinja2 environment for templates
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
    
    def generate_analysis_report(self, analysis_results, report_name=None):
        """
        Generate a specialized report focusing on failure analysis
        
        Args:
            analysis_results (dict): AI analysis results
            report_name (str, optional): Custom report name
            
        Returns:
            str: Path to generated report
        """
        if report_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"ai_analysis_{timestamp}.html"
        
        report_path = self.output_dir / report_name
        
        # Prepare template data
        template_data = {
            "title": "AI-Powered Failure Analysis",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_results": analysis_results,
            "metadata": analysis_results.get("metadata", {}),
            "results": analysis_results.get("results", [])
        }
        
        # Add statistics
        template_data["stats"] = self._calculate_analysis_stats(analysis_results)
        
        # Render template
        template = self.jinja_env.get_template("ai_analysis_template.html")
        report_html = template.render(**template_data)
        
        # Write to file
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_html)
        
        logger.info(f"AI analysis report generated: {report_path}")
        
        return str(report_path)
    
    def enhance_html_report(self, html_reporter, test_results):
        """
        Enhance standard HTML report with AI analysis insights
        
        Args:
            html_reporter (HTMLReporter): Instance of the standard HTML reporter
            test_results (dict): Test execution results
            
        Returns:
            str: Path to enhanced report
        """
        # First, load analysis results if available
        analysis_results = self._load_analysis_results()
        if not analysis_results:
            # No analysis available, generate standard report only
            logger.info("No AI analysis results found, generating standard report only")
            return html_reporter.generate_report(test_results)
        
        # If analysis is available, generate both reports
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate standard report first
        standard_report = html_reporter.generate_report(test_results)
        
        # Then generate AI analysis report
        ai_report = self.generate_analysis_report(analysis_results, 
                                                 f"ai_analysis_{timestamp}.html")
        
        logger.info(f"Enhanced reporting complete. Standard report: {standard_report}, AI report: {ai_report}")
        
        # Return both report paths
        return {
            "standard_report": standard_report,
            "ai_report": ai_report
        }
    
    def _load_analysis_results(self):
        """
        Load AI analysis results if available
        
        Returns:
            dict: Analysis results or None if not available
        """
        analysis_file = Path("test_results") / "analysis.json"
        
        if not analysis_file.exists():
            logger.debug(f"Analysis file not found: {analysis_file}")
            return None
        
        try:
            with open(analysis_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading analysis results: {str(e)}")
            return None
    
    def _calculate_analysis_stats(self, analysis_results):
        """
        Calculate statistics from analysis results
        
        Args:
            analysis_results (dict): AI analysis results
            
        Returns:
            dict: Statistics about the analysis
        """
        results = analysis_results.get("results", [])
        total = len(results)
        
        if total == 0:
            return {
                "total": 0,
                "true_bugs": 0,
                "false_positives": 0,
                "true_bug_percentage": 0,
                "categories": {},
                "high_confidence": 0
            }
        
        # Count true bugs
        true_bugs = sum(1 for r in results 
                    if r.get("analysis", {}).get("probability_true_bug", 0) > 0.5)
        
        # Count high confidence results
        high_confidence = sum(1 for r in results 
                          if r.get("analysis", {}).get("confidence", 0) > 0.8)
        
        # Count categories
        categories = {}
        for r in results:
            category = r.get("analysis", {}).get("category", "Unknown")
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total": total,
            "true_bugs": true_bugs,
            "false_positives": total - true_bugs,
            "true_bug_percentage": (true_bugs / total * 100) if total > 0 else 0,
            "categories": categories,
            "high_confidence": high_confidence
        }