import os
import sys
import logging
from dotenv import load_dotenv

# Import agents
from agents.triage_agent import TriageAgent
from agents.jtbd_agent import JTBDAgent
from agents.researcher_agent import ResearcherAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class JTBDMultiAgentSystem:
    """Main class for the JTBD Multi-Agent System."""
    
    def __init__(self):
        """Initialize the multi-agent system."""
        logger.info("Initializing JTBD Multi-Agent System")
        
        # Initialize agents
        self.triage_agent = TriageAgent()
        self.jtbd_agent = JTBDAgent()
        self.researcher_agent = ResearcherAgent()
    
    def process_query(self, user_query):
        """
        Process a user query through the multi-agent system.
        
        Args:
            user_query (str): The user's query about a topic
            
        Returns:
            dict: The response from the appropriate agent(s)
        """
        logger.info(f"Processing query: {user_query}")
        
        # Step 1: Triage the query
        triage_result = self.triage_agent.triage(user_query)
        
        # Step 2: Check data completeness
        data_completeness = triage_result.get("data_completeness", "none")
        topic = triage_result.get("topic", "")
        
        # Step 3: Route to appropriate agent based on data completeness
        if data_completeness == "complete":
            logger.info(f"Complete data found for topic: {topic}. Routing to JTBD Agent.")
            return self.jtbd_agent.analyze(topic, full_analysis=True)
        
        elif data_completeness == "partial":
            logger.info(f"Partial data found for topic: {topic}. Routing to JTBD Agent with research suggestions.")
            jtbd_analysis = self.jtbd_agent.analyze(topic, full_analysis=False)
            research_suggestions = self.researcher_agent.generate_research_plan(topic, jtbd_analysis)
            
            return {
                "jtbd_analysis": jtbd_analysis,
                "research_suggestions": research_suggestions,
                "note": "The data is not sufficient to be fully reliable. Additional research is recommended."
            }
        
        else:  # No data
            logger.info(f"No data found for topic: {topic}. Routing to Researcher Agent.")
            return self.researcher_agent.generate_research_plan(topic)

def main():
    """Main function to run the JTBD Multi-Agent System."""
    system = JTBDMultiAgentSystem()
    
    # Example usage
    query = "What are the jobs to be done for online grocery shopping?"
    result = system.process_query(query)
    
    print("\n===== JTBD Multi-Agent System Result =====")
    print(f"Query: {query}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main() 