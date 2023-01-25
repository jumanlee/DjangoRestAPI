from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *

class ProteinDetails(mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):

        queryset = Protein.objects.all()
        serializer_class = ProteinSerializer

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

        def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

        def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

        def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

class ProteinAddRecord(mixins.CreateModelMixin,
                        generics.GenericAPIView):

    serializer_class = ProteinAddRecordSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)   

class PfamDetails(mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProteinList(generics.ListAPIView):

    serializer_class = ProteinListSerializer

    def get_queryset(self):
        taxa_id = self.kwargs['pk']
        return Protein.objects.filter(foreign_taxa_id__taxa_id=taxa_id)

class DomainList(generics.ListAPIView):

    serializer_class = DomainListSerializer

    def get_queryset(self):
        taxa_id = self.kwargs['pk']
        protein_set = Protein.objects.filter(foreign_taxa_id__taxa_id=taxa_id)
        domain_set = Domain.objects.filter(foreign_protein_id__protein_id__in=protein_set)

        return domain_set

class CoverageView(
                     mixins.RetrieveModelMixin,
                     generics.GenericAPIView):

    queryset = Protein.objects.all()
    serializer_class = CoverageSerializer
    
    def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)
