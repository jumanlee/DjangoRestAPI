from rest_framework import serializers
from .models import *

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id', 'clade', 'genus', 'species']

class PfamSerializer(serializers.ModelSerializer):

    domain_id = serializers.CharField(source='pfam_id')

    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']

class DomainsSerializer(serializers.ModelSerializer):

    pfam_id = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['pfam_id', 'description', 'start', 'stop']

    def get_pfam_id(self, obj):

        pfam_id = Pfam.objects.filter(pfam_id=obj.domain_id)
        return PfamSerializer(pfam_id, many=True).data

class ProteinAddRecordSerializer(serializers.ModelSerializer):

    class Meta:

        model = Protein
        fields = ['protein_id', 'sequence', 'length', 'foreign_taxa_id']

    def create(self, validated_data):

        taxa_data = self.initial_data.get('foreign_taxa_id')

        protein = Protein(**{**validated_data,
            'foreign_taxa_id': Organism.objects.get(pk=taxa_data['foreign_taxa_id']),
            })
        protein.save()
        return protein


class ProteinSerializer(serializers.ModelSerializer):

    taxonomy = serializers.SerializerMethodField()
    domains = serializers.SerializerMethodField()

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

    def get_taxonomy(self, obj):
        taxonomy = Organism.objects.filter(taxa_id=obj.foreign_taxa_id.pk)
        return OrganismSerializer(taxonomy, many=True).data[0]

    def get_domains(self, obj):
        domains = Domain.objects.filter(foreign_protein_id=obj.protein_id)
        return DomainsSerializer(domains, many=True).data


class ProteinListSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='auto_increment_id')

    class Meta:
        model = Protein
        fields = ['id','protein_id']

class DomainListSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='auto_increment_id')
    pfam_id = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['id', 'pfam_id']

    def get_pfam_id(self, obj):
        pfam_id = Pfam.objects.filter(pfam_id=obj.domain_id)
        return PfamSerializer(pfam_id, many=True).data[0]

class CoverageSerializer(serializers.ModelSerializer):

    coverage = serializers.SerializerMethodField()

    class Meta:
        model = Protein
        fields = ['coverage']

    #method to get the coverage 
    def get_coverage(self, obj):

        #retrieve the associated protein set based on the url parameter (protein_id)
        protein_set = Protein.objects.filter(protein_id = obj.protein_id)

        #retrieve the associated domain objects based on the requested protein_id
        domain_set = Domain.objects.filter(foreign_protein_id__in = protein_set)

        #put the filtered domains into a list for processing
        domain_set = list(domain_set)

        totalSum = 0

        for data in domain_set:
            #retrieve the associated length in the filtered protein set
            length = protein_set.filter(protein_id = data.foreign_protein_id.protein_id)

            #place the length into a retrievable list structure for easy processing, then parse the length into a single varible.
            length = list(length)[0].length

            #calculate and add up the coverage figures
            totalSum = float(totalSum + (abs(data.start - data.stop)/length))

            #return the exact number of decimal places as shown in the API specification. 
            totalSum = round(totalSum, 15)
        
        return totalSum


            







