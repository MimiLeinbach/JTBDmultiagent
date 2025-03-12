import os
import json
import logging
from pathlib import Path
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

logger = logging.getLogger(__name__)

class JTBDAgent:
    """
    The JTBD Agent analyzes research data to identify Jobs to Be Done
    and clusters them into themes.
    """
    
    def __init__(self):
        """Initialize the JTBD Agent."""
        self.data_directory = Path("data")
    
    def analyze(self, topic, full_analysis=True):
        """
        Analyze the data for a given topic to identify JTBD insights.
        
        Args:
            topic (str): The topic to analyze
            full_analysis (bool): Whether to perform a full analysis
            
        Returns:
            dict: JTBD analysis results
        """
        # Load data for the topic
        research_data = self._load_research_data(topic)
        
        if not research_data:
            logger.warning(f"No research data found for topic: {topic}")
            return {"error": "No research data found for the specified topic"}
        
        # Step 1: Extract jobs from research data
        jobs = self._extract_jobs(research_data)
        
        # Step 2: Cluster jobs into themes
        themes = self._cluster_into_themes(jobs)
        
        # Step 3: Rank themes
        ranked_themes = self._rank_themes(themes)
        
        # Step 4: Summarize results
        result = {
            "topic": topic,
            "analysis_type": "full" if full_analysis else "partial",
            "themes": ranked_themes,
            "functional_jobs": self._filter_jobs_by_type(jobs, "functional"),
            "social_jobs": self._filter_jobs_by_type(jobs, "social"),
            "emotional_jobs": self._filter_jobs_by_type(jobs, "emotional"),
            "sources": research_data.get("sources", []),
            "data_points": len(research_data.get("research_data", [])),
        }
        
        # Add reliability assessment if it's not a full analysis
        if not full_analysis:
            result["reliability"] = self._assess_reliability(research_data)
        
        return result
    
    def _load_research_data(self, topic):
        """
        Load research data for the given topic.
        
        Args:
            topic (str): The topic to load data for
            
        Returns:
            dict: The combined research data for the topic
        """
        normalized_topic = topic.lower().replace(" ", "_")
        
        # Look for matching data files
        data_files = list(self.data_directory.glob(f"*{normalized_topic}*.json"))
        
        if not data_files:
            return {}
        
        # Combine data from multiple files
        combined_data = {
            "topic": topic,
            "sources": [],
            "research_data": []
        }
        
        for file_path in data_files:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Add sources
                    combined_data["sources"].extend(data.get("sources", []))
                    
                    # Add research data
                    combined_data["research_data"].extend(data.get("research_data", []))
            except Exception as e:
                logger.error(f"Error reading data file {file_path}: {e}")
        
        # Remove duplicate sources
        combined_data["sources"] = list(set(combined_data["sources"]))
        
        return combined_data
    
    def _extract_jobs(self, research_data):
        """
        Extract jobs from research data and categorize them.
        
        Args:
            research_data (dict): Research data containing interviews, surveys, etc.
            
        Returns:
            list: List of extracted and categorized jobs
        """
        jobs = []
        
        for entry in research_data.get("research_data", []):
            # Extract each statement/quote
            statement = entry.get("statement", "")
            source = entry.get("source", "Unknown")
            context = entry.get("context", "")
            
            # Classify the job type (in a real system, this would use NLP)
            job_types = self._classify_job_types(statement, context)
            
            # For each identified job type, create a job entry
            for job_type in job_types:
                jobs.append({
                    "statement": statement,
                    "type": job_type,
                    "source": source,
                    "context": context,
                    "frequency": 1  # Start with a frequency of 1
                })
        
        # Combine similar jobs and increment frequencies
        combined_jobs = self._combine_similar_jobs(jobs)
        
        return combined_jobs
    
    def _classify_job_types(self, statement, context):
        """
        Classify the statement into job types (functional, social, emotional).
        
        In a production system, this would use more sophisticated NLP.
        For this demo, we'll use simple keyword matching.
        
        Args:
            statement (str): User statement or quote
            context (str): Additional context about the statement
            
        Returns:
            list: List of job types identified
        """
        statement_lower = statement.lower() + " " + context.lower()
        
        job_types = []
        
        # Functional job indicators (related to practical tasks and outcomes)
        functional_indicators = [
            "need to", "have to", "want to", "trying to", "easier", "faster",
            "efficient", "help me", "allows me", "lets me", "enables me",
            "accomplish", "complete", "finish", "get done", "achieve"
        ]
        
        # Social job indicators (related to how others perceive the user)
        social_indicators = [
            "others think", "people see", "impression", "look good",
            "respected", "admired", "recognized", "status", "reputation",
            "colleagues", "friends", "family", "peers", "society",
            "community", "belong", "fit in", "stand out"
        ]
        
        # Emotional job indicators (related to how the user feels)
        emotional_indicators = [
            "feel", "feeling", "happy", "satisfied", "frustrated", "anxious",
            "worry", "stress", "peace of mind", "confidence", "trust",
            "comfortable", "uncomfortable", "enjoy", "love", "hate",
            "fear", "excited", "bored", "overwhelmed"
        ]
        
        # Check for indicators in the statement
        for indicator in functional_indicators:
            if indicator in statement_lower:
                job_types.append("functional")
                break
                
        for indicator in social_indicators:
            if indicator in statement_lower:
                job_types.append("social")
                break
                
        for indicator in emotional_indicators:
            if indicator in statement_lower:
                job_types.append("emotional")
                break
        
        # If no types were identified, default to functional
        if not job_types:
            job_types.append("functional")
        
        return job_types
    
    def _combine_similar_jobs(self, jobs):
        """
        Combine similar jobs and increment their frequencies.
        
        Args:
            jobs (list): List of extracted jobs
            
        Returns:
            list: List of combined jobs with updated frequencies
        """
        # In a real system, this would use more sophisticated text similarity
        # For this demo, we'll use a simple approach based on statement similarity
        
        combined_jobs = []
        statements_added = set()
        
        for job in jobs:
            # Normalize the statement to check for duplicates
            normalized_statement = self._normalize_statement(job["statement"])
            
            # Check if a similar statement already exists
            if normalized_statement in statements_added:
                # Find the existing job and update its frequency
                for existing_job in combined_jobs:
                    if self._normalize_statement(existing_job["statement"]) == normalized_statement:
                        existing_job["frequency"] += 1
                        break
            else:
                # Add the new job
                combined_jobs.append(job)
                statements_added.add(normalized_statement)
        
        return combined_jobs
    
    def _normalize_statement(self, statement):
        """
        Normalize a statement for comparison.
        
        Args:
            statement (str): The statement to normalize
            
        Returns:
            str: Normalized statement
        """
        # Remove punctuation and convert to lowercase
        normalized = re.sub(r'[^\w\s]', '', statement.lower())
        
        # Remove stop words (a simplified version)
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
                      'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
                      'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
                      'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                      'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                      'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                      'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                      'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                      'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                      'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
                      'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
                      'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                      'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'}
        
        words = normalized.split()
        filtered_words = [word for word in words if word not in stop_words]
        
        return ' '.join(filtered_words)
    
    def _cluster_into_themes(self, jobs):
        """
        Cluster jobs into themes using TF-IDF and K-means.
        
        Args:
            jobs (list): List of jobs to cluster
            
        Returns:
            list: List of themes with their associated jobs
        """
        if not jobs:
            return []
        
        # Extract statements
        statements = [job["statement"] for job in jobs]
        
        # If we have very few statements, just return one theme with all jobs
        if len(statements) < 3:
            return [{
                "name": "Primary Theme",
                "description": "Main theme identified from limited data",
                "jobs": jobs
            }]
        
        # Vectorize the statements
        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(statements)
        
        # Determine the number of clusters (themes)
        # In a real system, this would be determined more intelligently
        n_clusters = min(5, len(statements) // 2)
        n_clusters = max(2, n_clusters)  # At least 2 clusters
        
        # Cluster the statements
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Define stop words here
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
                      'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
                      'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
                      'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                      'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                      'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                      'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                      'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                      'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                      'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
                      'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
                      'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                      'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'}
        
        # Group jobs by cluster
        themes = []
        for i in range(n_clusters):
            theme_jobs = [jobs[j] for j in range(len(jobs)) if clusters[j] == i]
            
            if theme_jobs:
                # Extract keywords for theme naming
                theme_statements = [job["statement"] for job in theme_jobs]
                theme_text = " ".join(theme_statements)
                
                # Simple keyword extraction for theme naming
                words = theme_text.split()
                word_freq = Counter(words)
                common_words = [word for word, count in word_freq.most_common(3) 
                               if len(word) > 3 and word.lower() not in stop_words]
                
                theme_name = " ".join(common_words).title() if common_words else f"Theme {i+1}"
                
                themes.append({
                    "name": theme_name,
                    "description": self._generate_theme_description(theme_jobs),
                    "jobs": theme_jobs,
                    "job_count": len(theme_jobs),
                    "total_frequency": sum(job["frequency"] for job in theme_jobs)
                })
        
        return themes
    
    def _generate_theme_description(self, jobs):
        """
        Generate a description for a theme based on its jobs.
        
        Args:
            jobs (list): List of jobs in the theme
            
        Returns:
            str: Theme description
        """
        # Extract common elements from the jobs
        job_types = Counter([job["type"] for job in jobs])
        most_common_type = job_types.most_common(1)[0][0] if job_types else "functional"
        
        # Get high frequency jobs
        sorted_jobs = sorted(jobs, key=lambda x: x["frequency"], reverse=True)
        top_jobs = sorted_jobs[:3]  # Top 3 jobs
        
        # Create description
        if most_common_type == "functional":
            prefix = "Helping users to"
        elif most_common_type == "social":
            prefix = "Enabling users to be seen as"
        else:  # emotional
            prefix = "Making users feel"
        
        examples = "; ".join([f'"{job["statement"]}"' for job in top_jobs])
        
        return f"{prefix} accomplish their goals. Examples include: {examples}"
    
    def _rank_themes(self, themes):
        """
        Rank themes by total frequency.
        
        Args:
            themes (list): List of themes to rank
            
        Returns:
            list: Ranked themes
        """
        return sorted(themes, key=lambda x: x["total_frequency"], reverse=True)
    
    def _filter_jobs_by_type(self, jobs, job_type):
        """
        Filter jobs by type and rank them by frequency.
        
        Args:
            jobs (list): List of all jobs
            job_type (str): Type of jobs to filter for ("functional", "social", "emotional")
            
        Returns:
            list: Filtered and ranked jobs
        """
        filtered_jobs = [job for job in jobs if job["type"] == job_type]
        ranked_jobs = sorted(filtered_jobs, key=lambda x: x["frequency"], reverse=True)
        
        return ranked_jobs
    
    def _assess_reliability(self, research_data):
        """
        Assess the reliability of the analysis based on data completeness.
        
        Args:
            research_data (dict): The research data
            
        Returns:
            dict: Reliability assessment
        """
        sources = research_data.get("sources", [])
        entries = research_data.get("research_data", [])
        
        # Count entries per source to check for triangulation
        source_counts = Counter()
        for entry in entries:
            source_counts[entry.get("source", "Unknown")] += 1
        
        # Check for patterns across sources
        has_triangulation = len(source_counts) >= 2 and all(count >= 2 for count in source_counts.values())
        
        # Determine reliability level
        if len(sources) >= 3 and len(entries) >= 15 and has_triangulation:
            reliability_level = "high"
        elif len(sources) >= 2 and len(entries) >= 10:
            reliability_level = "medium"
        else:
            reliability_level = "low"
            
        return {
            "level": reliability_level,
            "factors": {
                "source_count": len(sources),
                "data_point_count": len(entries),
                "has_triangulation": has_triangulation
            },
            "description": self._get_reliability_description(reliability_level)
        }
    
    def _get_reliability_description(self, level):
        """
        Get a description for the reliability level.
        
        Args:
            level (str): Reliability level
            
        Returns:
            str: Description of the reliability level
        """
        if level == "high":
            return "The analysis is based on sufficient data from multiple sources with clear patterns."
        elif level == "medium":
            return "The analysis is based on a moderate amount of data. Some patterns are visible but more data would strengthen the conclusions."
        else:
            return "The analysis is based on limited data. The findings should be considered preliminary and require further validation." 