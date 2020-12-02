
import cherrypy

from . import VoteObjectHelper
from dataclasses import asdict
from rep.dao.ProcessedVoteResultDao import ProcessedVoteResultDao
from rep.dataclasses.PagedResponse import PagedResponse
from rep.dataclasses.VoteObjectFilter import VoteObjectFilter

class ProcessedVoteResultResource(object):
    def __init__(self, processed_vote_result_dao: ProcessedVoteResultDao):
        self.processed_vote_result_dao = processed_vote_result_dao

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, voteRecordId=None):
        vote_records = self.processed_vote_result_dao.getByVoteObjectId(voteRecordId)

        results = [
            asdict(i)
            for i in vote_records
        ]
        return VoteObjectHelper.to_paginated_response(len(results), 0, len(results)+1, results)
