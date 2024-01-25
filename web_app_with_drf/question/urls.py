from django.urls import path
from .views import add_question, QuestionListApiView, update, delete_question, detail_question, \
    AnswerAnyQuestionApiView, AnswerListApiView


urlpatterns = [
    # urls for questions
    path('add_question/', add_question, ),
    path('get_questions/', QuestionListApiView.as_view(), ),
    path('update_question/<int:pk>/', update, ),
    path('delete_question/<int:pk>/', delete_question, ),
    path('detail_question/<int:pk>/', detail_question, ),
    # urls for answers
    path('answer_question/<int:question_id>/', AnswerAnyQuestionApiView.as_view(), ),
    path("answer_list/", AnswerListApiView.as_view(), ),





]

