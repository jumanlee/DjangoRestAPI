import os
import sys
import django
import csv
from collections import defaultdict

# sys.path.append('/Users/jumanlee87/Desktop/University/AdvWeb/AdvWebMidterm/github/bioweb')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb.settings')
django.setup()

from biodata.models import *

#get the raw data files
protein_organism = os.path.join(BASE_DIR, 'proteinorganism.csv')
protein_sequence = os.path.join(BASE_DIR, 'proteinsequence.csv')
pfam = os.path.join(BASE_DIR, 'pfam.csv')

#clear out residuals
Pfam.objects.all().delete()
Protein.objects.all().delete()
Domain.objects.all().delete()
Organism.objects.all().delete()

#data containers
#domain_id : description
pfam_container = defaultdict(list)

#list type: protein_id, domain_id, description, start, stop
domain_container = []

#protein_id = domain_id, length, taxa_id, sequence
protein_container = defaultdict(list)

#taxa_id = clade, genus, species, protein_id
organism_container = defaultdict(list)


#foreign key containers
# taxa_id : primary key of taxa
taxa_keys = {}
# protein_id : primary key of protein
protein_keys = {}

# domain_id/pfam_id : domain primary key
pfam_keys = {}


with open(protein_organism) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for protein_organism_row in csv_reader:

        domain_container.append([protein_organism_row[0], protein_organism_row[5], protein_organism_row[4], protein_organism_row[6], protein_organism_row[7]])

        #protein_id = domain_id, length, taxa_id, sequence
        protein_container[protein_organism_row[0]] = [protein_organism_row[5],protein_organism_row[8], protein_organism_row[1]]

        tupple = protein_organism_row[3].split(" ")

        #taxa_id = clade, genus, species, protein_id
        organism_container[protein_organism_row[1]] = [protein_organism_row[2], tupple[0], tupple[1], protein_organism_row[0]]


with open(protein_sequence) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for protein_sequence_row in csv_reader:
        protein_container[protein_sequence_row[0]].append(protein_sequence_row[1])

with open(pfam) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for pfam_row in csv_reader:
        pfam_container[pfam_row[0]] = pfam_row[1]

#taxa_id = clade, genus, species, protein_id
for key, data in organism_container.items():
    row = Organism.objects.create(taxa_id=key, clade=data[0], genus=data[1], species=data[2])

    row.save()

    taxa_keys[key] = row

# #protein_id = domain_id, length, taxa_id, sequence
for key, data in protein_container.items():

    #not all protein has sequence, so we need to test it here
    try:
        sequence_test = data[3]
    except:
        row = Protein.objects.create(protein_id=key, length=data[1], sequence="", foreign_taxa_id=taxa_keys[data[2]])
        row.save()
    else:
        row = Protein.objects.create(protein_id=key, length=data[1], sequence=data[3], foreign_taxa_id=taxa_keys[data[2]])
        row.save()


    # protein_id : primary key of protein
    protein_keys[key] = row

#list type: protein_id, domain_id, description, start, stop
for data in domain_container:
    row = Domain.objects.create(domain_id=data[1], description=data[2], start=data[3], stop=data[4], foreign_protein_id=protein_keys[data[0]])

    row.save()

    pfam_keys[data[1]] = row

#domain_id/pfam id : domain_description 
for key, data in pfam_container.items():
    row = Pfam.objects.create(pfam_id = key, domain_description = data, foreign_domain_id=pfam_keys[key])

    row.save()







