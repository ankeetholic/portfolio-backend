from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Research, Experience, Education, Skill, ContactMessage
from .serializers import (
    ProjectSerializer, ResearchSerializer, ExperienceSerializer, 
    EducationSerializer, SkillSerializer, ContactMessageSerializer
)

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

class ResearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Research.objects.all().order_by('-created_at')
    serializer_class = ResearchSerializer
    lookup_field = 'slug'

class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all().order_by('-start_date')
    serializer_class = ExperienceSerializer

class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all().order_by('-start_date')
    serializer_class = EducationSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

import os
import google.generativeai as genai
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Force load .env explicitly to ensure the API keys are picked up
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Build context directly from the SQLite database
        skills = ", ".join([s.name for s in Skill.objects.all()])
        projects = "\n".join([f"- {p.title}: {p.description[:150]}..." for p in Project.objects.all()[:3]])
        edu = "\n".join([f"- {e.degree} from {e.institution}" for e in Education.objects.all()])
        
        system_prompt = f"""You are Ankit's AI Assistant on his portfolio website.
Answer the user's questions about Ankit Adhikari in a friendly, professional tone. 
Keep your answers very concise and conversational (1-3 sentences maximum). Do not invent information.
If you don't know the answer based on the provided data, just say you don't have that information.
Here is Ankit's data:
Skills: {skills}
Education: {edu}
Projects: {projects}
"""
        
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            # --- REALISTIC FALLBACK RESPONSES IF KEY IS MISSING ---
            msg = user_message.lower()
            if "project" in msg or "build" in msg or "work" in msg:
                fallback = f"Ankit has built some incredible projects! For example, {Project.objects.first().title}." if Project.objects.exists() else "Ankit has built several full-stack applications."
            elif "skill" in msg or "tech" in msg or "know" in msg:
                fallback = f"Ankit's technical expertise is vast. His core skills include {skills[:100]} and many other modern frameworks!"
            elif "education" in msg or "study" in msg or "degree" in msg:
                fallback = f"Ankit studied and earned a {Education.objects.first().degree} from {Education.objects.first().institution}." if Education.objects.exists() else "Ankit has a strong educational background in software engineering."
            elif "contact" in msg or "reach" in msg or "email" in msg:
                fallback = "You can easily reach Ankit via his LinkedIn or GitHub links provided at the top and bottom of the portfolio!"
            else:
                fallback = "Hello! I am Ankit's AI assistant. I can tell you about his programming skills, featured projects, and educational background. What would you like to know?"

            return Response({"answer": fallback}, status=200)

        # Configure Gemini
        genai.configure(api_key=api_key)
        
        try:
            # Using Gemini 2.5 Flash-Lite
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=system_prompt
            )
            
            response = model.generate_content(user_message)
            answer = response.text.strip()
            
            return Response({"answer": answer})
        except Exception as e:
            print("Error connecting to Gemini API:", e)
            return Response(
                {"answer": "I'm temporarily unable to connect to my AI brain (Google Gemini). Please try again later."}, 
                status=503
            )
