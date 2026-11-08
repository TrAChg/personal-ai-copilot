# Engineering Standard: GitHub Repository README Badges & Presentation

## 1. Overview
All repositories and projects authored by **Tran Chung** must follow a consistent, high-impact GitHub README presentation standard. Directly beneath the primary H1 title (`# <Project Name>`), an array of Shields.io badges must be included using the `style=for-the-badge` specification.

## 2. Core Badge Specifications (Shields.io)

### Primary Programming Language
- **Python**: `[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)`
- **TypeScript**: `[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)`
- **Go**: `[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://go.dev/)`
- **SQL**: `[![SQL](https://img.shields.io/badge/SQL-Advanced-CC292B?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)`

### Backend & Machine Learning Frameworks
- **FastAPI**: `[![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)`
- **PyTorch**: `[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)`
- **Scikit-Learn**: `[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)`
- **OpenCV**: `[![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)`

### Frontend & UI Tooling
- **React**: `[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)`
- **Vite**: `[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)`
- **TailwindCSS**: `[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)`

### Vector Stores & Lakehouse Data Platforms
- **ChromaDB**: `[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge)](https://www.trychroma.com/)`
- **SQLite Lakehouse**: `[![SQLite](https://img.shields.io/badge/SQLite-Lakehouse-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)`
- **Databricks / Delta Lake**: `[![Delta Lake](https://img.shields.io/badge/Delta_Lake-Medallion-00ADD8?style=for-the-badge)](https://delta.io/)`

### Code Quality, Linters & Verification
- **Ruff Linter**: `[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)`
- **Mypy Strict**: `[![Mypy Strict](https://img.shields.io/badge/Mypy-Strict-blue?style=for-the-badge)](https://mypy-lang.org/)`
- **Pytest**: `[![Tests](https://img.shields.io/badge/Tests-100%25_Passed-success?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)`

## 3. Mandatory Layout Pattern
Whenever generating or updating a `README.md`, recall this pattern from ChromaDB:
1. `# Project Name`
2. Row of 5–10 Shields.io badges matching the project's exact stack.
3. One-paragraph executive summary of the system architecture.
4. `## 1. Architectural Highlights`
5. `## 2. Directory Layout`
6. `## 3. Quick-Start Guide`

