from .models import *
from .core import *




def add_bookmark(pmid, user_id):
    s = Settings.objects.get(user_id=user_id)
    s.bookmarks.add(pmid=pmid)
    s.save()

def add_upvote(pmid, user_id):
    s = Settings.objects.get(user_id=user_id)
    s.upvotes.add(pmid=pmid)
    s.save()

def add_downvote(pmid, user_id):
    s = Settings.objects.get(user_id=user_id)
    s.downvotes.add(pmid=pmid)
    s.save()

def remove_bookmark(pmid, user_id):
    s = Settings.objects.get(user_id=user_id)
    s.bookmarks.remove(pmid=pmid)
    s.save()

def remove_upvote(pmid, user_id):
    s = Settings.objects.get(user_id=user_id)
    s.upvotes.remove(pmid=pmid)
    s.save()    

def remove_downvote(pmid, user_id): 
    s = Settings.objects.get(user_id=user_id)
    s.downvotes.remove(pmid=pmid)
    s.save()

def get_bookmarks(user_id):
    """Returns a list of pmids that are bookmarked by the user"""
    s = Settings.objects.get(user_id=user_id)
    return [i.pmid for i in s.bookmarks.all()]

def get_upvotes(user_id):
    """Returns a list of pmids that are upvoted by the user"""
    s = Settings.objects.get(user_id=user_id)
    return [i.pmid for i in s.upvotes.all()]

def get_downvotes(user_id):
    """Returns a list of pmids that are downvoted by the user"""
    s = Settings.objects.get(user_id=user_id)
    return [i.pmid for i in s.downvotes.all()]  

def get_keywords(user_id):
    """Returns a list of keywords that are set by the user"""
    s = Settings.objects.get(user_id=user_id)
    return s.keywords

def add_keywords(user_id, keywords):
    """Sets the keywords for the user"""
    s = Settings.objects.get(user_id=user_id)
    s.keywords = keywords
    s.save()

