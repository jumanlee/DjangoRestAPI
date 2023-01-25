import json
from django.test import TestCase

# Reverse allows us to take a path in our URL's file and turn it into an actual URL string. 
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factory import *
from .serializers import *
from collections import OrderedDict

class SerializerTest(APITestCase):
    taxa1 = None
    organismserializer = None

    protein1 = None
    proteinserializer = None

    domain1 = None
    domainsserializer = None

    pfam1 = None
    pfamserializer = None

    def setUp(self):
        #insert new data
        #organism
        self.taxa1 = OrganismFactory.create(taxa_id="12345")
        self.organismserializer = OrganismSerializer(instance=self.taxa1)

        #protein
        self.protein1 = ProteinFactory.create(protein_id="A123Test1", length=865, foreign_taxa_id = self.taxa1)
        self.proteinserializer = ProteinSerializer(instance=self.protein1)
        self.proteinListSerializer = ProteinListSerializer(instance=self.protein1)

        #domain
        self.domain1 = DomainFactory.create(domain_id='PF00002Test1', start=40, stop=94, foreign_protein_id = self.protein1)
        self.domainsserializer = DomainsSerializer(instance=self.domain1)
        self.domainListSerializer = DomainListSerializer(instance=self.domain1)

        #pfam
        self.pfam1 = PfamFactory.create(pfam_id="PF00002Test1", foreign_domain_id=self.domain1)
        self.pfamserializer = PfamSerializer(instance=self.pfam1)

    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

        OrganismFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)
        DomainFactory.reset_sequence(0)
        PfamFactory.reset_sequence(0)

    def test_serializers(self):
        organismData = self.organismserializer.data
        self.assertEqual(set(organismData.keys()), set(['taxa_id', 'clade', 'genus', 'species']))

        proteinData = self.proteinserializer.data
        self.assertEqual(set(proteinData.keys()), set(['protein_id', 'sequence', 'taxonomy', 'length', 'domains']))

        proteinListData = self.proteinListSerializer.data
        self.assertEqual(set(proteinListData.keys()), set(['id','protein_id']))

        domainData = self.domainsserializer.data
        self.assertEqual(set(domainData.keys()), set(['pfam_id', 'description', 'start', 'stop']))

        domainListData = self.domainListSerializer.data
        self.assertEqual(set(domainListData.keys()), set(['id', 'pfam_id']))

        pfamData = self.pfamserializer.data
        self.assertEqual(set(pfamData.keys()), set(['domain_id', 'domain_description']))


    def test_serializerHasCorrectData(self):
        organismData = self.organismserializer.data
        self.assertEqual(organismData['taxa_id'], '12345')

        proteinData = self.proteinserializer.data
        self.assertEqual(proteinData['protein_id'], "A123Test1")

        proteinListData = self.proteinListSerializer.data
        self.assertEqual(proteinListData['protein_id'], 'A123Test1')

        domainData = self.domainsserializer.data
        self.assertEqual(domainData['pfam_id'], [OrderedDict([('domain_id', 'PF00002Test1'), ('domain_description', 'PeptidaseC13family')])])

        domainListData = self.domainListSerializer.data
        self.assertEqual(domainListData['pfam_id'], OrderedDict([('domain_id', 'PF00002Test1'), ('domain_description', 'PeptidaseC13family')]))

        pfamData = self.pfamserializer.data
        self.assertEqual(pfamData['domain_id'], 'PF00002Test1')


class URLTest(APITestCase):

    taxa1 = None

    #protein details url
    working_url_protein = ''
    faulty_url_protein = ''
    remove_url_protein = ''

    #pfam details url
    working_url_pfam = ''
    faulty_url_pfam = ''
    remove_url_pfam = ''


    def setUp(self):
        self.taxa1 = OrganismFactory.create(taxa_id="12345")
        self.protein1 = ProteinFactory.create(protein_id="A123Test1", foreign_taxa_id=self.taxa1)
        self.protein2 = ProteinFactory.create(protein_id="A123Test2", foreign_taxa_id=self.taxa1)
        self.protein3 = ProteinFactory.create(protein_id="A123Test3", foreign_taxa_id=self.taxa1)

        self.domain1 = DomainFactory.create(domain_id='PF00002Test1', foreign_protein_id=self.protein1)
        self.pfam1 = PfamFactory.create(pfam_id='PF00002Test1', foreign_domain_id=self.domain1)

        #protein details url
        self.working_url_protein = reverse('protein_api', kwargs={'pk': "A123Test1"})
        self.faulty_url_protein = '/api/protein/bad/'
   
        #protien list url
        self.working_url_proteinList = reverse('protein_list_api', kwargs={'pk': "12345"})
        self.faulty_url_proteinList = '/api/proteins/bad/'

        #pfam details url
        self.working_url_pfam = reverse('pfam_api', kwargs={'pk':'PF00002Test1'})
        self.faulty_url_pfam = '/api/pfam/bad/'

        #pfam list url 
        self.working_url_pfamList = reverse('pfam_list_api', kwargs={'pk': "12345"})
        self.faulty_url_pfamList = '/api/pfams/bad/'

        #coverage url
        self.working_url_coverage = reverse('coverage_api', kwargs={'pk': 'A123Test1'})
        self.faulty_url_coverage = '/api/coverage/bad/'


    def tearDown(self):
        Organism.objects.all().delete()
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()

        OrganismFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)
        DomainFactory.reset_sequence(0)
        PfamFactory.reset_sequence(0)


    def test_detailsReturnGood(self):
        #testing protein details url
        response_protein = self.client.get(self.working_url_protein, format='json')
        response_protein.render()
        self.assertEqual(response_protein.status_code, 200)

        #testing protein list url
        response_protein_list = self.client.get(self.working_url_proteinList, format='json')
        response_protein_list.render()
        self.assertEqual(response_protein_list.status_code, 200)

        #testing pfam details url
        response_pfam = self.client.get(self.working_url_pfam, format='json')
        response_pfam.render()
        self.assertEqual(response_pfam.status_code, 200)

        #testing pfam list url 
        response_pfam_list = self.client.get(self.working_url_pfamList, format='json')
        response_pfam_list.render()
        self.assertEqual(response_pfam_list.status_code, 200)

        #coverage url
        response_coverage = self.client.get(self.working_url_coverage, format='json')
        response_coverage.render()
        self.assertEqual(response_coverage.status_code, 200)

        
        #check if data arrived is correct
        proteinDetailsData = json.loads(response_protein.content)
        self.assertTrue('sequence' in proteinDetailsData)
        self.assertTrue(proteinDetailsData['sequence'], 'ABCDEFGHIJKLMN')

        proteinListData = json.loads(response_protein_list.content)
        self.assertTrue({'id': '4', 'protein_id': 'A123Test2'} in proteinListData)

        pfamDetailsData = json.loads(response_pfam.content)
        self.assertTrue('domain_id' in pfamDetailsData)
        self.assertTrue(pfamDetailsData['domain_id'], 'PF00002Test1')

        pfamListData = json.loads(response_pfam_list.content)
        self.assertTrue({'id': '1', 'pfam_id': {'domain_id': 'PF00002Test1', 'domain_description': 'PeptidaseC13family'}} in pfamListData)

        coverageData = json.loads(response_coverage.content)
        self.assertTrue('coverage' in coverageData)
        self.assertTrue(coverageData['coverage'], (abs(40-94)/865))


    def test_detailsReturnBad(self):
        response_protein = self.client.get(self.faulty_url_protein, format='json')
        self.assertEqual(response_protein.status_code, 404)

        response_protein_list = self.client.get(self.faulty_url_proteinList, format='json')
        self.assertEqual(response_protein_list.status_code, 404)

        response_pfam = self.client.get(self.faulty_url_pfam, format='json')
        self.assertEqual(response_pfam.status_code, 404)

        response_pfam_list = self.client.get(self.faulty_url_proteinList, format='json')
        self.assertEqual(response_protein_list.status_code, 404)


















