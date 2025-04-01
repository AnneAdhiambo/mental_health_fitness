# Setting Up the Project Environment

This guide provides step-by-step instructions to set up a Python virtual environment and install the necessary dependencies listed in `requirements.txt`.

## Prerequisites

- **Python 3.x**: Ensure Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

- **pip**: This package installer for Python typically comes with Python. Verify its installation by running:

  
```bash
  python -m pip --version
  ```


## Steps to Set Up the Environment

1. **Navigate to Your Project Directory**

   Open your terminal or command prompt and move to your project's root directory:

   ```bash
   cd /path/to/your/project
   ```


2. **Create a Virtual Environment**

   Set up a virtual environment named `.venv` within your project directory:

   ```bash
   python -m venv .venv
   ```


3. **Activate the Virtual Environment**

   - **On macOS/Linux:**

     ```bash
     source .venv/bin/activate
     ```

   - **On Windows (Command Prompt):**

     ```bash
     .venv\Scripts\activate.bat
     ```

   - **On Windows (PowerShell):**

     ```powershell
     .venv\Scripts\Activate.ps1
     ```

   Upon activation, your terminal prompt may display the name of the virtual environment, indicating that it's active.

4. **Install Dependencies from `requirements.txt`**

   With the virtual environment activated, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```


   This command reads the `requirements.txt` file and installs all listed packages into your virtual environment.

5. **Deactivate the Virtual Environment (When Done)**

   After completing your work, deactivate the virtual environment to return to the global Python environment:

   ```bash
   deactivate
   ```


## Additional Notes

- **Virtual Environment Location:** It's common practice to create the virtual environment within your project directory and name it `.venv`. This setup keeps your project organized and ensures the environment is easily identifiable.

- **Excluding `.venv` from Version Control:** To prevent the virtual environment from being tracked by version control systems like Git, add `.venv/` to your `.gitignore` file.

- **Ensuring Consistency Across Environments:** Regularly update your `requirements.txt` by running `pip freeze > requirements.txt` after adding new packages. This practice ensures that all environments have consistent dependencies.

