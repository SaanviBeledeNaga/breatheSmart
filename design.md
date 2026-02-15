# breatheSmart - System Design Document

## 1. System Architecture

### 1.1 Architecture Overview

breatheSmart follows a **three-tier web application architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  index.html  │  │ carbon.html  │  │   style.css  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                          │                                   │
│                   ┌──────────────┐                          │
│                   │  script.js   │                          │
│                   └──────────────┘                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/JSON
┌─────────────────────────┴───────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                   ┌──────────────┐                          │
│                   │   Flask App  │                          │
│                   │   (app.py)   │                          │
│                   └──────┬───────┘                          │
│                          │                                   │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐          │
│    │  AQI ML  │    │  Carbon  │    │ Carbon AI│          │
│    │  Module  │    │  Module  │    │  Module  │          │
│    └────┬─────┘    └────┬─────┘    └────┬─────┘          │
└─────────┼───────────────┼───────────────┼─────────────────┘
          │               │               │
┌─────────┴───────────────┴───────────────┴─────────────────┐
│                      DATA LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ aqi_data.csv │  │aqi_model.pkl │  │  Emission    │    │
│  │              │  │              │  │  Factors     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Pattern

- **Pattern**: Model-View-Controller (MVC) variant
- **Frontend**: Static HTML/CSS/JavaScript (View)
- **Backend**: Flask REST API (Controller)
- **Business Logic**: Python modules (Model)
- **Data Storage**: CSV files and serialized ML models

### 1.3 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Vercel Platform                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Serverless Functions                  │  │
│  │         (Python Runtime - app.py)                 │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Static File CDN                       │  │
│  │         (HTML, CSS, JS, Models, Data)             │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS
                          ▼
                   ┌──────────────┐
                   │   End Users  │
                   └──────────────┘
```

---

## 2. Components

### 2.1 Frontend Components

#### 2.1.1 HTML Templates
- **index.html**: AQI prediction interface
  - City selector dropdown (Delhi, Mumbai, Chennai, Kolkata, Bangalore)
  - Prediction trigger button
  - Results display area
  - Navigation to carbon calculator

- **carbon.html**: Carbon footprint calculator interface
  - Distance input field
  - Transport mode selector (Car, Bus, Train, Bike)
  - Calculate button
  - Results and recommendations display
  - Navigation back to AQI predictor

#### 2.1.2 JavaScript Module (script.js)
- **predictAQI()**: Fetches AQI prediction from backend
  - Makes GET request to `/predict-aqi` endpoint
  - Updates UI with predicted AQI and classification
  - Handles errors gracefully

- **calculateCarbon()**: Calculates carbon footprint
  - Makes POST request to `/carbon` endpoint
  - Sends distance and transport mode as JSON
  - Displays emissions and AI recommendations
  - Error handling and validation

#### 2.1.3 Styling (style.css)
- Responsive design for mobile and desktop
- Hero section with gradient backgrounds
- Card-based UI components
- Consistent color scheme and typography

### 2.2 Backend Components

#### 2.2.1 Flask Application (app.py)
Main application controller with route handlers:

- **Route: `/`** (GET)
  - Serves home page (index.html)
  - Entry point for AQI prediction feature

- **Route: `/predict-aqi`** (GET)
  - Query parameter: `city` (default: "Delhi")
  - Returns: JSON with predicted AQI and classification
  - Integrates AQI ML module

- **Route: `/carbon`** (GET)
  - Serves carbon calculator page (carbon.html)

- **Route: `/carbon`** (POST)
  - Request body: `{distance, mode}`
  - Returns: JSON with emissions and suggestions
  - Integrates carbon calculation and AI recommendation modules

#### 2.2.2 AQI ML Module (`aqi_ml/`)

**predictor.py**
- `predict_tomorrow_aqi(city)`: Core prediction function
  - Loads pre-trained scikit-learn model
  - Reads historical data from CSV
  - Extracts last 7 days of pollutant data
  - Computes mean features (PM2.5, PM10, NO2, SO2)
  - Returns predicted AQI value
  - Fallback: Returns 100 if city not found

**aqi_utils.py**
- `classify_aqi(aqi)`: Classification function
  - Good: ≤50
  - Moderate: 51-100
  - Poor: 101-200
  - Severe: >200

**train_model.py**
- Model training script (offline process)
- Generates `aqi_model.pkl`

**preprocess.py**
- Data preprocessing utilities
- Feature engineering for ML model

#### 2.2.3 Carbon Module (`carbon/`)

**calculator.py**
- `calculate_total_emission(distance, mode)`: Main calculation function
  - Delegates to transport module
  - Returns structured emission data
  - Rounds to 2 decimal places

**transport.py**
- `calculate_transport_emission(distance_km, mode)`: Transport-specific calculation
  - Formula: `distance × emission_factor`
  - Uses emission factors from constants

**emission_factors.py**
- Emission constants (kg CO2 per km):
  - Car: 0.192
  - Bus: 0.082
  - Train: 0.041
  - Bike: 0.103
- Electricity factor: 0.82 kg CO2/kWh (for future use)

#### 2.2.4 Carbon AI Module (`carbon_ai/`)

**recommender.py**
- `recommend_actions(emissions, aqi_level)`: AI recommendation engine
  - Rule-based recommendation system
  - Emission-based suggestions:
    - High (>20 kg): Public transport/carpooling
    - Medium (5-20 kg): Reduce trips
    - Low (<5 kg): Positive reinforcement
  - AQI-based health advisories:
    - Poor/Severe: Outdoor activity warnings, mask recommendations, remote work suggestions

### 2.3 Data Components

#### 2.3.1 AQI Dataset (`data/aqi_data.csv`)
Structure:
```
city, pm25, pm10, no2, so2, date
```
- Historical pollutant measurements
- Multiple cities (Delhi, Mumbai, Chennai, Kolkata, Bangalore)
- Time-series data for trend analysis

#### 2.3.2 ML Model (`model/aqi_model.pkl`)
- Serialized scikit-learn model
- Trained on historical AQI data
- Input features: PM2.5, PM10, NO2, SO2 (averaged over 7 days)
- Output: Predicted AQI value

---

## 3. Data Flow

### 3.1 AQI Prediction Flow

```
User Action (Select City + Click Predict)
    │
    ▼
JavaScript: predictAQI()
    │
    ▼
GET /predict-aqi?city=Delhi
    │
    ▼
Flask Route Handler
    │
    ▼
predict_tomorrow_aqi(city)
    │
    ├─► Load aqi_data.csv
    │   └─► Filter by city
    │       └─► Get last 7 days
    │           └─► Calculate mean pollutants
    │
    ├─► Load aqi_model.pkl
    │   └─► model.predict(features)
    │
    ▼
classify_aqi(predicted_value)
    │
    ▼
JSON Response: {predicted_aqi, aqi_level}
    │
    ▼
JavaScript: Update DOM
    │
    ▼
Display Result to User
```

### 3.2 Carbon Calculation Flow

```
User Action (Enter Distance + Select Mode + Click Calculate)
    │
    ▼
JavaScript: calculateCarbon()
    │
    ▼
POST /carbon
Body: {distance: 50, mode: "car"}
    │
    ▼
Flask Route Handler
    │
    ├─► calculate_total_emission(distance, mode)
    │   │
    │   └─► calculate_transport_emission(distance, mode)
    │       │
    │       └─► distance × TRANSPORT_EMISSIONS[mode]
    │
    ├─► predict_tomorrow_aqi("Delhi")
    │   └─► Get AQI context
    │
    ├─► classify_aqi(predicted_aqi)
    │
    ▼
recommend_actions(emissions, aqi_level)
    │
    ├─► Analyze emission level
    ├─► Check AQI conditions
    └─► Generate suggestions
    │
    ▼
JSON Response: {emissions, suggestions}
    │
    ▼
JavaScript: Update DOM
    │
    ├─► Display total emissions
    └─► Render suggestion list
    │
    ▼
Display Results to User
```

### 3.3 Data Dependencies

```
┌─────────────────┐
│  aqi_data.csv   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  train_model.py │─────►│ aqi_model.pkl   │
└─────────────────┘      └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  predictor.py   │
                         └─────────────────┘
```

---

## 4. Tech Stack

### 4.1 Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.x | Core programming language |
| Flask | Latest | Web framework and REST API |
| Pandas | Latest | Data manipulation and CSV processing |
| NumPy | Latest | Numerical computations |
| scikit-learn | Latest | Machine learning model training and inference |
| joblib | Latest | Model serialization/deserialization |

### 4.2 Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Page structure and semantics |
| CSS3 | - | Styling and responsive design |
| JavaScript (ES6+) | - | Client-side interactivity and API calls |
| Fetch API | - | Asynchronous HTTP requests |

### 4.3 Development & Deployment

| Technology | Purpose |
|------------|---------|
| Vercel | Serverless deployment platform |
| Git | Version control |
| vercel.json | Deployment configuration |

### 4.4 Data Formats

- **CSV**: Historical AQI data storage
- **JSON**: API request/response format
- **PKL**: Serialized ML model format

---

## 5. High-Level Design

### 5.1 Design Principles

1. **Separation of Concerns**
   - Clear module boundaries (AQI, Carbon, AI)
   - Independent, reusable components

2. **Modularity**
   - Each module has single responsibility
   - Easy to extend with new features

3. **Stateless Architecture**
   - No session management required
   - Each request is independent

4. **Fail-Safe Design**
   - Fallback values for missing data
   - Graceful error handling

5. **Performance Optimization**
   - Pre-trained models loaded at startup
   - Minimal computation per request
   - Efficient data access patterns

### 5.2 API Design

#### REST API Endpoints

**GET /predict-aqi**
```
Request:
  Query Params: city (string, optional, default="Delhi")

Response:
  {
    "predicted_aqi": 125.5,
    "aqi_level": "Poor"
  }

Status Codes:
  200: Success
  500: Server error
```

**POST /carbon**
```
Request:
  Headers: Content-Type: application/json
  Body: {
    "distance": 50,
    "mode": "car"
  }

Response:
  {
    "emissions": {
      "transport": 9.6,
      "total": 9.6
    },
    "suggestions": [
      "Try reducing unnecessary vehicle trips.",
      "Avoid outdoor activities and use masks if necessary."
    ]
  }

Status Codes:
  200: Success
  400: Invalid input
  500: Server error
```

### 5.3 Machine Learning Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                   OFFLINE TRAINING                       │
│                                                          │
│  Raw Data → Preprocessing → Feature Engineering →       │
│  Model Training → Validation → Serialization            │
│                                                          │
│  Output: aqi_model.pkl                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   ONLINE INFERENCE                       │
│                                                          │
│  Load Model → Extract Features → Predict → Classify     │
│                                                          │
│  Latency: <2 seconds                                    │
└─────────────────────────────────────────────────────────┘
```

### 5.4 Module Interaction Diagram

```
┌──────────────┐
│   app.py     │
│  (Flask App) │
└──────┬───────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
       ▼                                     ▼
┌──────────────┐                    ┌──────────────┐
│   aqi_ml/    │                    │   carbon/    │
│              │                    │              │
│ ┌──────────┐ │                    │ ┌──────────┐ │
│ │predictor │ │                    │ │calculator│ │
│ └────┬─────┘ │                    │ └────┬─────┘ │
│      │       │                    │      │       │
│ ┌────▼─────┐ │                    │ ┌────▼─────┐ │
│ │aqi_utils │ │                    │ │transport │ │
│ └──────────┘ │                    │ └────┬─────┘ │
│              │                    │      │       │
│              │                    │ ┌────▼─────┐ │
│              │                    │ │emission_ │ │
│              │                    │ │factors   │ │
│              │                    │ └──────────┘ │
└──────────────┘                    └──────────────┘
       │                                     │
       │                                     │
       └──────────────┬──────────────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  carbon_ai/  │
              │              │
              │ ┌──────────┐ │
              │ │recommend │ │
              │ │   er     │ │
              │ └──────────┘ │
              └──────────────┘
```

### 5.5 Security Considerations

1. **Input Validation**
   - City names normalized to lowercase
   - Distance values validated as numbers
   - Transport mode restricted to predefined options

2. **Error Handling**
   - Try-catch blocks in JavaScript
   - Fallback values in Python
   - No sensitive data exposure in errors

3. **Data Privacy**
   - No user data stored
   - No authentication required
   - Stateless requests

4. **API Security**
   - CORS handled by Flask
   - JSON content-type validation
   - No SQL injection risk (CSV-based)

### 5.6 Scalability Considerations

1. **Horizontal Scaling**
   - Stateless design enables multiple instances
   - Vercel serverless functions auto-scale

2. **Caching Opportunities**
   - Model loaded once per instance
   - CSV data cached in memory
   - Static assets served via CDN

3. **Performance Bottlenecks**
   - CSV file size (mitigated by filtering)
   - Model inference time (optimized with scikit-learn)
   - Network latency (mitigated by CDN)

### 5.7 Future Architecture Enhancements

1. **Database Integration**
   - Replace CSV with PostgreSQL/MongoDB
   - Enable real-time data updates

2. **Caching Layer**
   - Redis for frequently accessed predictions
   - Reduce computation overhead

3. **Microservices**
   - Separate AQI and Carbon services
   - Independent scaling and deployment

4. **Real-time Data**
   - Integration with live AQI APIs
   - WebSocket for live updates

5. **Authentication**
   - User accounts and profiles
   - Personalized tracking and history

---

**Document Version**: 1.0  
**Last Updated**: February 15, 2026  
**Project**: breatheSmart
