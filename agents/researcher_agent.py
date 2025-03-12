import logging
import random
from collections import Counter

logger = logging.getLogger(__name__)

class ResearcherAgent:
    """
    The Researcher Agent generates research plans when there is insufficient 
    data to perform a reliable JTBD analysis.
    """
    
    def __init__(self):
        """Initialize the Researcher Agent."""
        pass
    
    def generate_research_plan(self, topic, existing_analysis=None):
        """
        Generate a research plan for the given topic.
        
        Args:
            topic (str): The topic to generate a research plan for
            existing_analysis (dict, optional): Existing partial analysis
            
        Returns:
            dict: Research plan with interview questions and survey questions
        """
        logger.info(f"Generating research plan for topic: {topic}")
        
        # Determine research goals based on existing analysis
        research_goals = self._determine_research_goals(topic, existing_analysis)
        
        # Generate interview questions
        interview_questions = self._generate_interview_questions(topic, research_goals)
        
        # Generate survey questions
        survey_questions = self._generate_survey_questions(topic, research_goals)
        
        # Create the research plan
        research_plan = {
            "topic": topic,
            "research_goals": research_goals,
            "interview_questions": interview_questions,
            "survey_questions": survey_questions,
            "recommended_methods": self._recommend_research_methods(topic, existing_analysis),
            "sample_size_recommendations": self._recommend_sample_sizes(existing_analysis)
        }
        
        return research_plan
    
    def _determine_research_goals(self, topic, existing_analysis):
        """
        Determine the goals for the research plan.
        
        Args:
            topic (str): The topic for the research
            existing_analysis (dict, optional): Existing partial analysis
            
        Returns:
            list: Research goals
        """
        goals = []
        
        # Base goals that apply to any research project
        base_goals = [
            f"Identify the key functional jobs users are trying to accomplish related to {topic}",
            f"Understand the emotional needs users have when engaging with {topic}",
            f"Discover the social context and implications of {topic} for users"
        ]
        
        goals.extend(base_goals)
        
        # If we have existing analysis, add specific goals to address gaps
        if existing_analysis:
            # Check which job types have less data
            job_types = ["functional", "social", "emotional"]
            
            for job_type in job_types:
                jobs = existing_analysis.get(f"{job_type}_jobs", [])
                
                if not jobs or len(jobs) < 3:
                    goals.append(f"Expand understanding of {job_type} jobs related to {topic}")
            
            # Check reliability if available
            reliability = existing_analysis.get("reliability", {})
            reliability_level = reliability.get("level", "low")
            
            if reliability_level == "low":
                goals.append(f"Validate preliminary findings by gathering more diverse data")
            
            # Look for additional goals based on themes
            themes = existing_analysis.get("themes", [])
            if themes:
                # Find the theme with the fewest jobs
                min_jobs_theme = min(themes, key=lambda x: x.get("job_count", 0))
                theme_name = min_jobs_theme.get("name", "")
                
                if theme_name:
                    goals.append(f"Gather more data about the '{theme_name}' theme to strengthen analysis")
        
        # Add some specific goals based on the topic
        topic_specific_goals = [
            f"Identify the main pain points users experience with current {topic} solutions",
            f"Understand user expectations and desired outcomes when using {topic}",
            f"Discover unmet needs in the {topic} space that could inform innovation"
        ]
        
        goals.extend(topic_specific_goals)
        
        return goals
    
    def _generate_interview_questions(self, topic, research_goals):
        """
        Generate interview questions based on the topic and research goals.
        
        Args:
            topic (str): The topic for the research
            research_goals (list): The research goals
            
        Returns:
            list: Interview questions
        """
        # General JTBD interview questions
        general_questions = [
            f"Can you tell me about the last time you used/experienced {topic}?",
            f"What were you trying to accomplish when you used {topic}?",
            f"What prompted you to look for a solution like {topic}?",
            f"What alternatives did you consider before choosing {topic}?",
            f"What does a successful outcome look like when you use {topic}?",
            f"What frustrations or challenges do you face when using {topic}?",
            f"How do you measure success when using {topic}?",
            f"How has using {topic} changed your routine or process?",
            f"If {topic} wasn't available, what would you do instead?",
            f"What improvement to {topic} would make the biggest difference for you?"
        ]
        
        # Functional job questions
        functional_questions = [
            f"What specific tasks are you trying to complete with {topic}?",
            f"How do you know when {topic} has successfully helped you accomplish your goal?",
            f"What features or capabilities are most important to you when using {topic}?",
            f"What steps or processes related to {topic} take too much time or effort?",
            f"What problems does {topic} solve for you?"
        ]
        
        # Emotional job questions
        emotional_questions = [
            f"How do you feel before, during, and after using {topic}?",
            f"What worries or concerns do you have when using {topic}?",
            f"What aspects of {topic} give you confidence or peace of mind?",
            f"What emotions would you associate with your experience using {topic}?",
            f"What would make you feel more satisfied with your {topic} experience?"
        ]
        
        # Social job questions
        social_questions = [
            f"How does using {topic} impact how others perceive you?",
            f"Do you discuss your use of {topic} with others? What do you share?",
            f"How important is it that others know you use {topic}?",
            f"Has using {topic} affected your relationships or social interactions?",
            f"Are there social expectations around using {topic} in your community or workplace?"
        ]
        
        # Combine and select questions
        all_questions = general_questions + functional_questions + emotional_questions + social_questions
        
        # Select a subset of questions (about 10-15)
        selected_count = min(15, len(all_questions))
        selected_questions = random.sample(all_questions, selected_count)
        
        # Add some goal-specific questions
        for goal in research_goals[:2]:  # Just use the first couple of goals
            goal_lower = goal.lower()
            
            if "functional" in goal_lower:
                selected_questions.extend(random.sample(functional_questions, 2))
            elif "emotional" in goal_lower:
                selected_questions.extend(random.sample(emotional_questions, 2))
            elif "social" in goal_lower:
                selected_questions.extend(random.sample(social_questions, 2))
        
        # Remove duplicates and sort
        unique_questions = list(dict.fromkeys(selected_questions))
        
        return unique_questions
    
    def _generate_survey_questions(self, topic, research_goals):
        """
        Generate survey questions based on the topic and research goals.
        
        Args:
            topic (str): The topic for the research
            research_goals (list): The research goals
            
        Returns:
            list: Survey questions
        """
        survey_questions = []
        
        # Multiple choice questions
        multiple_choice_questions = [
            {
                "question": f"How often do you use {topic}?",
                "type": "multiple_choice",
                "options": ["Daily", "Weekly", "Monthly", "Rarely", "Never"]
            },
            {
                "question": f"What is your primary reason for using {topic}?",
                "type": "multiple_choice",
                "options": ["To save time", "To save money", "For convenience", "For quality", "Other (please specify)"]
            },
            {
                "question": f"How satisfied are you with your current {topic} solution?",
                "type": "scale",
                "options": ["Very dissatisfied", "Somewhat dissatisfied", "Neutral", "Somewhat satisfied", "Very satisfied"]
            },
            {
                "question": f"Which of the following best describes how you feel when using {topic}?",
                "type": "multiple_choice",
                "options": ["Frustrated", "Anxious", "Neutral", "Satisfied", "Delighted"]
            },
            {
                "question": f"How likely are you to recommend {topic} to a friend or colleague?",
                "type": "scale",
                "options": ["0 - Not at all likely", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10 - Extremely likely"]
            }
        ]
        
        # Likert scale questions
        likert_questions = [
            {
                "question": f"{topic} helps me accomplish my goals efficiently.",
                "type": "likert",
                "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
            },
            {
                "question": f"Using {topic} makes me feel confident.",
                "type": "likert",
                "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
            },
            {
                "question": f"Others respect me for my choice to use {topic}.",
                "type": "likert",
                "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
            },
            {
                "question": f"I often feel frustrated when using {topic}.",
                "type": "likert",
                "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
            },
            {
                "question": f"Using {topic} saves me time compared to alternatives.",
                "type": "likert",
                "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
            }
        ]
        
        # Open-ended questions
        open_ended_questions = [
            {
                "question": f"What are you trying to accomplish when you use {topic}?",
                "type": "open_ended"
            },
            {
                "question": f"What is the most frustrating aspect of using {topic}?",
                "type": "open_ended"
            },
            {
                "question": f"How would you describe your ideal experience with {topic}?",
                "type": "open_ended"
            },
            {
                "question": f"What would make you switch from {topic} to an alternative?",
                "type": "open_ended"
            },
            {
                "question": f"What other solutions have you tried instead of {topic}, and why did you choose {topic}?",
                "type": "open_ended"
            }
        ]
        
        # Combine all questions and add them to the survey
        survey_questions.extend(multiple_choice_questions)
        survey_questions.extend(likert_questions)
        survey_questions.extend(open_ended_questions)
        
        # Add goal-specific questions
        for goal in research_goals[:3]:  # Just use a few goals
            goal_lower = goal.lower()
            
            if "functional" in goal_lower:
                survey_questions.append({
                    "question": f"What tasks do you most commonly use {topic} for?",
                    "type": "open_ended"
                })
            elif "emotional" in goal_lower:
                survey_questions.append({
                    "question": f"How does using {topic} make you feel?",
                    "type": "open_ended"
                })
            elif "social" in goal_lower:
                survey_questions.append({
                    "question": f"How important is it that others know you use {topic}?",
                    "type": "scale",
                    "options": ["Not at all important", "Slightly important", "Moderately important", "Very important", "Extremely important"]
                })
        
        return survey_questions
    
    def _recommend_research_methods(self, topic, existing_analysis):
        """
        Recommend research methods based on the topic and existing analysis.
        
        Args:
            topic (str): The topic for the research
            existing_analysis (dict, optional): Existing partial analysis
            
        Returns:
            list: Recommended research methods
        """
        # Basic research methods
        methods = [
            {
                "method": "User Interviews",
                "description": f"One-on-one interviews with current or potential users of {topic} to deeply understand their needs, motivations, and pain points.",
                "priority": "High"
            },
            {
                "method": "Surveys",
                "description": f"Quantitative data collection to understand patterns across a larger user base for {topic}.",
                "priority": "Medium"
            },
            {
                "method": "Contextual Inquiry",
                "description": f"Observing users in their natural environment while they interact with {topic} to identify unspoken needs and workarounds.",
                "priority": "Medium"
            },
            {
                "method": "Diary Studies",
                "description": f"Having users document their experiences with {topic} over time to capture real-time feedback and evolving needs.",
                "priority": "Low"
            }
        ]
        
        # If we have existing analysis, adjust priorities
        if existing_analysis:
            reliability = existing_analysis.get("reliability", {})
            level = reliability.get("level", "low")
            
            if level == "low":
                # Recommend more in-depth methods
                for method in methods:
                    if method["method"] == "User Interviews" or method["method"] == "Contextual Inquiry":
                        method["priority"] = "High"
                
                # Add focus groups as a method
                methods.append({
                    "method": "Focus Groups",
                    "description": f"Group discussions with 6-8 users to explore collective opinions and experiences with {topic}.",
                    "priority": "Medium"
                })
            
            # Check which job types need more focus
            job_counts = {
                "functional": len(existing_analysis.get("functional_jobs", [])),
                "social": len(existing_analysis.get("social_jobs", [])),
                "emotional": len(existing_analysis.get("emotional_jobs", []))
            }
            
            min_job_type = min(job_counts.items(), key=lambda x: x[1])
            
            if min_job_type[0] == "social":
                methods.append({
                    "method": "Social Media Analysis",
                    "description": f"Analyzing how users discuss {topic} on social platforms to understand social context and influence.",
                    "priority": "High"
                })
            elif min_job_type[0] == "emotional":
                methods.append({
                    "method": "Sentiment Analysis",
                    "description": f"Analyzing user reviews and feedback to understand emotional responses to {topic}.",
                    "priority": "High"
                })
        
        return methods
    
    def _recommend_sample_sizes(self, existing_analysis):
        """
        Recommend sample sizes for different research methods.
        
        Args:
            existing_analysis (dict, optional): Existing partial analysis
            
        Returns:
            dict: Recommended sample sizes
        """
        # Base recommendations
        recommendations = {
            "interviews": {
                "min": 8,
                "ideal": 12,
                "justification": "8-12 interviews typically reveal most major patterns in qualitative research."
            },
            "surveys": {
                "min": 100,
                "ideal": 300,
                "justification": "A sample of 300+ provides good statistical power for most analyses."
            },
            "contextual_inquiry": {
                "min": 4,
                "ideal": 6,
                "justification": "4-6 contextual inquiries balance depth with resource constraints."
            }
        }
        
        # Adjust based on existing analysis if available
        if existing_analysis:
            reliability = existing_analysis.get("reliability", {})
            factors = reliability.get("factors", {})
            
            current_sources = factors.get("source_count", 0)
            current_data_points = factors.get("data_point_count", 0)
            
            # If we already have some data, adjust the recommendations
            if current_sources > 0:
                # Reduce interview recommendation based on existing sources
                recommendations["interviews"]["min"] = max(5, 8 - current_sources)
                recommendations["interviews"]["ideal"] = max(8, 12 - current_sources)
                recommendations["interviews"]["justification"] += f" Currently have {current_sources} sources."
            
            if current_data_points > 0:
                # Reduce survey recommendation based on existing data points
                recommendations["surveys"]["min"] = max(50, 100 - current_data_points)
                recommendations["surveys"]["ideal"] = max(150, 300 - current_data_points)
                recommendations["surveys"]["justification"] += f" Currently have {current_data_points} data points."
        
        return recommendations 