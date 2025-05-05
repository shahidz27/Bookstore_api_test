📘 Bookstore API Testing Project

🔧 Tools & Technologies:

Flask: Used for developing the Bookstore API, implementing key endpoints (GET, POST, RESET) for managing books.
Pytest – Used for writing and executing test cases for the Bookstore API.
Fixtures – Set up reusable test components (e.g., Flask test client, sample book data).
Parameterization – Run tests with multiple input datasets to ensure API reliability.
Jenkins – Automates test setup, execution, and result reporting.
CI/CD Pipeline – Includes stages for checkout, environment setup, server start, health check, test execution, and cleanup.

⚙️ Key Pipeline Stages

Checkout – Pulls latest code from GitHub.
Setup Environment – Creates virtual environment and installs all dependencies.
Start Server – Launches the Flask API in the background.
Run Tests – Executes all Pytest cases with fixture and parameterized data.
Stop Server – Cleans up by terminating the Flask server.
Post Steps – Publishes test reports and cleans workspace.

✅ Automation Highlights

Virtualenv creation and package installation
Flask server boot and validation
Test execution triggered automatically
Health checks to avoid test failures on down server
JUnit XML reporting for Jenkins integration
