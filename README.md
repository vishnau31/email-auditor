# Email Audit Service

A comprehensive email quality assessment service that analyzes .eml files using dynamic rules to evaluate email effectiveness and professionalism.

## Features

- **EML File Parsing**: Robust parsing of .eml email files with support for headers, content, and attachments
- **Dynamic Rule System**: Pluggable rule architecture for customizable email quality checks
- **Comprehensive Auditing**: Multi-rule analysis with detailed scoring and recommendations
- **RESTful API**: Clean FastAPI-based interface for easy integration
- **JSON Reporting**: Structured audit reports with actionable insights
- **Containerized**: Ready-to-deploy Docker container

## Architecture

The service follows a modular architecture:

```
app/
├── api/          # FastAPI endpoints
├── audit/        # Core audit engine and reporting
├── models/       # Pydantic data models
├── parser/       # EML file parsing logic
└── rules/        # Dynamic rule system
```

## Installation

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker
- Docker Compose

#### Quick Start with Docker

1. Run with Docker Compose:
```bash
docker-compose up
```

2. The service will be available at `http://localhost:8000`


## API Usage

### Audit an Email

```bash
curl -X POST "http://localhost:8000/api/v1/audit" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_email.eml"
```

### Example Response

```json
{
  "audit_timestamp": "2025-06-19T13:00:41.643578",
  "overall_score": 1.0,
  "summary": "Email quality is excellent. 3/3 rules passed (100.0%).",
  "recommendations": [
    "Great job! Your email meets all quality standards."
  ],
  "rule_results": [
    {
      "rule_name": "AttachmentRule",
      "status": "pass",
      "score": 1.0,
      "justification": "At least one image attachment found"
    },
    {
      "rule_name": "LengthRule",
      "status": "pass",
      "score": 1.0,
      "justification": "Email length is appropriate (563 characters)"
    },
    {
      "rule_name": "GreetingRule",
      "status": "pass",
      "score": 1.0,
      "justification": "Email contains appropriate greeting"
    }
  ],
  "statistics": {
    "total_rules": 3,
    "passed_rules": 3,
    "failed_rules": 0,
    "pass_rate": 1.0
  }
}
```

## Available Rules

### GreetingRule
Checks for appropriate email greetings (Dear, Hello, Hi, etc.)

### AttachmentRule
Verifies presence of image attachments for visual content

### LengthRule
Ensures email content is neither too short nor too long

## Development

### Project Structure

- **EML Parser**: Handles .eml file parsing with support for multipart MIME
- **Rule Registry**: Dynamic rule discovery and management system
- **Audit Engine**: Orchestrates rule execution and scoring
- **Report Generator**: Creates structured audit reports

### Adding New Rules

1. Create a new rule class in `app/rules/`
2. Inherit from `BaseRule`
3. Implement the `evaluate` method
4. The rule will be automatically discovered and loaded

Example:
```python
from app.rules.base import BaseRule
from app.models import EmailMessage

class CustomRule(BaseRule):
    name = "CustomRule"
    description = "Custom email quality check"
    
    def evaluate(self, email: EmailMessage) -> RuleResult:
        # Your rule logic here
        pass
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## License

MIT License - see LICENSE file for details.

## Author

Vishesh Nautiyal

---

For questions or contributions, please open an issue or submit a pull request.