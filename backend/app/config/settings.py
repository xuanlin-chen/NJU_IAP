# Configuration settings for the application

# Flask and Database settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://crawler:241880625@47.122.71.85:3306/information_for_students?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OpenAI configuration
OPENAI_API_KEY = "your-openai-key"

# Message type definitions
MESSAGE_TYPES = {
    # Sample message type configuration
    "通知": {
        "table_name": "notifications",
        "tags_schema": {
            # Tag structure definition
        },
        "content_schema": {
            # Content structure definition
        }
    },
    "规章制度": {
        "table_name": "regulations",
        "tags_schema": {
            # Tag structure definition
        },
        "content_schema": {
            # Content structure definition
        }
    }
    # Add more message types as needed
}