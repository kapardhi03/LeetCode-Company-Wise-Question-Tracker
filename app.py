import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import os
import json
from typing import Dict, List

class LeetCodeTracker:
    def __init__(self):
        self.companies = ['amazon', 'google', 'microsoft', 'meta', 'netflix']
        self.base_url = "https://raw.githubusercontent.com/krishnadey30/LeetCode-Questions-CompanyWise/master/"
        self.progress_file = "progress.json"
        
    def load_progress(self) -> Dict:
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}

    def save_progress(self, progress: Dict):
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f)

    def fetch_company_questions(self, company: str) -> pd.DataFrame:
        file_url = f"{self.base_url}/{company}_alltime.csv"
        try:
            df = pd.read_csv(file_url)
            return df
        except:
            st.error(f"Failed to fetch questions for {company}")
            return pd.DataFrame()

    def create_difficulty_section(self, questions: pd.DataFrame, difficulty: str, 
                                progress: Dict, company: str) -> None:
        filtered = questions[questions['Difficulty'] == difficulty]
        if not filtered.empty:
            st.subheader(f"{difficulty} Problems")
            for _, row in filtered.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"[{row['Title']}]({row['Leetcode Question Link']})")
                with col2:
                    st.write(f"Acceptance: {row['Acceptance']}%")
                with col3:
                    question_key = f"{company}_{row['ID']}"
                    completed = progress.get(question_key, False)
                    if st.checkbox("Completed", value=completed, key=question_key):
                        progress[question_key] = True
                    else:
                        progress[question_key] = False

def main():
    st.set_page_config(page_title="LeetCode Tracker", layout="wide")
    st.title("LeetCode Company-Wise Question Tracker")
    
    tracker = LeetCodeTracker()
    progress = tracker.load_progress()
    
    company = st.sidebar.selectbox(
        "Select Company",
        tracker.companies
    )
    
    questions = tracker.fetch_company_questions(company)
    if not questions.empty:
        total_questions = len(questions)
        completed_questions = sum(1 for key in progress if key.startswith(company) and progress[key])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Completed", completed_questions)
        with col3:
            completion_rate = (completed_questions / total_questions * 100) if total_questions > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        for difficulty in ['Easy', 'Medium', 'Hard']:
            tracker.create_difficulty_section(questions, difficulty, progress, company)
            
        tracker.save_progress(progress)

if __name__ == "__main__":
    main()