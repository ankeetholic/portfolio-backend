from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, ResearchViewSet, ExperienceViewSet, 
    EducationViewSet, SkillViewSet, ContactMessageCreateView,
    ChatAPIView
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'research', ResearchViewSet)
router.register(r'experience', ExperienceViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    path('chat/', ChatAPIView.as_view(), name='chat'),
]
