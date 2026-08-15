import os
import requests
import json
from django.conf import settings
from portfolio.models import Project, Research, Experience, Education, Skill

def get_portfolio_context(query):
    query_lower = query.lower()
    
    # Very basic search for grounding
    projects = Project.objects.all()
    research = Research.objects.all()
    experience = Experience.objects.all()
    education = Education.objects.all()
    skills = Skill.objects.all()
    
    context_parts = []
    
    if "project" in query_lower or any(p.title.lower() in query_lower for p in projects):
        proj_texts = [f"{p.title}: {p.description} (Technologies: {p.technologies})" for p in projects[:5]]
        if proj_texts:
            context_parts.append("Projects:\n" + "\n".join(proj_texts))
            
    if "research" in query_lower or "paper" in query_lower or any(r.title.lower() in query_lower for r in research):
        res_texts = [f"{r.title}: {r.description}" for r in research[:5]]
        if res_texts:
            context_parts.append("Research:\n" + "\n".join(res_texts))
            
    if "experience" in query_lower or "work" in query_lower or "intern" in query_lower:
        exp_texts = [f"{e.title} at {e.company} ({e.start_date} to {'Present' if e.current else e.end_date}): {e.description}" for e in experience]
        if exp_texts:
            context_parts.append("Experience:\n" + "\n".join(exp_texts))
            
    if "education" in query_lower or "degree" in query_lower or "college" in query_lower:
        edu_texts = [f"{e.degree} at {e.institution}" for e in education]
        if edu_texts:
            context_parts.append("Education:\n" + "\n".join(edu_texts))
            
    if "skill" in query_lower or "know" in query_lower or "tech" in query_lower:
        skill_texts = [s.name for s in skills]
        if skill_texts:
            context_parts.append(f"Skills: {', '.join(skill_texts)}")

    # If nothing matched specifically, provide a general summary
    if not context_parts:
        proj_summary = ", ".join([p.title for p in projects[:3]])
        exp_summary = ", ".join([e.title for e in experience[:2]])
        context_parts.append(f"Ankit is a Software Engineer. Recent projects: {proj_summary}. Experience: {exp_summary}.")
        
    return "\n\n".join(context_parts)


def generate_chat_response(message):
    hf_token = os.environ.get("HF_TOKEN")
    hf_model = os.environ.get("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
    
    if not hf_token or hf_token == "your_hugging_face_token_here":
        return {
            "answer": "I'm currently running in local mode without a Hugging Face API token configured. I'm unable to answer right now.",
            "sources": []
        }
        
    context = get_portfolio_context(message)
    
    system_prompt = f"""You are Ask Ankit AI, the official AI assistant for Ankit Adhikari's personal portfolio.
Your job is to answer questions about Ankit.
Use ONLY the information provided in the portfolio context below.
Do not invent projects, technologies, employment, publications, awards, education, achievements, or personal information.
If the answer is not available in the provided context, clearly say that you do not have that information.
Never pretend to know something that is not present in the portfolio data.
Be concise, professional, friendly, and factual.

PORTFOLIO CONTEXT:
{context}
"""

    prompt = f"<s>[INST] {system_prompt}\n\nUser Question: {message} [/INST]"
    
    api_url = f"https://api-inference.huggingface.co/models/{hf_model}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.3,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get("generated_text", "").strip()
                return {
                    "answer": answer,
                    "sources": ["portfolio_database"]
                }
        elif response.status_code == 503:
             return {
                "answer": "The AI model is currently loading. Please try asking your question again in a few seconds.",
                "sources": []
            }
        else:
            print(f"HF API Error: {response.status_code} - {response.text}")
            return {
                "answer": "I'm temporarily unable to process your request due to an AI service error. Please try again later.",
                "sources": []
            }
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
        return {
            "answer": "I'm temporarily unable to answer right now due to a network error. Please try again later.",
            "sources": []
        }
