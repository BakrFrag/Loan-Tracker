# from django.db.models.signals import post_save;
# from loan.models import Offer;
# from django.dispatch import receiver;
# @receiver(post_save,sender=Offer)
# def set_new_values(sender,created,instance,**kwargs):
#         instance.investor.balance -= 5003;
#         instance.loan.total_money += 750;
#         instance.loan.status="funded";
#         instance.save();