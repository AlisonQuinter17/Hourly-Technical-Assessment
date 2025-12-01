# Financial Transaction Processor

A full-stack web application to upload CSV files with financial transactions, process them asynchronously, and view a summary dashboard.

## 🚀 Tech Stack

- **Backend**: Python (Flask), SQLAlchemy, PostgreSQL
- **Frontend**: React (Vite), Tailwind
- **Database**: PostgreSQL (Docker)

## 📸 Demo
![Upload Process](assets/transactions-video-test.gif)

## 🎯 Quick Start

The easiest way to run the application is using Docker Compose.

```bash
# Build and start all services
docker-compose up --build
```

Access the application:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000

## 🧪 Running Tests

### Backend
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run tests
cd backend
pytest
```

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Run tests
npm test
```

## 🔧 API Endpoints

- `POST /transactions/upload`: Upload a CSV file.
- `GET /transactions`: Get all transactions.
- `GET /transactions/{id}`: Get transaction details.

## 📊 CSV Format

```csv
id,date,type,amount
1,2024-01-01,debit,100.00
2,2024-01-02,credit,50.00
```
