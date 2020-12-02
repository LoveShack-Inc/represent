
from rep.dao.ProcessedVoteResultDao import ProcessedVoteResultDao
from rep.dataclasses.ProcessedVoteResult import ProcessedVoteResult
from . import get_test_dao
from typing import List


def _get_vote_result(suffix: str="", **kwargs) -> ProcessedVoteResult:
    return ProcessedVoteResult(
        unixTime=0,
        billNumber=f"HBFOO{suffix}",
        voteName=f"VOTE_FOO{suffix}",
        repName=[
            "foo",
            "bar",
            "baz",
            "qux"
        ],
        repVote=[
            "Y",
            "N",
            "A",
            "Y",
        ],
        rawVoteObjectId=kwargs.get('rawVoteObjectId', 1)
    )

def _flatten(result: ProcessedVoteResult) -> List[ProcessedVoteResult]:
    return [
        ProcessedVoteResult(
            unixTime=result.unixTime,
            billNumber=result.billNumber,
            voteName=result.voteName,
            repName=result.repName[num],
            repVote=result.repVote[num],
            rawVoteObjectId=result.rawVoteObjectId
        ) for num, i in enumerate(result.repVote)
    ]

class Test:
    def setup_method(self, test_method):
        self.dao = get_test_dao(ProcessedVoteResultDao, True)

    def test_itCanInsertRecord(self):
        self.dao.write(_get_vote_result())

    def test_itCanGetByBillNumber(self):
        expected = _get_vote_result()
        self.dao.write(expected)
        self.dao.write(_get_vote_result("foo"))

        actual = self.dao.getByBillNumber(expected.billNumber)
        assert sorted(_flatten(expected), key=lambda x: x.repName) == sorted(actual, key=lambda x: x.repName)

    def test_itCanGetByVoteName(self):
        expected = _get_vote_result()
        self.dao.write(expected)
        self.dao.write(_get_vote_result("foo"))

        actual = self.dao.getByVoteName(expected.voteName)
        assert sorted(_flatten(expected), key=lambda x: x.repName) == sorted(actual, key=lambda x: x.repName)

    def test_itCanGetByRepName(self):
        insert = _get_vote_result()
        self.dao.write(insert)
        self.dao.write(_get_vote_result("foo", rawVoteObjectId=2))

        actual = self.dao.getByRepName("foo")

        expected = [
            ProcessedVoteResult(0, "HBFOO", "VOTE_FOO", "foo", "Y", 1),
            ProcessedVoteResult(0, "HBFOOfoo", "VOTE_FOOfoo", "foo", "Y", 2)
        ]
        assert 2 == len(actual)
        assert expected == sorted(actual, key=lambda x: x.voteName)

    def test_itCanGetByVoteObjectId(self):
        insert = _get_vote_result()
        self.dao.write(insert)
        self.dao.write(_get_vote_result(rawVoteObjectId=2))

        actual = self.dao.getByVoteObjectId(1)

        expected = [
            ProcessedVoteResult(0, "HBFOO", "VOTE_FOO", "bar", "N", 1),
            ProcessedVoteResult(0, "HBFOO", "VOTE_FOO", "baz", "A", 1),
            ProcessedVoteResult(0, "HBFOO", "VOTE_FOO", "foo", "Y", 1),
            ProcessedVoteResult(0, "HBFOO", "VOTE_FOO", "qux", "Y", 1),
        ]
        assert 4 == len(actual)
        assert expected == sorted(actual, key=lambda x: x.voteName)
