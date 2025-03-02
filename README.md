# ASAL Tech - Test Automation Framework

A comprehensive test automation framework supporting Web, Mobile, and API testing with AI-powered analysis capabilities. This framework demonstrates a strategic approach to test automation with a focus on sustainable, maintainable, and scalable solutions.

## Project Structure

```
test-automation-demo/
├── automation-framework/     # Core automation framework
│   ├── src/                  # Framework source code
│   │   ├── core/             # Shared core functionality
│   │   ├── web/              # Web testing components
│   │   ├── mobile/           # Mobile testing components
│   │   ├── api/              # API testing components
│   │   ├── ai_module/        # AI analysis capabilities
│   │   └── reporters/        # Reporting functionality
│   ├── tests/                # Framework test suite
│   └── config/               # Configuration files
│
├── demo-app/                 # Demo applications for testing
│   ├── web-app/              # Demo web application
│   ├── mobile-app/           # Demo mobile application
│   └── api/                  # Demo API service
│
├── docs/                     # Documentation
│   ├── strategy/             # Test Automation Strategy (Milestone 1)
│   ├── framework/            # Framework Documentation (Milestone 2)
│   └── ai-analysis/          # AI Analysis Documentation
│
├── examples/                 # Complete example implementations
│   ├── web_example/          # Web testing example
│   ├── mobile_example/       # Mobile testing example
│   └── api_example/          # API testing example
│
└── demo-results/             # Sample test results and reports
```

## Key Components

### 1. Test Automation Strategy (Milestone 1)

Our approach begins with strategy, not just scripts. The `docs/strategy/` directory contains:
- Strategic approach documentation
- Test prioritization guidelines
- ROI calculation templates
- Milestone 1 deliverables

### 2. Test Automation Framework (Milestone 2)

A production-ready framework supporting:
- **Web Testing**: Selenium-based web testing with Page Object Model
- **Mobile Testing**: Appium-based mobile testing for Android and iOS
- **API Testing**: RESTful API testing with request/response validation

### 3. AI-Powered Test Analysis

Intelligent analysis capabilities:
- Failure pattern recognition
- False positive detection
- Smart test result classification
- Test optimization recommendations

## Usage Examples

Each testing type includes complete examples:

### Web Testing

```python
# Example from examples/web_example/tests/test_login.py
def test_valid_login(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("valid_user", "valid_password")
    assert login_page.is_logged_in()
```

### Mobile Testing

```python
# Example from examples/mobile_example/tests/test_login.py
def test_valid_login(app_driver):
    login_screen = LoginScreen(app_driver)
    login_screen.enter_credentials("valid_user", "valid_password")
    login_screen.tap_login_button()
    assert login_screen.is_logged_in()
```

### API Testing

```python
# Example from examples/api_example/tests/test_auth.py
def test_valid_login_api():
    auth_service = AuthService()
    response = auth_service.login("valid_user", "valid_password")
    assert response.status_code == 200
    assert "token" in response.json()
```

## Getting Started

1. Clone this repository
2. Run the setup script: `./scripts/setup.sh`
3. Explore the examples: `./scripts/run_demo.sh`
4. Read the documentation in the `docs/` directory

## Framework Features

- **Cross-platform core**: Shared interfaces with platform-specific implementations
- **Modular design**: Mix and match components based on your needs
- **Reporting**: Comprehensive HTML reports with dashboards
- **CI/CD integration**: GitHub Actions workflows included
- **AI-powered analysis**: Intelligent test result classification

## License

This project is licensed under the terms of the LICENSE file included in this repository.