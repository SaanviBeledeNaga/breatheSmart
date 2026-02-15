# breatheSmart - Requirements Document

## 1. Project Overview

breatheSmart is a web-based environmental awareness platform that combines air quality monitoring with carbon footprint tracking. The application provides users with predictive AQI (Air Quality Index) forecasts and personalized carbon emission calculations based on transportation choices, along with AI-driven recommendations for reducing environmental impact.

### Key Features
- Tomorrow's AQI prediction for Indian cities using machine learning
- Carbon footprint calculator for transportation modes
- Intelligent recommendations based on AQI levels and emission data
- Real-time web interface for user interaction

### Target Users
- Urban residents concerned about air quality
- Environmentally conscious individuals tracking their carbon footprint
- Commuters seeking sustainable transportation alternatives

---

## 2. Functional Requirements

### 2.1 Air Quality Index (AQI) Prediction

**FR-1.1**: The system shall predict tomorrow's AQI for a specified city
- Input: City name (default: Delhi)
- Output: Predicted AQI value and classification level

**FR-1.2**: The system shall classify AQI values into standard categories
- Good, Moderate, Poor, Severe, etc.
- Based on standard AQI classification thresholds

**FR-1.3**: The system shall use historical pollutant data for predictions
- PM2.5, PM10, NO2, SO2 levels
- Last 7 days of data as input features

**FR-1.4**: The system shall provide fallback AQI values when city data is unavailable
- Default safe value: 100 (Moderate)

### 2.2 Carbon Footprint Calculator

**FR-2.1**: The system shall calculate carbon emissions for transportation
- Input: Distance traveled and mode of transport
- Output: CO2 emissions in kg

**FR-2.2**: The system shall support multiple transportation modes
- Car, bike, public transport, walking, etc.
- Each mode with specific emission factors

**FR-2.3**: The system shall provide total emission breakdown
- Transport emissions
- Total carbon footprint

### 2.3 AI-Driven Recommendations

**FR-3.1**: The system shall generate personalized action recommendations
- Based on calculated emission levels
- Contextual to current AQI conditions

**FR-3.2**: The system shall provide tiered suggestions based on emission thresholds
- High emissions (>20 kg CO2): Strong alternatives suggested
- Medium emissions (5-20 kg CO2): Moderate reduction tips
- Low emissions (<5 kg CO2): Positive reinforcement

**FR-3.3**: The system shall provide health advisories during poor air quality
- Outdoor activity warnings
- Protective measure recommendations
- Alternative work arrangement suggestions

### 2.4 Web Interface

**FR-4.1**: The system shall provide a home page for AQI predictions
- City selection interface
- Display predicted AQI and classification

**FR-4.2**: The system shall provide a dedicated carbon calculator page
- Input form for distance and transport mode
- Display emission results and recommendations

**FR-4.3**: The system shall use RESTful API endpoints
- `/predict-aqi` for AQI predictions (GET)
- `/carbon` for emission calculations (POST)

**FR-4.4**: The system shall return data in JSON format
- Structured response objects
- Error handling for invalid inputs

---

## 3. Non-Functional Requirements

### 3.1 Performance

**NFR-1.1**: AQI prediction response time shall be under 2 seconds
**NFR-1.2**: Carbon calculation response time shall be under 1 second
**NFR-1.3**: The system shall handle concurrent requests from multiple users

### 3.2 Reliability

**NFR-2.1**: The system shall provide graceful degradation when data is unavailable
**NFR-2.2**: The ML model shall be pre-trained and loaded at application startup
**NFR-2.3**: The system shall maintain 99% uptime during operational hours

### 3.3 Usability

**NFR-3.1**: The interface shall be intuitive and require no training
**NFR-3.2**: Results shall be displayed in user-friendly formats
**NFR-3.3**: The application shall be responsive across desktop and mobile devices

### 3.4 Maintainability

**NFR-4.1**: Code shall follow Python PEP 8 style guidelines
**NFR-4.2**: The system shall use modular architecture for easy updates
**NFR-4.3**: ML models shall be versioned and easily replaceable

### 3.5 Scalability

**NFR-5.1**: The system architecture shall support horizontal scaling
**NFR-5.2**: The application shall be deployable on cloud platforms (Vercel)
**NFR-5.3**: Database/CSV storage shall accommodate growing historical data

### 3.6 Security

**NFR-6.1**: Input validation shall prevent injection attacks
**NFR-6.2**: API endpoints shall handle malformed requests gracefully
**NFR-6.3**: No sensitive user data shall be stored or logged

---

## 4. Constraints

### 4.1 Technical Constraints

**C-1.1**: The application must be built using Flask framework
**C-1.2**: Machine learning models must use scikit-learn library
**C-1.3**: The system must run on Python 3.x environment
**C-1.4**: Frontend must use standard HTML/CSS/JavaScript (no framework dependencies)

### 4.2 Data Constraints

**C-2.1**: AQI predictions are limited to cities present in the training dataset
**C-2.2**: Historical data must include at least 7 days for accurate predictions
**C-2.3**: Emission factors are based on standard transportation emission databases

### 4.3 Deployment Constraints

**C-3.1**: The application must be deployable on Vercel platform
**C-3.2**: Static files must be served from the `/static` directory
**C-3.3**: Templates must be stored in the `/templates` directory

### 4.4 Resource Constraints

**C-4.1**: ML model file size should be optimized for fast loading
**C-4.2**: CSV data files should be kept under reasonable size limits
**C-4.3**: No external database dependencies in initial version

---

## 5. Assumptions

### 5.1 Data Assumptions

**A-1.1**: Historical AQI data in `aqi_data.csv` is accurate and up-to-date
**A-1.2**: City names in the dataset follow consistent naming conventions
**A-1.3**: Pollutant measurements (PM2.5, PM10, NO2, SO2) are in standard units
**A-1.4**: The last 7 days of data are representative for next-day prediction

### 5.2 User Assumptions

**A-2.1**: Users have basic understanding of AQI and carbon emissions
**A-2.2**: Users will provide reasonable distance values for calculations
**A-2.3**: Users have access to modern web browsers with JavaScript enabled
**A-2.4**: Primary user base is in India (Delhi as default city)

### 5.3 Model Assumptions

**A-3.1**: The pre-trained ML model (`aqi_model.pkl`) is properly trained and validated
**A-3.2**: Model accuracy is sufficient for general awareness purposes
**A-3.3**: Emission factors remain relatively stable over time
**A-3.4**: Linear relationship exists between distance and emissions for each transport mode

### 5.4 Operational Assumptions

**A-4.1**: The application will be accessed during normal internet connectivity
**A-4.2**: Server infrastructure has sufficient resources for expected load
**A-4.3**: No real-time data feeds are required (batch updates acceptable)
**A-4.4**: Debug mode will be disabled in production deployment

### 5.5 Business Assumptions

**A-5.1**: The application is for educational and awareness purposes
**A-5.2**: No monetization or user authentication required in initial version
**A-5.3**: Recommendations are advisory and not legally binding
**A-5.4**: Users understand predictions are estimates, not guarantees

---

## 6. Future Enhancements (Out of Scope for Current Version)

- Multi-day AQI forecasting
- User accounts and historical tracking
- Additional carbon sources (electricity, food, etc.)
- Real-time AQI data integration
- Mobile native applications
- Multi-language support
- Social sharing features
- Gamification and achievement system

---

**Document Version**: 1.0  
**Last Updated**: February 15, 2026  
**Project**: breatheSmart
