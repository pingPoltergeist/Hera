from django.urls import path
from . import views

urlpatterns = [

    path('movie-collection-list/', views.MovieCollectionList.as_view()),
    path('movie-collection/<str:movie_collection_id>/', views.MovieCollectionDetails.as_view()),
    path('random-media/', views.RandomMedia.as_view()),

    path('movie/<str:movie_id>/', views.MovieDetails.as_view()),
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:count>/', views.MovieList.as_view()),
    path('movies/<str:sort_type>/', views.MovieList.as_view()),
    path('movies/<str:sort_type>/<int:count>/', views.MovieList.as_view()),

    path('tv/<str:tv_id>/', views.TVDetails.as_view()),
    path('tvs/', views.TVList.as_view()),
    path('tvs/<int:count>/', views.TVList.as_view()),
    path('tvs/<str:sort_type>/', views.TVList.as_view()),
    path('tvs/<str:sort_type>/<int:count>/', views.TVList.as_view()),

    path('genre/', views.GenreList.as_view()),
    path('genre/<str:genre_id>/', views.GenreDetails.as_view()),
    path('random-media/', views.RandomMedia.as_view()),
    path('random-media/<int:count>/', views.RandomMedia.as_view()),
    path('random-media/<str:filter>/', views.RandomMedia.as_view()),
    path('random-media/<str:filter>/<int:count>/', views.RandomMedia.as_view()),
    path('random-collection/', views.RandomCollection.as_view()),

    path('search/', views.Search.as_view()),

    path('change-tmdb-id/<str:data_type>/<int:tmdb_id>/', views.change_tmdb_id),

    path('mongodb/', views.MongoDb.as_view()),
]
