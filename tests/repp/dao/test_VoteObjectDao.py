from rep.dao.VoteObjectDao import VoteObjectDao
from rep.dataclasses.VoteObject import VoteObject
from rep.dataclasses.VoteObjectFilter import VoteObjectFilter
from rep.dataclasses.Enums import SourceFormat, SourceType
from . import get_test_dao


TEST_VOTE_OBJECT = VoteObject(
    blob="foo_blob",
    sourceUrl="http://foo.localhost.com/VOTE/foo.pdf",
    sourceFormat=SourceFormat.PDF.name,
    sourceType=SourceType.CT_STATE_GOV.name,
    isProcessed=0
)

class Test:
    def setup_method(self, test_method):
        self.dao = get_test_dao(VoteObjectDao, True)

    def _helper_insert_n_records(self, count: int):
        inserted = []
        for i in range(0, count):
            to_write = VoteObject(
                    vote_id=i + 1,
                    blob=f"foo_blob_{i}",
                    sourceUrl=f"http://foo.localhost.com?foo={i}",
                    sourceFormat=SourceFormat.PDF.name,
                    sourceType=SourceType.CT_STATE_GOV.name,
                    isProcessed=0
                )
            self.dao.write(to_write)
            inserted.append(to_write)
        return inserted

    def test_itCanInsertRecord(self):
        self.dao.write(TEST_VOTE_OBJECT)


    def test_itOnlyInsertsNewRecords(self):
        expected = 1
        for i in range(0, 10):
            self.dao.write(TEST_VOTE_OBJECT)

        actual = self.dao.getCount()
        assert expected == actual


    def test_itCanGetTotalCount(self):
        expected = 1
        self.dao.write(TEST_VOTE_OBJECT)
        actual = self.dao.getCount()
        assert expected == actual


    def test_itCanGetTotalCountWithFilter(self):
        expected = 1
        self._helper_insert_n_records(10)
        self.dao.write(TEST_VOTE_OBJECT)
        actual = self.dao.getCount(VoteObjectFilter(sourceUrl=TEST_VOTE_OBJECT.sourceUrl))
        assert expected == actual


    # TODO: handle the sourceType and sourceFormat insert/selects better
    def test_itCanGetRecordById(self):
        self.dao.write(
            VoteObject(
                blob="foo_blob",
                sourceUrl="http://foo.localhost.com",
                sourceFormat=SourceFormat.PDF.name,
                sourceType=SourceType.CT_STATE_GOV.name,
                isProcessed=0,
                vote_id=1,
            )
        )
        expected = VoteObject(
            blob="foo_blob",
            sourceUrl="http://foo.localhost.com",
            sourceFormat=SourceFormat.PDF.name,
            sourceType=SourceType.CT_STATE_GOV.name,
            isProcessed=0,
            vote_id=1,
        )
        actual = self.dao.getById(1)
        assert expected == actual

    def test_itCanGetAll(self):
        expected = self._helper_insert_n_records(10)
        all_objects = self.dao.getAll()
        assert expected == all_objects


    def test_itCanGetAllWithSourceUrlFilter(self):
        expected = []
        expected = self._helper_insert_n_records(10)
        q_filter = VoteObjectFilter(sourceUrl="http://foo.localhost.com?foo=1")

        all_objects = self.dao.getAll(q_filter=q_filter)
        assert [expected[1]] == all_objects


    # TODO: modify if we ever add more formats
    def test_itCanGetAllWithSourceFormatFilter(self):
        expected = []
        expected = self._helper_insert_n_records(10)
        q_filter = VoteObjectFilter(sourceFormat="PDF")

        all_objects = self.dao.getAll(q_filter=q_filter)
        assert expected == all_objects

    # TODO: modify if we ever add more types
    def test_itCanGetAllWithSourceTypeFilter(self):
        expected = []
        expected = self._helper_insert_n_records(10)
        q_filter = VoteObjectFilter(sourceType="CT_STATE_GOV")

        all_objects = self.dao.getAll(q_filter=q_filter)
        assert expected == all_objects

    def test_itCanGetAllWithIsProcessedFilter(self):
        expected = VoteObject(
            blob="foo_blob_1",
            sourceUrl="http://foo.localhost.com?foo=1",
            sourceFormat=SourceFormat.PDF.name,
            sourceType=SourceType.CT_STATE_GOV.name,
            isProcessed=1,
            vote_id=2
        )

        self._helper_insert_n_records(10)
        self.dao.markProcessedBySourceUrl("http://foo.localhost.com?foo=1")
        q_filter = VoteObjectFilter(isProcessed=1)

        all_objects = self.dao.getAll(q_filter=q_filter)
        assert [expected] == all_objects


    def test_itCanGetProcessed(self):
        self.dao.write(TEST_VOTE_OBJECT)
        self.dao.markProcessedBySourceUrl(TEST_VOTE_OBJECT.sourceUrl)
        expected = VoteObject(
            blob=TEST_VOTE_OBJECT.blob,
            sourceUrl=TEST_VOTE_OBJECT.sourceUrl,
            sourceType=TEST_VOTE_OBJECT.sourceType,
            sourceFormat=TEST_VOTE_OBJECT.sourceFormat,
            isProcessed=1,
            vote_id=1
        )
        actual = self.dao.getProcessed()

        assert 1 == len(actual)
        assert expected == actual[0]

    def test_itCanGetUnprocessed(self):
        self.dao.write(TEST_VOTE_OBJECT)
        self.dao.markProcessedBySourceUrl(TEST_VOTE_OBJECT.sourceUrl)

        expected = VoteObject(
            blob=TEST_VOTE_OBJECT.blob,
            sourceUrl=f"{TEST_VOTE_OBJECT.sourceUrl}-insert",
            sourceType=TEST_VOTE_OBJECT.sourceType,
            sourceFormat=TEST_VOTE_OBJECT.sourceFormat,
            isProcessed=0,
            vote_id=2,
        )
        self.dao.write(expected)
        actual = self.dao.getUnprocessed()

        assert 1 == len(actual)
        assert expected == actual[0]

    def test_itCanCheckIfUrlIsIngested(self):
        self.dao.write(TEST_VOTE_OBJECT)
        assert True == self.dao.isUrlIngested(TEST_VOTE_OBJECT.sourceUrl)
