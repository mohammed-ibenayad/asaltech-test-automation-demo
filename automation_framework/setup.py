# automation_framework/setup.py
setup(
    # existing setup code
    entry_points={
        'pytest11': [
            'ai_analysis = automation_framework.src.ai_module.pytest_plugin',
        ],
    },
)