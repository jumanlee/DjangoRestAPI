from django.urls import include, path

from . import api

urlpatterns = [

    path('api/protein', api.ProteinAddRecord.as_view(), name='addprotein_api'),
    path('api/protein/<str:pk>', api.ProteinDetails.as_view(), name='protein_api'),
    path('api/pfam/<str:pk>', api.PfamDetails.as_view(), name='pfam_api'),
    path('api/proteins/<str:pk>', api.ProteinList.as_view(), name='protein_list_api'),
    path('api/pfams/<str:pk>', api.DomainList.as_view(), name='domain_list_api'),
    path('api/coverage/<str:pk>', api.CoverageView.as_view(), name='coverage_api')

]