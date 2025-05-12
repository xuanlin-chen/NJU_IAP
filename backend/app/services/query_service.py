# Query services for database interaction
import json
from ..models.db import db
from ..config.settings import MESSAGE_TYPES

def query_messages(message_type, query_conditions=None):
    """Generic message query function
    
    Args:
        message_type: Message type (e.g., "通知", "规章制度", etc.)
        query_conditions: Query condition dictionary, including tags and content parts
        
    Returns:
        Query result list
    """
    if message_type not in MESSAGE_TYPES:
        return []
    
    table_name = MESSAGE_TYPES[message_type]["table_name"]
    query_conditions = query_conditions or {}
    
    # Build base SQL query
    query = f"SELECT id, tags_json, content_json FROM {table_name} WHERE 1=1"
    params = []
    
    # Handle tag query conditions
    if "tags" in query_conditions:
        for path, value in _flatten_json_conditions(query_conditions["tags"]):
            query += f" AND JSON_EXTRACT(tags_json, '$.{path}') = %s"
            params.append(str(value))
    
    # Handle content query conditions
    if "content" in query_conditions:
        for path, value in _flatten_json_conditions(query_conditions["content"]):
            query += f" AND JSON_EXTRACT(content_json, '$.{path}') = %s"
            params.append(str(value))
    
    try:
        # Execute query using SQLAlchemy
        result = db.session.execute(query, params)
        messages = result.fetchall()
        
        # Format results
        messages_data = []
        for msg in messages:
            try:
                # Parse JSON fields
                tags = json.loads(msg.tags_json) if msg.tags_json else {}
                content = json.loads(msg.content_json) if msg.content_json else {}
                
                message_data = {
                    'id': msg.id,
                    'tags': tags,
                    'content': content,
                    'message_type': message_type
                }
                messages_data.append(message_data)
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error processing message {msg.id}: {e}")
                continue
        
        return messages_data
    except Exception as e:
        print(f"Database query error: {e}")
        return []

def _flatten_json_conditions(conditions, parent_path=''):
    """Flatten nested JSON query conditions into path-value pairs
    
    Args:
        conditions: Nested query condition dictionary
        parent_path: Parent path prefix
        
    Returns:
        Flattened path-value pair list
    """
    flattened = []
    for key, value in conditions.items():
        current_path = f"{parent_path}.{key}" if parent_path else key
        
        if isinstance(value, dict):
            # Handle nested dictionaries recursively
            flattened.extend(_flatten_json_conditions(value, current_path))
        else:
            flattened.append((current_path, value))
    
    return flattened

def query_by_question(question, extracted_tags):
    """Query relevant information based on user question
    
    Args:
        question: User question
        extracted_tags: Tags extracted by AI
        
    Returns:
        Query result list
    """
    # TODO: Implement intelligent query based on extracted tags
    # 1. Analyze extracted tags to determine message type
    # 2. Build query conditions
    # 3. Call query_messages function to execute query
    
    # Sample implementation (needs adjustment based on actual requirements)
    results = []
    
    # Try querying all message types
    for message_type in MESSAGE_TYPES.keys():
        # Build query conditions - this needs intelligent mapping from AI tags
        query_conditions = {"tags": {}, "content": {}}
        
        # TODO: Fill query_conditions based on extracted_tags
        # Simple example, actual implementation needs more complex logic
        for tag in extracted_tags:
            # Assume tag is a dictionary containing key and value
            if isinstance(tag, dict) and "key" in tag and "value" in tag:
                # Check if tag belongs to current message type's tag pattern
                if tag["key"] in MESSAGE_TYPES[message_type]["tags_schema"]:
                    query_conditions["tags"][tag["key"]] = tag["value"]
                elif tag["key"] in MESSAGE_TYPES[message_type]["content_schema"]:
                    query_conditions["content"][tag["key"]] = tag["value"]
        
        # Execute query if conditions exist
        if query_conditions["tags"] or query_conditions["content"]:
            message_results = query_messages(message_type, query_conditions)
            results.extend(message_results)
    
    return results