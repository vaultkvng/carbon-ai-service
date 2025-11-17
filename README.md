# 🧠 Carbon Footprint AI Service (Microservice)

## 📌 Overview
This is the intelligence layer for the **Group 1 Carbon Footprint Tracker**. 
It is a standalone microservice built with **Python (FastAPI)** that accepts user logs from the main Backend (Spring Boot/PostgreSQL) and returns real-time recommendations.

## ⚙️ Installation & Setup
1. **Install Dependencies:** `pip install -r requirements.txt`
2. **Run Server:** `uvicorn main:app --reload`
3. **View Docs:** `http://localhost:8000/docs`

---

## 🔌 API Integration Guide (Java/Spring Boot Friendly)

**Base URL:** `http://localhost:8000`
**Content-Type:** `application/json`

### 1. Food Recommendation
**Endpoint:** `POST /api/v1/recommend/food`

**Request Body (Java DTO):**
| Field | Type | Description | Valid Options |
| :--- | :--- | :--- | :--- |
| `user_id` | `String` | Unique ID | Any string |
| `meal_type` | `String` | Time of day | "lunch", "dinner" |
| `main_ingredient` | `String` | Primary item | "beef", "chicken", "vegetables" |
| `portion_size` | `String` | Meal size | "small", "medium", "large" |
| `side_dish` | `String` | (Optional) | Any string |

### 2. Transport Recommendation
**Endpoint:** `POST /api/v1/recommend/transport`

**Request Body (Java DTO):**
| Field | Type | Description | Valid Options |
| :--- | :--- | :--- | :--- |
| `user_id` | `String` | Unique ID | Any string |
| `transport_mode` | `String` | Mode | "car", "bus", "bicycle", "walking" |
| `distance_km` | `Float` | Distance | Any number (e.g., 2.5) |
| `carpool` | `Boolean` | Shared ride? | `true`, `false` |

### 3. Energy Recommendation (Nigeria Context)
**Endpoint:** `POST /api/v1/recommend/energy`

**Request Body (Java DTO):**
| Field | Type | Description | Valid Options |
| :--- | :--- | :--- | :--- |
| `user_id` | `String` | Unique ID | Any string |
| `appliance_type` | `String` | Device | "ac", "heater", "tv", "laptop" |
| `hours_used` | `Float` | Duration | Any number (e.g., 5.0) |
| `energy_source` | `String` | Power source | "grid", "generator" |

---

### 📤 The Response (Standard Output)
All endpoints return this structure:

```json
{
  "title": "String",
  "message": "String",
  "action_type": "String (substitution | praise | warning)",
  "severity": "String (high | medium | low)",
  "estimated_savings_co2_kg": "Float"
}