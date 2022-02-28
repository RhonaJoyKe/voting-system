from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import secrets
from cloudinary.models import CloudinaryField
class Position(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    name = models.CharField(max_length=50)
    total_vote = models.IntegerField(default=0, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image=CloudinaryField('image')
    def __str__(self):
        return "{} - {}".format(self.name, self.position.title)


class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    time_voted=models.DateTimeField()

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.position, self.status)

# POSITIONS = (
#         ("President", "President"),
#         ("Vice-President", "Vice-President"),
#         ("Secretary-General", "Secretary-General"),
#     )

# class Candidate(models.Model):
#     name=models.CharField(max_length=255)
#     image=CloudinaryField('image')
#     position=models.CharField(max_length=50,choices=POSITIONS)
#     admin = models.ForeignKey(User, on_delete=models.CASCADE)

#     def user_can_vote(self, user):
#         """ 
#         Return False if user already voted
#         """
#         user_votes = user.vote_set.all()
#         qs = user_votes.filter(poll=self)
#         if qs.exists():
#             return False
#         return True

#     @property
#     def get_vote_count(self):
#         return self.vote_set.count()

#     def get_result_dict(self):
#         res = []
#         for choice in self.choice_set.all():
#             d = {}
           
#             d['num_votes'] = choice.get_vote_count
#             if not self.get_vote_count:
#                 d['percentage'] = 0
#             else:
#                 d['percentage'] = (choice.get_vote_count /
#                                    self.get_vote_count)*100

#             res.append(d)
#         return res

#     def __str__(self):
#         return self.text


# class Votes(models.Model):
#     voter_name=models.OneToOneField(User, on_delete=models.CASCADE)
#     time_voted=models.DateTimeField()
#     candidate_voted = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    

#     def __str__(self):
#         return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
