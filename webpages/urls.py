from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('histogram/', views.histogram, name='histogram'),
    path('boxplot/', views.boxplot, name='boxplot'),
    path('density/', views.density, name='density'),
    path('count/', views.count, name='count'),
    path('pie/', views.pie, name='pie'),
    path('pairplot/', views.pairplot, name='pairplot'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('scatterplot/', views.scatterplot, name='scatterplot'),
    path('lineplot/', views.lineplot, name='lineplots'),
    path('sample/', views.sample, name='sample'),
    path('midpair/', views.midpair, name='midpair'),
    path('midheat/', views.midheat, name='midheat'),
    path('midscatter/', views.midscatter, name='midscatter'),
    path('midline/', views.midline, name='midline'),
    path('midhistogram/', views.midhistogram, name='midhistogram'),
    path('midboxplot/', views.midboxplot, name='midboxplot'),
    path('middensity/', views.middensity, name='middensity'),
    path('midcount/', views.midcount, name='midcount'),
    path('midpie/', views.midpie, name='midpie'),
]
