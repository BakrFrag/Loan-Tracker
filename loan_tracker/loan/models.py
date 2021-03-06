from django.db import models
from django.dispatch import receiver;
from django.db.models.signals import post_save;
from django.urls import reverse;
# Annual Interest Rate 5000*(15/100) =750
Annual_Interest_Rate=750;
LOAN_CHOICES=(

    # investor submit offer
    ("funded","Fundded"), 
    # brrower return mony back to investor
    ("completed","Completed") 
);

class Brrower(models.Model):
    name=models.CharField(max_length=256,unique=True);
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name;
    def get_absolute_url(self):
        return reverse("brrower", kwargs={"pk": self.pk})
    
class Investor(models.Model):
    name=models.CharField(max_length=256,unique=True);
    balance=models.IntegerField();
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name;
    def get_absolute_url(self):
        return reverse("investor", kwargs={"pk": self.pk})
    

"""
total_money field will hold the total money brrower have to 
give back to investor 
when loan created the field will be 5000 (loan ammount)
when offer come to this loan the total_money will be 
5750 (amount + annual_rate)
"""
class Loan(models.Model):
    duration=models.CharField(default="6 Months",max_length=256);
    amount=models.IntegerField(default=5000.0);
    annual_rate = models.FloatField(default=0.15);
    currency=models.CharField(default="$ Americian Dolar",max_length=256);
    status=models.CharField(choices=LOAN_CHOICES,max_length=256,null=True);
    total_money=models.IntegerField(default=5000);
    brrower=models.OneToOneField(Brrower,on_delete=models.CASCADE);
    created=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        self.duration="6 Months";
        self.amount=5000.0;
        self.currency="$ Americian Dolar";
        self.annual_rate=0.15;
        super(Loan,self).save(*args,**kwargs);

    def __str__(self):
        return f"Loan With Brrower {self.brrower.name} "
    def get_absolute_url(self):
        return reverse("loan", kwargs={"pk": self.pk})
    
class Offer(models.Model):
    loan=models.OneToOneField(Loan,on_delete=models.CASCADE);
    investor=models.OneToOneField(Investor,on_delete=models.CASCADE);
    created=models.DateTimeField(auto_now_add=True);
    def __str__(self):
        return f"Offer On Loan f{self.loan}";
    def get_absolute_url(self):
        return reverse("offer", kwargs={"pk": self.pk})
    
    
"""
this post save signal achive logic on offer
if offer created :
    investor balance will decrease by 5003 (loan ammount + fee)
    also loan status will be funded;
    loan total money will increase by 750 (annual interst )
    total_money 5000+750=5750 
"""

def set_new_values(sender,created,instance,**kwargs):
    if created:
        investor=instance.investor;
        loan=instance.loan;
        investor.balance -= 5003;
        investor.save();
        loan.status = "funded";
        loan.total_money += 750;
        loan.save();
post_save.connect(set_new_values,sender=Offer)