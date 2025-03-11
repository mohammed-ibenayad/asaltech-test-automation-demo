# automation_framework/src/reporters/ai_report_generator.py
import json
import os
from pathlib import Path
import datetime
import logging
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class AIReportGenerator:
    """
    Generates AI-specific analysis reports based on failure analysis results.
    """
    
    def __init__(self, output_dir="reports"):
        """
        Initialize the AI report generator
        
        Args:
            output_dir (str): Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Set up Jinja2 environment for templates
        # Look for templates in multiple locations to handle different project structures
        possible_template_dirs = [
            Path(__file__).parent / "templates",  # Same directory as this file
            Path(__file__).parent.parent / "ai_module" / "reporters" / "templates",  # AI module path
            Path(__file__).parent.parent.parent / "automation_framework" / "src" / "reporters" / "templates",  # From project root
            Path.cwd() / "automation_framework" / "src" / "reporters" / "templates",  # From current directory
        ]
        
        # Find the first directory that exists and contains the template
        template_dir = None
        for directory in possible_template_dirs:
            if directory.exists() and (directory / "ai_analysis_template.html").exists():
                template_dir = directory
                break
        
        if template_dir is None:
            # If no template directory is found, create a default one
            template_dir = self.output_dir / "templates"
            template_dir.mkdir(exist_ok=True)
            self._create_default_template(template_dir)
            
        logger.info(f"Using template directory: {template_dir}")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
    
    def _create_default_template(self, template_dir):
        """Create a default template if none exists"""
        template_path = template_dir / "ai_analysis_template.html"
        with open(template_path, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { background-color: #f4f4f4; padding: 20px; margin-bottom: 20px; }
        .true-bug { background-color: #ffecec; border-left: 5px solid #f44336; padding: 15px; margin-bottom: 15px; }
        .false-positive { background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p>Generated: {{ timestamp }}</p>
            <p>Model: {{ metadata.provider }} / {{ metadata.model }}</p>
        </header>
        
        <section>
            <h2>Analysis Summary</h2>
            <p>Total Failures: {{ stats.total }}</p>
            <p>True Bugs: {{ stats.true_bugs }}</p>
            <p>False Positives: {{ stats.false_positives }}</p>
        </section>
        
        <section>
            <h2>Failure Analysis Details</h2>
            {% for result in results %}
            <div class="{% if result.analysis.probability_true_bug > 0.5 %}true-bug{% else %}false-positive{% endif %}">
                <h3>{{ result.test_name }}</h3>
                <p><strong>Category:</strong> {{ result.analysis.category }}</p>
                <p><strong>Analysis:</strong> {{ result.analysis.reasoning }}</p>
                {% if result.analysis.suggested_fix %}
                <p><strong>Suggested Fix:</strong> {{ result.analysis.suggested_fix }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </section>
    </div>
</body>
</html>""")
        logger.info(f"Created default template at {template_path}")
    
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
            "metadata": analysis_results.get("metadata", {}),
            "results": analysis_results.get("results", [])
        }
        
        # Add statistics
        template_data["stats"] = self._calculate_analysis_stats(analysis_results)
        
        # Try to get the template
        try:
            template = self.jinja_env.get_template("ai_analysis_template.html")
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            # If template can't be loaded, use a basic inline template
            template_str = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <p>Generated: {{ timestamp }}</p>
                    <p>Model: {{ metadata.provider }} / {{ metadata.model }}</p>
                    <h2>Analysis Summary</h2>
                    <p>Total Failures: {{ stats.total }}</p>
                    <p>True Bugs: {{ stats.true_bugs }}</p>
                    <p>False Positives: {{ stats.false_positives }}</p>
                </div>
            </body>
            </html>
            """
            template = self.jinja_env.from_string(template_str)
        
        # Render template
        try:
            report_html = template.render(**template_data)
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            # Fallback to very basic HTML
            report_html = f"""
            <html>
            <body>
                <h1>{template_data['title']}</h1>
                <p>Generated: {template_data['timestamp']}</p>
                <p>Error rendering full report: {str(e)}</p>
            </body>
            </html>
            """
        
        # Write to file
        try:
            # Ensure directory exists
            report_path.parent.mkdir(exist_ok=True, parents=True)
            
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_html)
        except Exception as e:
            logger.error(f"Error writing report to {report_path}: {e}")
            # Try writing to a different location if possible
            fallback_path = Path(os.getcwd()) / report_name
            with open(fallback_path, "w", encoding="utf-8") as f:
                f.write(report_html)
            logger.info(f"Wrote report to fallback location: {fallback_path}")
            return str(fallback_path)
        
        logger.info(f"AI analysis report generated: {report_path}")
        
        return str(report_path)
    
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