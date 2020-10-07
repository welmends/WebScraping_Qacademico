from django.urls import path, include
from rest_framework import routers
from qacademico.aluno.views import alunos

urlpatterns = [
    # api/payment/payments
    path('aluno', alunos.as_view()),
]