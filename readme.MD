#  Project Overview

The objective is to develop a Web application that allows users to search for scientific articles based on a list of keywords.

### User Features:

- **Search** in titles, keywords, authors, and full text for articles matching user-specified terms.
- **Filter** search results by:
  - Keywords
  - Authors
  - Institutions
  - Publication date range
- **View** details of each article, including:
  - Full text (as text and PDF)
  - Bibliographic references
- **Save favorite articles** for future reading.

### Admin Features:

- **Manage moderators** (add, edit, delete).
- **Upload PDFs** from a URL:
  - Extract text from PDFs (one or two-column layouts supported).
  - Analyze extracted text to obtain article metadata.
  - Index data into **Elasticsearch** for efficient searching.
- **Review and correct** extracted data if necessary.

---
# Backend

**Backend repository for the project**

##  Specifications

- Developed with **FastAPI** (Python framework).
- Using a virtual environment is highly recommended; [Miniconda] is suggested for this project.

##  Running the Application

1. **Create a virtual environment**:
   ```bash
   conda create -n "env_name" python=3.11
   ```
2. **Activate the environment**:
   ```bash
   conda activate "env_name"
   ```
3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the application**:
   ```bash
   python main.py
   ```

##  Code Conventions

- If you install a new package:
  ```bash
  pip install <package-name>
  ```
  Before committing and pushing, make sure to update the `requirements.txt` file:
  ```bash
  pip freeze > requirements.txt
  ```

- **Database Access**:
  - All database operations must use **SQLAlchemy** for clean code and security.

- **Working with Git**:
  - Create a feature branch before implementing anything:
    ```bash
    git checkout -b "firstname/feature-name"
    ```
  - Push your branch after your changes:
    ```bash
    git push origin "firstname/feature-name"
    ```

##  Project Folder Structure

- `models/` — Database models/entities.
- `controllers/` — Business logic.
- `routes/` — API route definitions.
- `validators/` — Classes used for validating request data.
- `utils/` — Utility functions and credentials management.
- `tests/` — Unit tests.

[Miniconda]: https://docs.conda.io/projects/miniconda/en/latest/
