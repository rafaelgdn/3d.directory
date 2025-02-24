# Printing Directory

This project uses Poetry for dependency management and virtual environment handling.

## Installing Poetry

1. Install Poetry by following the official instructions:
   https://python-poetry.org/docs/#installation

   For Windows users, you can use PowerShell:
   ```
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

   For macOS / Linux users:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Verify the installation by running:
   ```
   poetry --version
   ```

## Project Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/printing-directory.git
   cd printing-directory
   ```

2. Install project dependencies:
   ```
   poetry install
   ```

## Running the Project

To run the main.py file, use the following command:

```
poetry run python -m printing_directory.main 
```

This command will activate the virtual environment created by Poetry and run the main.py script with all necessary dependencies.

## Running the Project Using requirements.txt

If you prefer not to use Poetry, you can set up and run the project using a traditional requirements.txt file:

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the main.py file:
   ```
   python printing_directory/main.py
   ```

Remember to deactivate the virtual environment when you're done:
```
deactivate
```