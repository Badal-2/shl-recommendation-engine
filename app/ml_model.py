"""
AI/ML Recommendation Engine
Uses TF-IDF and Cosine Similarity to match job roles with assessments
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Assessment

class RecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        self.assessment_vectors = None
        self.assessments_data = []
    
    def train(self, db: Session):
        """
        Train the recommendation model
        Combines test descriptions and skills into feature vectors
        """
        print("🤖 Training recommendation model...")
        
        # Fetch all assessments from database
        assessments = db.query(Assessment).all()
        
        if not assessments:
            raise ValueError("No assessments found in database. Please seed data first.")
        
        # Prepare training data
        self.assessments_data = []
        texts = []
        
        for assessment in assessments:
            # Combine all relevant text fields for better matching
            combined_text = f"{assessment.test_name} {assessment.test_description} {assessment.skills_assessed} {assessment.category}"
            texts.append(combined_text)
            
            self.assessments_data.append({
                'id': assessment.id,
                'test_name': assessment.test_name,
                'test_description': assessment.test_description,
                'category': assessment.category,
                'skills_assessed': assessment.skills_assessed,
                'difficulty_level': assessment.difficulty_level,
                'duration_minutes': assessment.duration_minutes
            })
        
        # Create TF-IDF vectors
        self.assessment_vectors = self.vectorizer.fit_transform(texts)
        
        print(f"✅ Model trained with {len(self.assessments_data)} assessments!")
        return self
    
    def recommend(self, job_role: str, top_k: int = 5) -> List[Dict]:
        """
        Recommend top K assessments for a given job role
        
        Args:
            job_role: Job title or description
            top_k: Number of recommendations to return
        
        Returns:
            List of recommended assessments with confidence scores
        """
        if self.assessment_vectors is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Convert job role to vector
        job_vector = self.vectorizer.transform([job_role])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(job_vector, self.assessment_vectors)[0]
        
        # Get top K indices
        top_indices = np.argsort(similarity_scores)[::-1][:top_k]
        
        # Prepare recommendations
        recommendations = []
        for idx in top_indices:
            score = float(similarity_scores[idx])
            
            # Only include if similarity score > 0
            if score > 0:
                assessment = self.assessments_data[idx].copy()
                assessment['confidence_score'] = round(score * 100, 2)  # Convert to percentage
                assessment['relevance'] = self._get_relevance_label(score)
                recommendations.append(assessment)
        
        # If no matches found, return top general assessments
        if not recommendations:
            recommendations = self._get_default_recommendations(top_k)
        
        return recommendations
    
    def _get_relevance_label(self, score: float) -> str:
        """Convert similarity score to relevance label"""
        if score >= 0.5:
            return "High"
        elif score >= 0.3:
            return "Medium"
        else:
            return "Low"
    
    def _get_default_recommendations(self, top_k: int) -> List[Dict]:
        """Return default recommendations when no match found"""
        # Return most common assessments
        defaults = [
            "Logical Reasoning Test",
            "Problem Solving Assessment",
            "Verbal Reasoning Test",
            "Numerical Reasoning Assessment",
            "Communication Skills Assessment"
        ]
        
        recommendations = []
        for assessment in self.assessments_data[:top_k]:
            if assessment['test_name'] in defaults:
                assessment_copy = assessment.copy()
                assessment_copy['confidence_score'] = 50.0
                assessment_copy['relevance'] = "Medium"
                recommendations.append(assessment_copy)
        
        return recommendations[:top_k]
    
    def get_model_info(self) -> Dict:
        """Return model information and statistics"""
        return {
            "model_type": "TF-IDF + Cosine Similarity",
            "total_assessments": len(self.assessments_data),
            "feature_dimensions": self.assessment_vectors.shape[1] if self.assessment_vectors is not None else 0,
            "trained": self.assessment_vectors is not None
        }


# Global model instance
recommendation_engine = RecommendationEngine() 
