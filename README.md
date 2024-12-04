```
# Image Processing System

This system works with two pictures – a 'before' and an 'after.' Both pictures need to be the same size for the system to do its magic. The backend, powered by OpenCV in Python, analyzes these images and uploads the results to Firebase. The frontend, built with ReactJS, showcases the processed images.

## Demo

Check out the live demo (https://ccc-imageproccessing.netlify.app/).

## Table of Contents
- [Backend Installation](#backend-installation)
- [Frontend Installation](#frontend-installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

## Backend Installation

Ensure you have Python and the required dependencies installed.

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/AbdinasirM/ImageProcessingApp.git]
   ```

2. **Navigate to the backend folder:**

   ```bash
   cd backend
   ```

3. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Frontend Installation

1. **Navigate to the frontend folder:**

   ```bash
   cd frontend
   ```

2. **Install frontend dependencies:**

   ```bash
   npm install
   ```

## Usage

1. Prepare two images – a 'before' and an 'after,' ensuring they are the same size.
2. **Run the backend:**

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. The backend will analyze the images and upload the results to Firebase.
4. **Run the frontend:**

   ```bash
   cd frontend
   npm run dev
   ```

5. Access the frontend at [http://localhost:8000](http://localhost:port) to view the processed images.

## Tech Stack

### Backend
- Python
- OpenCV
- Firebase

### Frontend
- ReactJS

