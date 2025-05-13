# API routes
from flask import Blueprint, request
from . import api_response
import json

from app.services.query_service import query_messages, query_by_question
from app.services.ai_service import extract_tags_with_ai, generate_answer_with_ai
from app.services.news_service import generate_daily_news, generate_ddl_events

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/messages', methods=['GET'])
def get_messages():
    """Direct query for messages (advanced users)"""
    try:
        # Get query parameters
        message_type = request.args.get('message_type')
        query_conditions_str = request.args.get('query_conditions', '{}')
        
        # Validate message type
        if not message_type:
            return api_response(message="Message type is required", code=400)
        
        # Parse query conditions
        try:
            query_conditions = json.loads(query_conditions_str)
        except json.JSONDecodeError:
            return api_response(message="Query conditions must be valid JSON", code=400)
        
        # Execute query
        results = query_messages(message_type, query_conditions)
        
        return api_response(results)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/news/today', methods=['GET'])
def get_today_news():
    """Get daily news summary"""
    try:
        # Call generate daily news function
        news_data = generate_daily_news()
        return api_response(news_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/ddl-events', methods=['GET'])
def get_ddl_events():
    """Get recent important DDL event list"""
    try:
        # Call generate DDL events function
        events_data = generate_ddl_events()
        return api_response(events_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/knowledge/query', methods=['POST'])
def ask_question():
    """Complete process for handling user questions"""
    try:
        # Get user question
        data = request.get_json()
        if not data or 'question' not in data:
            return api_response(message="Question cannot be empty", code=400)
            
        question = data.get('question', '')
        
        # Use AI to extract query tags
        extracted_tags = extract_tags_with_ai(question)
        
        # Query relevant information - using flexible query function
        results = query_by_question(question, extracted_tags)
        
        # Generate answer
        answer = generate_answer_with_ai(question, results)
        
        # Build response data - include more information
        references = []
        for i, r in enumerate(results):
            # Extract summary information of tags and content
            tags_summary = ", ".join([f"{k}: {v}" for k, v in r.get('tags', {}).items() if k != 'time'])
            content_preview = str(r.get('content', {}))[:50] + '...' if r.get('content') else ''
            
            reference = {
                'id': i+1,
                'type': r.get('message_type', 'Unknown type'),
                'tags': tags_summary,
                'content_preview': content_preview
            }
            references.append(reference)
        
        response_data = {
            'question': question,
            'extracted_tags': extracted_tags,  # Add extracted tags
            'answer': answer,
            'references': references
        }
        
        return api_response(response_data)
    except Exception as e:
        return api_response(message=str(e), code=500)

@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """Return API documentation"""
    from ..config.settings import MESSAGE_TYPES
    
    docs = {
        "api_version": "1.0",
        "message_types": {
            "description": "Message types supported by the system",
            "types": list(MESSAGE_TYPES.keys())
        },
        "endpoints": [
            {
                "path": "/api/news/today",
                "method": "GET",
                "description": "Get daily message summary",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "Success",
                        "schema": {
                            "date": "Date (ISO format)",
                            "content": "Message content (text or JSON)",
                            "format": "Content format (text or json)"
                        }
                    }
                }
            },
            {
                "path": "/api/ddl-events",
                "method": "GET",
                "description": "Get list of upcoming important DDL events",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "Success",
                        "schema": {
                            "name": "Event name",
                            "ddl": "Deadline date (YYYY-MM-DD)"
                        }
                    }
                }
            },
            {
                "path": "/api/knowledge/query",
                "method": "POST",
                "description": "Intelligent Q&A",
                "parameters": [
                    {
                        "name": "question",
                        "type": "string",
                        "required": True,
                        "description": "User question"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Success",
                        "schema": {
                            "question": "User question",
                            "extracted_tags": "Query tags extracted by AI",
                            "answer": "Answer generated by AI",
                            "references": "References, including message type, tag summary and content preview"
                        }
                    }
                }
            },
            {
                "path": "/api/messages",
                "method": "GET",
                "description": "Direct message query (advanced users)",
                "parameters": [
                    {
                        "name": "message_type",
                        "type": "string",
                        "required": True,
                        "description": "Message type, refer to message_types field"
                    },
                    {
                        "name": "query_conditions",
                        "type": "json",
                        "required": False,
                        "description": "Query conditions, JSON format, including tags and content parts"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Success",
                        "schema": {
                            "id": "Message ID",
                            "tags": "Tags JSON object",
                            "content": "Content JSON object",
                            "message_type": "Message type"
                        }
                    }
                }
            }
        ]
    }
    return api_response(docs)