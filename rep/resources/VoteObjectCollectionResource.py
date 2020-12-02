import cherrypy

from . import VoteObjectHelper
from dataclasses import asdict
from rep.dataclasses.PagedResponse import PagedResponse
from rep.dataclasses.VoteObjectFilter import VoteObjectFilter

class VoteObjectCollectionResource(object):
    """
        Collection view for vote objects
    """
    def __init__(self, vote_objects_dao):
        self.vote_objects_dao = vote_objects_dao


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, page=0, size=100, sourceUrl=None, sourceType=None, sourceFormat=None, isProcessed=None, voteId=None):
        page = int(page)
        size = int(size)

        vote_objects = None
        count = None

        if (sourceUrl is not None 
            or sourceType is not None or sourceFormat is not None
            or isProcessed is not None or voteId is not None):

            q_filter = VoteObjectFilter(
                sourceUrl=sourceUrl,
                sourceType=sourceType,
                sourceFormat=sourceFormat,
                isProcessed=isProcessed,
                vote_id=voteId,
            )
            vote_objects = self.vote_objects_dao.getAll(size, page * size, q_filter)
            count = self.vote_objects_dao.getCount(q_filter)
        else:
            vote_objects = self.vote_objects_dao.getAll(size, page * size)
            count = self.vote_objects_dao.getCount()

        results = [
            asdict(VoteObjectHelper.strip_blob(i))
            for i in vote_objects
        ]
        return VoteObjectHelper.to_paginated_response(count, page, size, results)
