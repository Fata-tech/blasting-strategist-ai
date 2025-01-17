import streamlit as st
import pandas as pd
from datetime import datetime
import json

class BlastingBusinessAgent:
    def __init__(self):
        self.knowledge_base = {
            "safety_regulations": [
                "OSHA safety standards for explosives",
                "Storage requirements for explosive materials",
                "Personnel certification requirements",
                "Emergency response protocols",
                "Environmental impact considerations"
            ],
            "cost_factors": [
                "Explosive materials",
                "Equipment depreciation",
                "Labor costs",
                "Safety equipment",
                "Insurance and permits",
                "Environmental compliance"
            ],
            "business_metrics": [
                "Cost per cubic meter",
                "Project completion time",
                "Safety incident rate",
                "Client satisfaction",
                "Environmental compliance score"
            ]
        }
    
    def analyze_project(self, project_data):
        recommendations = []
        risks = []
        opportunities = []
        
        # Analyze costs
        if project_data['budget'] < project_data['estimated_cost']:
            risks.append("Budget constraints may impact project feasibility")
            recommendations.append("Consider cost optimization strategies such as bulk material purchasing")
        
        # Analyze timeline
        if project_data['timeline'] < 30:
            risks.append("Accelerated timeline may impact safety protocols")
            recommendations.append("Implement expedited safety check procedures")
        
        # Analyze scope
        if project_data['blast_volume'] > 10000:
            opportunities.append("Large project scope allows for economies of scale")
            recommendations.append("Consider investing in automated drilling equipment")
        
        return {
            "recommendations": recommendations,
            "risks": risks,
            "opportunities": opportunities
        }
    
    def calculate_roi(self, project_data):
        total_cost = project_data['estimated_cost']
        expected_revenue = project_data['expected_revenue']
        
        roi = ((expected_revenue - total_cost) / total_cost) * 100
        return roi
    
    def generate_safety_checklist(self):
        return [
            "Verify all permits are in place",
            "Conduct pre-blast site survey",
            "Check weather conditions",
            "Verify explosive storage compliance",
            "Ensure all personnel are certified",
            "Review emergency response plan",
            "Set up blast monitoring equipment",
            "Establish exclusion zones",
            "Verify communication systems"
        ]

def main():
    st.title("AI Business Strategist - Blasting Domain")
    st.write("An intelligent assistant for blasting project analysis and recommendations")
    
    st.sidebar.header("Project Parameters")
    
    project_data = {
        "project_name": st.sidebar.text_input("Project Name"),
        "budget": st.sidebar.number_input("Budget ($)", min_value=0, value=100000),
        "estimated_cost": st.sidebar.number_input("Estimated Cost ($)", min_value=0, value=80000),
        "expected_revenue": st.sidebar.number_input("Expected Revenue ($)", min_value=0, value=150000),
        "timeline": st.sidebar.number_input("Project Timeline (days)", min_value=1, value=45),
        "blast_volume": st.sidebar.number_input("Blast Volume (cubic meters)", min_value=0, value=5000)
    }
    
    agent = BlastingBusinessAgent()
    
    if st.button("Analyze Project"):
        st.header("Project Analysis")
        
        analysis = agent.analyze_project(project_data)
        roi = agent.calculate_roi(project_data)
        safety_checklist = agent.generate_safety_checklist()
        
        st.subheader("Financial Analysis")
        st.metric("Projected ROI", f"{roi:.1f}%")
        
        st.subheader("Recommendations")
        for rec in analysis['recommendations']:
            st.write(f"• {rec}")
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Risks")
            for risk in analysis['risks']:
                st.write(f"• {risk}")
        
        with col2:
            st.subheader("Opportunities")
            for opp in analysis['opportunities']:
                st.write(f"• {opp}")
        
        st.subheader("Safety Checklist")
        for item in safety_checklist:
            st.checkbox(item, key=item)
        
        if st.button("Export Analysis"):
            export_data = {
                "project_data": project_data,
                "analysis": analysis,
                "roi": roi,
                "safety_checklist": safety_checklist,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.download_button(
                label="Download Analysis Report",
                data=json.dumps(export_data, indent=2),
                file_name=f"blasting_analysis_{project_data['project_name']}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
