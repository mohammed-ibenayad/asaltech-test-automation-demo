# ASAL Tech Automation Framework

## 🚀 Comprehensive Test Automation Solution

### Overview

The ASAL Tech Automation Framework is a robust, scalable, and intelligent test automation platform designed to streamline and enhance your software testing processes. Built with flexibility and intelligence in mind, this framework supports web, mobile, and API testing with cutting-edge AI-powered analysis capabilities.

### 🌟 Key Features

#### Comprehensive Testing Support
- **Web Testing**: Selenium-based testing with advanced Page Object Model
- **Mobile Testing**: Appium-powered testing for Android and iOS
- **API Testing**: Comprehensive RESTful API testing capabilities
- **Cross-Browser Support**: Chrome, Firefox, Edge, Safari, and more

#### AI-Powered Intelligent Analysis
- Automated failure categorization
- Intelligent bug detection
- Root cause analysis
- Confidence scoring for test failures
- Automated suggested fixes

#### Framework Advantages
- Modular and extensible architecture
- Easy integration with CI/CD pipelines
- Configurable across different environments
- Detailed HTML and AI-powered reporting

### 🛠 Prerequisites

- Python 3.8+
- pip
- Virtual environment support

### 📦 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/your-org/automation-framework.git
cd automation-framework
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

### 🧪 Running Tests

#### Web Testing
```bash
# Run all web tests
pytest examples/web_the_internet/tests/

# Run specific test
pytest examples/web_the_internet/tests/test_login.py

# Run with specific browser
pytest --browser=chrome
pytest --browser=firefox

# Run in headless mode
pytest --headless
```

#### Mobile Testing
```bash
# Run mobile tests
pytest examples/mobile_example/tests/

# Specify device/platform
pytest --device=android --platform=11
```

#### API Testing
```bash
# Run API tests
pytest examples/api_example/tests/
```

### 🤖 AI-Powered Analysis

Enable AI-powered failure analysis with the `--analyze-failures` flag:

```bash
pytest --analyze-failures
```

This generates:
- Detailed JSON analysis
- Interactive HTML report with:
  - Failure categorization
  - Confidence scoring
  - Suggested fixes
  - Visualizations

### 🔧 Configuration

#### Environment Configuration
Configuration files are located in `automation_framework/config/`:
- `dev.yaml`: Development environment settings
- `staging.yaml`: Staging environment settings
- `prod.yaml`: Production environment settings

#### AI Analysis Configuration
Configure AI providers in `.env`:
```
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key
```

### 📊 Reporting

The framework generates multiple report types:
- Console output
- HTML reports
- AI-powered analysis reports
- Detailed logs

### 🔍 Project Structure
```
automation-framework/
│
├── automation_framework/      # Core framework
│   ├── src/
│   │   ├── web/               # Web testing components
│   │   ├── mobile/            # Mobile testing components
│   │   ├── api/               # API testing components
│   │   └── ai_module/         # AI analysis capabilities
│   │
│   └── config/                # Configuration files
│
├── examples/                  # Example test implementations
│   ├── web_example/
│   ├── mobile_example/
│   └── api_example/
│
├── docs/                      # Documentation
└── reports/                   # Test reports
```

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📋 Best Practices

1. Always use Page Object Model for web tests
2. Implement explicit waits
3. Keep tests independent
4. Use meaningful test and method names
5. Leverage AI analysis for continuous improvement

### 🔒 License

Distributed under the MIT License. See `LICENSE` for more information.

### 📞 Contact

ASAL Tech - `info@asaltech.com`

Project Link: `https://github.com/your-org/automation-framework`

---

**🌈 Happy Automated Testing!**