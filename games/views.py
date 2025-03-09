import random
from tabnanny import check

from django.db.models.query_utils import Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from questions.models import Category
from .models import Game,GameRound,GameQuestion
from users.models import User
from questions.models import Question
from .serializers import UserSerializer


#/game/start
class StartGameView(APIView):
    def user_has_other_active_games(self,id):
        user_games = Game.objects.filter(Q(user1__numeric=id) | Q(user2__numeric=id)).filter(status != 'finished')
        if user_games.exists():
            return True
        return False

    def post(self, request):
        """if the user with that id exist and have no other game
        we looking for last game
                if last started game has not started and wait for a user, our user joins the game.
                 if not a new game created"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try :
                user = User.objects.get(id=serializer.data['id'])
            except User.DoesNotExist:
                return Response({'detail' : 'not user with this id'},status=status.HTTP_400_BAD_REQUEST)
            if self.user_has_other_active_games(serializer.data['id']):
                return Response({'detail' : 'this user already have active games'},status=status.HTTP_400_BAD_REQUEST)
            last_game = Game.objects.filter(status = 'pre-started').order_by('created_at').first()
            #join the user to a game
            if last_game:
                last_game.user2 = user
                last_game.status = 'started'
                last_game.save()
                return Response({'detail':'Game started'}, status=status.HTTP_200_OK)
            #create new game
            new_game = Game.objects.create(user1 = user,status = 'pre-started')
            return Response({'detail':'game been created','game_id' : new_game.id }, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#game/{game_id}/round/{round_number}/select_category/{category_name}
class SelectCategoryView(APIView):
            def post(self, request, game_id,category_name):
                try :
                    game = Game.objects.get(id=game_id,status='started')
                except Game.DoesNotExist:
                    return Response({'detail' : 'Game does not exist'}, status=status.HTTP_404_NOT_FOUND)
                if game.status != 'active' :
                    return Response({'detail' : 'game is not active'}, status=status.HTTP_404_NOT_FOUND)
                try :
                    category = Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    return Response({'detail' : 'invalid selected_category'}, status=status.HTTP_404_NOT_FOUND)
                GameRound.objects.create(game = game, category = category,round_number =game.current_round+1)
                game.currrent_round += 1
                game.save()
                return Response({'detail' : 'selected_category been selected'}, status=status.HTTP_200_OK)

#game/{game_id}/round/{round_number}/question/{question_number}
class QuestionDetailView(APIView):
    """see the detail of a gamequestion
    if the question been answered by the first in turn user now the seconde user sees that and start time for that user
    starts.
    if not a new gamequestion object creates and time starts for that user"""
    def get(self,game_id,round_number,question_number):
        try :
            game = Game.objects.get(id=game_id,status = "started")
        except Game.DoesNotExist:
            return Response({'detail' : 'Game does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try :
            round = GameRound.objects.get(game = game,
                                          round_number=round_number)
        except GameRound.DoesNotExist:
            return Response({'detail' : 'Round does not exist'}, status=status.HTTP_404_NOT_FOUND)
        question = GameQuestion.objects.filter(question_number = question_number,
                                           round = round)
        #now the second user submit the answer.
        if question.exists():
            if round.turn == 1:
                question.start_time_for_user1 = timezone.now()
                question.save()
            else:
                question.start_time_for_user2 = timezone.now()
                question.save()
            return Response({'question' : question.text},status = status.HTTP_200_OK)
        else:
            category_releated_questions = Question.objects.filter(category__name = round.selected_category)
            if category_releated_questions.count() > 3:
                random_selected_question = random.choice(category_releated_questions)
            else:
                return Response({'detail' : 'not question in this selected_category'},status=status.HTTP_400_BAD_REQUEST)

        if round.turn == 1:
            question = GameQuestion.objects.create(question_number = question_number,
                                               round = round,
                                               question = random_selected_question,
                                               start_time_for_user1 = timezone.now() )
        else:
            question = GameQuestion.objects.create(question_number = question_number,
                                                   round = round,
                                                   question = random_selected_question,
                                                   start_time_for_user2 = timezone.now())

        return Response({'question' : question.text},
                        status = status.HTTP_200_OK)

#game/{game_id}/round/{round_number}/question/{question_number}/submit
class SubmitAnswerView(APIView):
    def check_end_game(self,round_number,question_number,game):
        # if we in round5 and question3 and turn of user2 it means the game ended after answering the question.
        if round_number == 5 and question_number == 3 and game.turn == 2:
            return True
        return False

    def is_correct_answer(self,question,user_answer):
        """gets the gamequestion object and the answer that user sends to that and check if it is correct"""
        correct_answer = question.question.answers.get(is_correct = True)
        if user_answer == correct_answer:
            return True
        return False

    def post(self,request,game_id,round_number,question_number):
        game = Game.objects.get(id=game_id,status = 'started')
        round = GameRound.objects.get(game = game,
                                      round_number=round_number)
        question = GameQuestion.objects.get(question_number = question_number,
                                            round = round)
        detail_text = str()
        is_ended = self.check_end_game(round_number,question_number,game)
        if round.turn == 1:
            answer_taken_time = timezone.now() - question.start_time_for_user1
            if answer_taken_time.total_seconds() < 30:
                detail_text = 'time been ended'
            else:
                question.user1_answer = request.data.get('answer')
                question.save()
                if self.is_correct_answer(question,question.user1_answer):
                    detail_text = 'correct answer'
                    round.user1_point += 1
                else:
                    detail_text = 'wrong answer'
        else:
            answer_taken_time = timezone.now() - question.start_time_for_user2
            if answer_taken_time.total_seconds() < 30:
                detail_text = 'time has been ended'
            else:
                question = GameQuestion.objects.get(question_number = question_number,
                                                round = round)
                question.user2_answer = request.data.get['answer']
                question.save()
                if self.is_correct_answer(question,question.user2_answer):
                    detail_text = 'correct answer'
                    round.user2_point += 1
                else:
                    detail_text = 'wrong answer'

        if is_ended:
            game.status = 'ended'
            game.end_time = timezone.now()
            game.save()
        return Response({'detail' : detail_text},status=status.HTTP_200_OK)


#game/{game_id}/result
class GameResultView(APIView):
    def get(self,request,game_id):
        try :
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'detail' : 'Game does not exist'}, status=status.HTTP_404_NOT_FOUND)
        game_rounds = GameRound.objects.filter(game = game)
        status = game.status
        total_user1_score = sum(round.user1_score for round in game_rounds)
        total_user2_score = sum(round.user2_score for round in game_rounds) 
        return Response({"status" : status,
                         "user1_score" : total_user1_score,
                         "user2_score" : total_user2_score},
                        status = status.HTTP_200_OK)












