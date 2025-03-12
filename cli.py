import sys
import json
import logging
import argparse
from main import JTBDMultiAgentSystem
from utils.data_generator import TestDataGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="JTBD Multi-Agent System CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Query parser
    query_parser = subparsers.add_parser("query", help="Process a user query")
    query_parser.add_argument("text", type=str, help="The query text to process")
    
    # Generate data parser
    generate_parser = subparsers.add_parser("generate", help="Generate test data")
    generate_parser.add_argument("topic", type=str, help="The topic to generate data for")
    generate_parser.add_argument("--complete", action="store_true", help="Generate complete data")
    generate_parser.add_argument("--partial", action="store_true", help="Generate partial data")
    
    return parser.parse_args()

def process_query(query_text):
    """Process a user query."""
    system = JTBDMultiAgentSystem()
    result = system.process_query(query_text)
    
    # Pretty print the result
    print("\n===== JTBD Multi-Agent System Result =====")
    print(f"Query: {query_text}")
    print("\nResult:")
    print(json.dumps(result, indent=2))

def generate_data(topic, complete=False, partial=False):
    """Generate test data for a topic."""
    if not complete and not partial:
        complete = True  # Default to complete if neither is specified
    
    generator = TestDataGenerator()
    data = generator.generate_data(topic, complete=complete, partial=partial)
    
    print(f"\nGenerated {'complete' if complete else 'partial'} test data for topic: {topic}")
    print(f"Data saved to: data/{topic.lower().replace(' ', '_')}_{('complete' if complete else 'partial')}.json")

def main():
    """Main function for the CLI."""
    args = parse_args()
    
    if args.command == "query":
        process_query(args.text)
    
    elif args.command == "generate":
        generate_data(args.topic, args.complete, args.partial)
    
    else:
        print("Please specify a command. Use --help for more information.")

if __name__ == "__main__":
    main() 