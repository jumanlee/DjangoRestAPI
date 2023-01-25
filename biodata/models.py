from django.db import models


class Organism(models.Model):
    auto_increment_id = models.IntegerField(unique=True, default=1)
    taxa_id = models.CharField(max_length=256, null=False, blank=False, primary_key=True, db_index=True)
    clade = models.CharField(max_length=256, null=False, blank=False)
    genus = models.CharField(max_length=256, null=False, blank=True)
    species = models.CharField(max_length=256, null=False, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Organism.objects.all().aggregate(largest=models.Max('auto_increment_id'))['largest']

            if last_id is not None:
                self.auto_increment_id = last_id + 1

        super(Organism, self).save(*args, **kwargs)

class Protein(models.Model):
    auto_increment_id = models.IntegerField(unique=True, default=1)
    protein_id = models.CharField(max_length=256, null=False, blank=False, primary_key=True, db_index=True)
    sequence = models.CharField(max_length=40000, null=False, blank=True)
    length = models.IntegerField(null=False, blank=True)

    #foreign keys
    foreign_taxa_id = models.ForeignKey(Organism, on_delete=models.CASCADE)

    #emulating AutoField code. The code is taken from https://stackoverflow.com/questions/41228034/django-non-primary-key-autofield
    def save(self, *args, **kwargs):
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Protein.objects.all().aggregate(largest=models.Max('auto_increment_id'))['largest']

            if last_id is not None:
                self.auto_increment_id = last_id + 1

        super(Protein, self).save(*args, **kwargs)

class Domain(models.Model):
    auto_increment_id = models.AutoField(primary_key=True, db_index=True)
    domain_id = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=False)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)

    #foreign keys
    foreign_protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)


class Pfam(models.Model):
    auto_increment_id = models.IntegerField(unique=True, default=1)
    pfam_id = models.CharField(max_length=256, null=False, blank=False, primary_key=True, db_index=True)
    domain_description = models.CharField(max_length=256, null=False, blank=False)

    #foreign keys
    foreign_domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)

    #emulating AutoField code. The code is taken from https://stackoverflow.com/questions/41228034/django-non-primary-key-autofield
    def save(self, *args, **kwargs):
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Pfam.objects.all().aggregate(largest=models.Max('auto_increment_id'))['largest']

            if last_id is not None:
                self.auto_increment_id = last_id + 1

        super(Pfam, self).save(*args, **kwargs)



    
