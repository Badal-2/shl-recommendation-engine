 # SHL Assessment Recommendation Engine

AI-powered test recommendation system for talent assessment using FastAPI, PostgreSQL, and Machine Learning.

## 🎯 Features

- **AI-Powered Recommendations**: Uses TF-IDF and Cosine Similarity to match job roles with assessments
- **RESTful API**: Built with FastAPI for high performance
- **PostgreSQL Database**: Stores assessments, job roles, and recommendation history
- **Interactive Frontend**: Clean, responsive UI for easy interaction
- **Real-time Processing**: Instant recommendations with confidence scores

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI
- **Database**: PostgreSQL
- **ML/AI**: Scikit-learn, TF-IDF, Cosine Similarity
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Render.com

## 📁 Project Structure
```
shl-recommendation-engine/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── ml_model.py          # ML recommendation engine
│   └── utils.py
├── ml/
│   ├── train_model.py       # Model training script
│   ├── seed_database.py     # Database seeder
│   └── data/
│       └── sample_assessments.py
├── static/
│   └── index.html           # Frontend UI
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Git

8. **Access the application**
- API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:8000/static/index.html

## 📡 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /db-status` - Database connection status

### Assessment Endpoints

- `GET /assessments` - Get all assessments
- `GET /assessments/{id}` - Get specific assessment
- `GET /job-roles` - Get all job roles
- `GET /stats` - Database statistics





### Recommendation Endpoint

- `POST /recommend` - Get AI recommendations

**Request Body:**
```json
{
  "job_role": "Software Engineer",
  "top_k": 5
}
```

**Response:**
```json
{
  "job_role": "Software Engineer",
  "recommendations": [
    {
      "test_name": "Python Coding Assessment",
      "confidence_score": 87.5,
      "category": "Technical",
      "test_description": "...",
      "skills_match": "Python, Algorithms, Problem Solving"
    }
  ],
  "total_recommendations": 5,
  "timestamp": "2024-12-17T10:30:00"
}
```

## 🤖 ML Model Details

**Algorithm**: TF-IDF (Term Frequency-Inverse Document Frequency) + Cosine Similarity

**How it works**:
1. Converts job roles and test descriptions to numerical vectors
2. Calculates similarity scores between job role and all tests
3. Returns top K most relevant tests with confidence scores
4. Confidence score = Similarity score × 100

**Features Used**:
- Test name
- Test description
- Skills assessed
- Category (Technical/Cognitive/Behavioral)

## 🎨 Frontend Features

- Clean, modern gradient UI
- Real-time API integration
- Loading animations
- Error handling
- Quick suggestion chips
- Responsive design (mobile-friendly)
- Confidence score badges

## 📦 Deployment

### Deploy on Render.com

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

## 🧪 Testing

Test the API using Swagger UI:
```
http://your-domain/docs
```

Or use curl:
```bash
curl -X POST "http://your-domain/recommend" \
  -H "Content-Type: application/json" \
  -d '{"job_role": "Data Scientist", "top_k": 5}'
```

## 📊 Sample Data

The system includes 15 pre-configured assessments:
- Technical Tests (Python, JavaScript, SQL, ML, DevOps, etc.)
- Cognitive Tests (Logic, Numerical, Verbal Reasoning)
- Behavioral Tests (Leadership, Communication, Project Management)

## 🔒 Environment Variables
```env
DATABASE_URL=postgresql://user:pass@host:port/db
APP_NAME=SHL Recommendation Engine
DEBUG=False  # Set to False in production
```

## 📝 License

This project is created as part of SHL AI Research Intern Application.

## 👤 Author

[Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- SHL for the internship opportunity
- FastAPI framework
- Scikit-learn for ML capabilities