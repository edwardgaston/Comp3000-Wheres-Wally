# Object Detection Backend

This project is a backend application for an object detection model built using the MERN stack (MongoDB, Express, React, Node.js). It provides RESTful APIs to handle object detection requests.

## Project Structure

```
object-detection-backend
├── src
│   ├── app.js                     # Entry point of the application
│   ├── config
│   │   └── db.js                  # Database connection configuration
│   ├── controllers
│   │   └── objectDetectionController.js # Controller for object detection logic
│   ├── models
│   │   └── objectDetectionModel.js # Mongoose model for object detection data
│   ├── routes
│   │   └── objectDetectionRoutes.js # Routes for object detection API
│   └── utils
│       └── index.js                # Utility functions
├── package.json                    # NPM package configuration
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd object-detection-backend
   ```

3. Install the dependencies:
   ```
   npm install
   ```

4. Create a `.env` file in the root directory and add your MongoDB connection string:
   ```
   MONGODB_URI=<your_mongodb_connection_string>
   ```

## Usage

1. Start the server:
   ```
   npm start
   ```

2. The server will run on `http://localhost:5000` by default.

## API Endpoints

- `POST /api/detections` - Create a new object detection entry.
- `GET /api/detections` - Retrieve all object detection entries.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.