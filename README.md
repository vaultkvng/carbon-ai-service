# 🧠 Carbon Footprint AI Service (Microservice)

## 📌 Overview
This is the intelligence layer for the **Group 1 Carbon Footprint Tracker**. 
It is a standalone microservice built with **Python (FastAPI)** that accepts user logs from the main Backend (Node.js/PostgreSQL) and returns real-time, personalized recommendations to reduce carbon emissions.

**Key Features:**
* **Rules-Based Recommendation Engine:** Logic trees for Food, Transport, and Energy.
* **Localized Context:** Specific logic for Nigerian energy scenarios (Grid vs. Generator).
* **FastAPI:** High-performance, asynchronous API handling.

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.9+
* pip (Python Package Manager)

### 1. Clone and Install Dependencies
```bash
# Install the required libraries
pip install fastapi uvicorn pydantic