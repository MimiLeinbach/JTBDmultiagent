import json
import random
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TestDataGenerator:
    """
    Generates test research data for the JTBD multi-agent system.
    """
    
    def __init__(self):
        """Initialize the test data generator."""
        self.data_directory = Path("data")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
            logger.info(f"Created data directory at {self.data_directory}")
    
    def generate_data(self, topic, complete=True, partial=False, save=True):
        """
        Generate test research data for a given topic.
        
        Args:
            topic (str): The topic to generate data for
            complete (bool): Whether to generate complete data
            partial (bool): Whether to generate partial data
            save (bool): Whether to save the data to files
            
        Returns:
            dict: The generated data
        """
        if complete:
            data = self._generate_complete_data(topic)
            if save:
                self._save_data(data, f"{topic.lower().replace(' ', '_')}_complete.json")
            return data
        
        elif partial:
            data = self._generate_partial_data(topic)
            if save:
                self._save_data(data, f"{topic.lower().replace(' ', '_')}_partial.json")
            return data
        
        else:
            return {}
    
    def _generate_complete_data(self, topic):
        """
        Generate complete research data for a topic.
        
        Args:
            topic (str): The topic to generate data for
            
        Returns:
            dict: The generated data
        """
        # Define sources for complete data
        sources = [
            "User Interviews",
            "Customer Support Logs",
            "Product Reviews",
            "Survey Responses",
            "Usability Testing"
        ]
        
        # Generate research data with a good mix of functional, social, and emotional jobs
        research_data = []
        
        # Generate data from each source
        for source in sources:
            # Number of entries per source
            entries_count = random.randint(5, 10)
            
            for _ in range(entries_count):
                entry = self._generate_research_entry(topic, source)
                research_data.append(entry)
        
        return {
            "topic": topic,
            "sources": sources,
            "research_data": research_data
        }
    
    def _generate_partial_data(self, topic):
        """
        Generate partial research data for a topic.
        
        Args:
            topic (str): The topic to generate data for
            
        Returns:
            dict: The generated data
        """
        # Define sources for partial data (fewer sources)
        sources = random.sample([
            "User Interviews",
            "Customer Support Logs",
            "Product Reviews"
        ], 2)
        
        # Generate research data with limited entries
        research_data = []
        
        # Generate data from each source
        for source in sources:
            # Fewer entries per source for partial data
            entries_count = random.randint(2, 5)
            
            for _ in range(entries_count):
                entry = self._generate_research_entry(topic, source)
                research_data.append(entry)
        
        return {
            "topic": topic,
            "sources": sources,
            "research_data": research_data
        }
    
    def _generate_research_entry(self, topic, source):
        """
        Generate a single research data entry.
        
        Args:
            topic (str): The topic for the entry
            source (str): The source of the data
            
        Returns:
            dict: The generated entry
        """
        # Select job type
        job_type = random.choice(["functional", "social", "emotional"])
        
        # Generate statement based on job type
        if job_type == "functional":
            statement = self._generate_functional_statement(topic)
            context = random.choice([
                f"When discussing how they accomplish tasks with {topic}",
                f"While demonstrating their use of {topic}",
                f"When asked about their workflow with {topic}",
                f"During a discussion about productivity and {topic}"
            ])
        elif job_type == "social":
            statement = self._generate_social_statement(topic)
            context = random.choice([
                f"When discussing how others perceive their use of {topic}",
                f"In a conversation about workplace status and {topic}",
                f"When asked about sharing their experience with {topic}",
                f"During a discussion about professional identity and {topic}"
            ])
        else:  # emotional
            statement = self._generate_emotional_statement(topic)
            context = random.choice([
                f"When reflecting on their feelings about {topic}",
                f"After using {topic} for a challenging task",
                f"When discussing stress factors related to {topic}",
                f"During a conversation about satisfaction with {topic}"
            ])
        
        # Generate user demographics
        age = random.randint(18, 65)
        gender = random.choice(["Male", "Female", "Non-binary"])
        experience_level = random.choice(["Beginner", "Intermediate", "Advanced"])
        
        return {
            "statement": statement,
            "source": source,
            "context": context,
            "job_type": job_type,
            "user_demographics": {
                "age": age,
                "gender": gender,
                "experience_level": experience_level
            }
        }
    
    def _generate_functional_statement(self, topic):
        """
        Generate a statement about functional jobs.
        
        Args:
            topic (str): The topic for the statement
            
        Returns:
            str: A functional job statement
        """
        templates = [
            f"I need to use {topic} to get my work done faster.",
            f"I have to use {topic} because it helps me organize everything in one place.",
            f"Using {topic} allows me to accomplish multiple tasks at once.",
            f"I want to use {topic} that doesn't require much training or setup.",
            f"{topic} helps me avoid mistakes in my work.",
            f"I need {topic} to handle the complex parts of the process automatically.",
            f"I'm trying to find a {topic} solution that integrates with my existing tools.",
            f"The main reason I use {topic} is to save time on repetitive tasks.",
            f"{topic} needs to help me track my progress toward my goals.",
            f"I switch between different {topic} options until I find one that's efficient enough.",
            f"The most important thing for me is that {topic} is reliable and doesn't crash.",
            f"I need {topic} to work across all my devices seamlessly."
        ]
        
        return random.choice(templates)
    
    def _generate_social_statement(self, topic):
        """
        Generate a statement about social jobs.
        
        Args:
            topic (str): The topic for the statement
            
        Returns:
            str: A social job statement
        """
        templates = [
            f"My colleagues respect me more when they see me using {topic} effectively.",
            f"I want people to see that I'm skilled with advanced {topic} features.",
            f"Using {topic} shows that I'm serious about my work.",
            f"I feel like I belong to a community of professionals who use {topic}.",
            f"It's important that my boss sees me using {topic} to solve problems.",
            f"I don't want to be the only person in my team who doesn't understand {topic}.",
            f"People ask for my advice about {topic}, which makes me feel valued.",
            f"Using the latest {topic} trends helps me stay relevant in my industry.",
            f"I want to be seen as an expert in {topic} by my peers.",
            f"Being able to recommend good {topic} solutions gives me status in my network.",
            f"I don't talk about using {topic} because I don't want to seem like I'm showing off.",
            f"I want my clients to be impressed by the {topic} tools I use."
        ]
        
        return random.choice(templates)
    
    def _generate_emotional_statement(self, topic):
        """
        Generate a statement about emotional jobs.
        
        Args:
            topic (str): The topic for the statement
            
        Returns:
            str: An emotional job statement
        """
        templates = [
            f"I feel anxious when {topic} isn't working correctly.",
            f"Using {topic} gives me confidence that I won't miss anything important.",
            f"I get frustrated when {topic} is too complicated to figure out quickly.",
            f"I feel a sense of accomplishment when I master new {topic} features.",
            f"I worry about making mistakes when using {topic} for important tasks.",
            f"I feel overwhelmed by all the {topic} options available.",
            f"Using {topic} gives me peace of mind knowing my work is backed up.",
            f"I feel in control when I use {topic} to organize my projects.",
            f"I get excited when I discover new ways that {topic} can help me.",
            f"I feel stressed when {topic} changes its interface or features.",
            f"I trust that {topic} will protect my privacy and security.",
            f"I feel satisfied when {topic} helps me complete something difficult."
        ]
        
        return random.choice(templates)
    
    def _save_data(self, data, filename):
        """
        Save generated data to a JSON file.
        
        Args:
            data (dict): The data to save
            filename (str): The name of the file to save to
        """
        file_path = self.data_directory / filename
        
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            
            logger.info(f"Saved test data to {file_path}")
        
        except Exception as e:
            logger.error(f"Error saving test data to {file_path}: {e}")


def generate_sample_datasets():
    """Generate sample datasets for common topics."""
    generator = TestDataGenerator()
    
    # Generate complete datasets
    topics_complete = [
        "online grocery shopping",
        "project management software",
        "video conferencing tools"
    ]
    
    # Generate partial datasets
    topics_partial = [
        "meal kit delivery services",
        "fitness tracking apps"
    ]
    
    # Generate the datasets
    for topic in topics_complete:
        generator.generate_data(topic, complete=True, partial=False)
    
    for topic in topics_partial:
        generator.generate_data(topic, complete=False, partial=True)
    
    logger.info("Generated sample datasets for testing")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Generate sample datasets
    generate_sample_datasets() 