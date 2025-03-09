from django.urls import path
from .views import StartGameView, SubmitAnswerView, SelectCategoryView, QuestionDetailView, GameResultView

urlpatterns = [
    path('game/start',
         StartGameView.as_view()),
    path('game/<int:game_id>/round/<int:round_number>/select_category',
         SelectCategoryView.as_view()),
    path('game/<int:game_id>/round/<int:round_number>/question/<int:question_number>',
         QuestionDetailView.as_view()),
    path('game/<int:game_id>/round/<int:round_number>/question/<int:question_number>/submit',
         SubmitAnswerView.as_view()),
    path('game/<int:game_id>/result',
         GameResultView.as_view()),
]