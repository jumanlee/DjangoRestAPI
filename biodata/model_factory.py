import factory
from random import randint
from random import choice
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class OrganismFactory(factory.django.DjangoModelFactory):
    auto_increment_id = factory.Sequence(lambda n: '%d' % n)
    taxa_id = '55555'
    clade = 'E'
    genus = 'TestGenus'
    species = 'TestSpecies'

    class Meta:
        model = Organism

class ProteinFactory(factory.django.DjangoModelFactory):
    auto_increment_id = factory.Sequence(lambda n: '%d' % n)
    protein_id = 'A0A091SFC6Test'
    sequence = 'ABCDEFGHIJKLMN'
    length = randint(1, 10000)

    #foreign keys
    foreign_taxa_id = factory.SubFactory(OrganismFactory)

    class Meta:
        model = Protein

class DomainFactory(factory.django.DjangoModelFactory):
    auto_increment_id = factory.Sequence(lambda n: '%d' % n)
    domain_id = 'PF00002Test'
    description = 'Peptidase C13 legumain'
    start = randint(1, 2000)
    stop = randint(1, 2000)

    #foreign keys
    foreign_protein_id = factory.SubFactory(ProteinFactory)

    class Meta:
        model = Domain

class PfamFactory(factory.django.DjangoModelFactory):
    auto_increment_id = factory.Sequence(lambda n: '%d' % n)
    pfam_id = 'PF00002Test'
    domain_description = 'PeptidaseC13family'

    #foreign keys
    foreign_domain_id = factory.SubFactory(DomainFactory)

    class Meta:
        model = Pfam



