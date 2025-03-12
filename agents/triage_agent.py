import os
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class TriageAgent:
    """
    The Triage Agent processes user questions and determines the appropriate routing
    based on data availability for the requested topic.
    """
    
    def __init__(self):
        """Initialize the Triage Agent."""
        self.data_directory = Path("data")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
            logger.info(f"Created data directory at {self.data_directory}")
    
    def triage(self, user_query):
        """
        Process the user query and determine data completeness.
        
        Args:
            user_query (str): The user's query about a topic
            
        Returns:
            dict: Triage result containing topic and data completeness assessment
        """
        # Extract the topic from the user query
        topic = self._extract_topic(user_query)
        
        # Check data completeness for the topic
        data_completeness = self._check_data_completeness(topic)
        
        logger.info(f"Triage result for '{topic}': Data completeness = {data_completeness}")
        
        return {
            "query": user_query,
            "topic": topic,
            "data_completeness": data_completeness
        }
    
    def _extract_topic(self, user_query):
        """
        Extract the main topic from the user query.
        
        In a production system, this would use NLP techniques for better topic extraction.
        For this demo, we'll use a simple approach.
        
        Args:
            user_query (str): The user's query
            
        Returns:
            str: The extracted topic
        """
        # Simple implementation - look for "for" in the query
        if "for" in user_query.lower():
            parts = user_query.lower().split("for")
            if len(parts) > 1:
                topic = parts[1].strip().strip("?").strip()
                return topic
        
        # If no "for" is found, just return the query without question marks
        return user_query.strip().strip("?").strip()
    
    def _check_data_completeness(self, topic):
        """
        Check the completeness of data available for the given topic.
        
        Args:
            topic (str): The topic to check
            
        Returns:
            str: Data completeness assessment ("complete", "partial", or "none")
        """
        # Normalized topic name for file matching
        normalized_topic = topic.lower().replace(" ", "_")
        
        # Look for matching data files
        data_files = list(self.data_directory.glob(f"*{normalized_topic}*.json"))
        
        if not data_files:
            return "none"
        
        # Check the completeness of the data in the files
        total_sources = 0
        total_entries = 0
        
        for file_path in data_files:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Count sources and entries
                    sources = data.get("sources", [])
                    total_sources += len(sources)
                    
                    entries = data.get("research_data", [])
                    total_entries += len(entries)
            except Exception as e:
                logger.error(f"Error reading data file {file_path}: {e}")
        
        # Determine completeness based on the amount of data
        # This is a simplified heuristic and should be adjusted for real-world use
        if total_sources >= 3 and total_entries >= 15:
            return "complete"
        elif total_sources >= 1 and total_entries >= 5:
            return "partial"
        else:
            return "none" 