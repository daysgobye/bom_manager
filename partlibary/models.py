from django.db import models

class Part(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    qty = models.IntegerField()
    note = models.TextField()
    location = models.TextField()
    data_sheet= models.TextField()
    missing_in_db=models.BooleanField(default=False)
    def clone(self):
         new_part=Part(name="missing",
                              package="missing",
                              value="missing",
                              part_number="missing",
                              qty=0,
                              note="missing",
                              location="missing",
                              data_sheet="missing")
         new_part.name=self.name
         new_part.package=self.package
         new_part.value=self.value
         new_part.part_number=self.part_number
         new_part.qty=self.qty
         new_part.note=self.note
         new_part.location=self.location
         new_part.data_sheet=self.data_sheet
         new_part.save()
         return new_part

    def __str__(self):
        return f"{self.name}:{self.package}:{self.value}"
    @staticmethod
    def new_part_for_row(row,missing_in_db=False):
        new_part=Part(name="missing",
                              package="missing",
                              value="missing",
                              part_number="missing",
                              qty=0,
                              note="missing",
                              location="missing",
                              data_sheet="missing",
                            missing_in_db=missing_in_db
                              )
        if 'name'in row:
            new_part.name=row['name']
        if 'qty'in row:
            new_part.qty=row['qty']
        if 'package'in row:
            new_part.package=row['package']
        if 'value'in row:
            new_part.value=row['value']
        if 'note'in row:
            new_part.note=row['note']
        if 'datasheet'in row:
            new_part.data_sheet=row['datasheet']
        if 'part number'in row:
            new_part.part_number=row['part number']
        if 'location'in row:
            new_part.location=row['location']
        new_part.save()
        return new_part