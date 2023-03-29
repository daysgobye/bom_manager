from django.contrib.auth.models import AbstractUser
from django.db import models
from partlibary.models import Part
from io import StringIO
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned



class CustomUser(AbstractUser):
    part_libary = models.ManyToManyField(Part,related_name='part_library')
    old_part_libary = models.ManyToManyField(Part,related_name="rollback")
    incoming_part_libary = models.ManyToManyField(Part,related_name="incoming")
    part_libary_lookup = models.ManyToManyField(Part,related_name="lookup")
    def check_if_locations_are_needed(self):
        current_lib=self.incoming_part_libary.all()
        if len(current_lib)!=0:
            return True
        return False
    def setup_rollback(self):
        current_lib=self.part_libary.all()
        self.old_part_libary.all().delete()
        for part in current_lib:
            new_part=part.clone()
            self.old_part_libary.add(new_part)
        self.save()

    def add_csv(self,file_data:str):
        csvStringIO = StringIO(file_data)
        df = pd.read_csv(csvStringIO)
        df=df.fillna("missing")
        current_lib=self.part_libary.all()
        if len(current_lib)!=0:
            self.setup_rollback()
            for index, row in df.iterrows():
                if 'qty'in row:
                    try:
                        part_in_db=self.part_libary.get(value=row['value'],
                                            package=row['package'],
                                            part_number=row['part number'])
                        part_in_db.qty+=row['qty']
                        part_in_db.save()
                    except MultipleObjectsReturned:
                        part_in_db=self.part_libary.filter(value=row['value'],
                                            package=row['package'],
                                            part_number=row['part number']).first()
                        part_in_db.qty+=row['qty']
                        part_in_db.save()
                    except ObjectDoesNotExist:
                        new_part=Part.new_part_for_row(row)
                        if new_part.location!="missing":
                            self.part_libary.add(new_part)
                        else:
                            self.incoming_part_libary.add(new_part)
            self.save()

        else:
            for index, row in df.iterrows():
                new_part=Part.new_part_for_row(row)
                self.part_libary.add(new_part)
            self.save()

    def add_location_to_incoming_part(self,id:int,new_location:str):
        part_in_db=self.incoming_part_libary.get(id=id)
        if part_in_db:
            part_in_db.location=new_location
            part_in_db.save() 
            self.part_libary.add(part_in_db)
            self.incoming_part_libary.remove(id)
            self.save()
            return""
        else:
            return f"cant find id:{id} in the db"
    def lookup_single_part(self,value:str,package:str,part_number:str,qty:int):
        self.part_libary_lookup.all().delete()
        value_parts=self.part_libary.filter(value=value,package=package)
        part_number_parts=self.part_libary.filter(part_number=part_number)
        



    def lookup_csv(self,file_data:str):
        message="row"
        csvStringIO = StringIO(file_data)
        df = pd.read_csv(csvStringIO)
        df=df.fillna("missing")
        self.part_libary_lookup.all().delete()
        for index, row in df.iterrows():
            if 'qty'in row and row['qty']!="missing":
                temp_part=Part.new_part_for_row(row)
                try:
                    part_in_db=self.part_libary.get(value=row['value'],
                                        package=row['package'],
                                        part_number=row['part number'])
                    temp_part.location=part_in_db.location
                    if temp_part.qty<part_in_db.qty:
                        temp_part.missing_in_db=True
                except MultipleObjectsReturned:
                    part_in_db=self.part_libary.filter(value=row['value'],
                                            package=row['package'],
                                            part_number=row['part number']).first()
                    temp_part.location=part_in_db.location
                    if temp_part.qty<part_in_db.qty:
                        temp_part.missing_in_db=True
                except ObjectDoesNotExist:
                    temp_part.missing_in_db=True
                temp_part.save()
                self.part_libary_lookup.add(temp_part)

            else:
                message+=f" {index},"
        self.save()

        if message !="row":
            message+=" are missing qty field"
            return message
        else:
            return""
        
    def checkout_lookup(self):
        lookup=self.part_libary_lookup.all()
        for temp_part in lookup:
            try:
                part_in_db=self.part_libary.get(value=temp_part.value,
                                    package=temp_part.package,
                                    part_number=temp_part.part_number)
                part_in_db.qty-=temp_part.qty
                part_in_db.save()
            except MultipleObjectsReturned:
                part_in_db=self.part_libary.filter(value=temp_part.value,
                                    package=temp_part.package,
                                    part_number=temp_part.part_number).first()
                part_in_db.qty-=temp_part.qty
                part_in_db.save()
            except ObjectDoesNotExist:
                pass
    def delete_lookup(self):
        self.part_libary_lookup.all().delete()


    def __str__(self):
        return self.email