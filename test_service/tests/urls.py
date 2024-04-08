from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, QuestionViewSet, AnswerViewSet, TestAnalyticsView, UserAnswerViewSet

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'user-answers', UserAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tests/<int:test_id>/analytics/', TestAnalyticsView.as_view(), name='test-analytics'),
]