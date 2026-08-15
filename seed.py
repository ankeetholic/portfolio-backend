import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, Research, Experience, Education, Skill

def seed():
    print("Seeding database...")
    
    # Skills
    skills_data = [
        ("Python", "Programming"), ("TypeScript", "Programming"), ("JavaScript", "Programming"), ("SQL", "Programming"),
        ("React", "Frontend"), ("Next.js", "Frontend"), ("Tailwind CSS", "Frontend"),
        ("Django", "Backend"), ("FastAPI", "Backend"), ("Django REST Framework", "Backend"),
        ("PyTorch", "AI / ML"), ("TensorFlow", "AI / ML"), ("Transformers", "AI / ML"), ("Computer Vision", "AI / ML"),
        ("PostgreSQL", "Databases")
    ]
    for name, cat in skills_data:
        Skill.objects.get_or_create(name=name, defaults={'category': cat})
        
    # Education
    Education.objects.get_or_create(
        degree='Bachelor of Software Engineering',
        institution='Gandaki College of Engineering and Science (GCES)',
        defaults={
            'location': 'Pokhara, Nepal',
            'start_date': date(2022, 1, 1),
            'end_date': date(2026, 12, 31),
            'description': 'Focusing on software development, AI/ML, deep learning, and computer vision.'
        }
    )

    # Experience
    Experience.objects.get_or_create(
        title='Research Intern \u2013 AI Research & R&D',
        company='XTEN IT Technologies Pvt. Ltd.',
        defaults={
            'location': 'Pokhara, Nepal',
            'start_date': date(2023, 6, 1),
            'current': True,
            'description': 'Working on AI/ML research, specifically image captioning, explainable AI, model robustness analysis, and Vision-Language Model evaluation.'
        }
    )

    # Projects
    Project.objects.get_or_create(
        slug='image-steganography',
        defaults={
            'title': 'Image Steganography',
            'description': 'Deep learning based image steganography system using a fully convolutional architecture.',
            'technologies': 'Python, PyTorch, Computer Vision, CNN',
            'category': 'Deep Learning',
            'github_url': 'https://github.com/ankeetholic',
            'featured': True
        }
    )
    
    Project.objects.get_or_create(
        slug='futsal-booking-system',
        defaults={
            'title': 'Futsal Booking System',
            'description': 'Full-stack futsal booking application to schedule and manage matches.',
            'technologies': 'React, FastAPI, SQL, Tailwind CSS',
            'category': 'Full-Stack',
            'github_url': 'https://github.com/ankeetholic',
            'featured': True
        }
    )
    
    # Research
    Research.objects.get_or_create(
        slug='image-captioning-transformer',
        defaults={
            'title': 'Transformer-based Image Captioning',
            'description': 'Transformer-based image captioning research/project using CNN/Transformer architectures and Flickr datasets.',
            'methodology': 'CNN + Transformer',
            'dataset': 'Flickr8k',
            'technologies': 'Transformers, NLP, Computer Vision',
            'publication_status': 'In Progress'
        }
    )

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
