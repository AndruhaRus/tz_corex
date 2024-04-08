from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test, Question, Answer, UserAnswer
from .serializers import TestSerializer, QuestionSerializer, AnswerSerializer, UserAnswerSerializer


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer



class TestAnalyticsView(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
            # Получаем общее количество прохождений теста
            total_attempts = test.questions.count()

            # Вычисляем процент успешного прохождения
            correct_answers_count = 0
            for question in test.questions.all():
                correct_answers_count += question.answers.filter(is_correct=True).count()
            success_rate = (correct_answers_count / total_attempts) * 100 if total_attempts > 0 else 0

            # Находим самый сложный вопрос (вопрос с наименьшим процентом правильных ответов)
            hardest_question = None
            lowest_success_rate = 100
            for question in test.questions.all():
                question_total_attempts = question.answers.count()
                if question_total_attempts > 0:
                    question_correct_answers = question.answers.filter(is_correct=True).count()
                    question_success_rate = (question_correct_answers / question_total_attempts) * 100
                    if question_success_rate < lowest_success_rate:
                        hardest_question = question
                        lowest_success_rate = question_success_rate

            # Составляем JSON ответ с аналитикой
            analytics_data = {
                "total_attempts": total_attempts,
                "success_rate": success_rate,
                "hardest_question": {
                    "text": hardest_question.text if hardest_question else None,
                    "success_rate": lowest_success_rate
                }
            }
            return Response(analytics_data, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({"error": "Test not found."}, status=status.HTTP_404_NOT_FOUND)