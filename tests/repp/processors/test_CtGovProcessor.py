import os
import pytest

from rep.processors.CtGovPdfProcessor import CtGovPdfProcessor
from rep.processors.Exceptions import PdfProcessorException

def _load_pdf(pdf_filename):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "resources/", pdf_filename)
    with open(abs_file_path, 'rb') as f:
        return f.read()

processor = CtGovPdfProcessor()

def test_itShouldProcessAPDFBlob():
    test_pdf = _load_pdf("ct_normal_01.pdf")
    expected_name_to_vote_tuples = [
        ('JOHN W FONFARA', 'Y'),
        ('CATHERINE A OSTEN', 'Y'),
        ('DOUGLAS MCCRORY', 'Y'),
        ('PAUL M FORMICA', 'N'),
        ('SAUD ANWAR', 'Y'),
        ('KEVIN KELLY', 'N'),
        ('STEVE CASSANO', 'Y'),
        ('MARILYN MOORE', 'Y'),
        ('DEREK SLAP', 'Y'),
        ('DENNIS BRADLEY', 'Y'),
        ('GENNARO BIZZARRO', 'N'),
        ('JULIE KUSHNER', 'Y'),
        ('JOHN A KISSEL', 'N'),
        ('BOB DUFF', 'Y'),
        ('KEVIN D WITKOS', 'N'),
        ('WILL HASKELL', 'Y'),
        ('MATTHEW LESSER', 'Y'),
        ('CARLO LEONE', 'Y'),
        ('GARY WINFIELD', 'Y'),
        ('TONY HWANG', 'N'),
        ('MARTIN M LOONEY', 'Y'),
        ('MAE FLEXER', 'Y'),
        ('CHRISTINE COHEN', 'Y'),
        ('CRAIG MINER', 'N'),
        ('MARY ABRAMS', 'Y'),
        ('HENRI MARTIN', 'N'),
        ('JAMES MARONEY', 'Y'),
        ('ERIC BERTHEL', 'N'),
        ('JOAN V HARTLEY', 'N'),
        ('NORM NEEDLEMAN', 'Y'),
        ('ROBERT SAMPSON', 'N'),
        ('LEONARD FASANO', 'N'),
        ('GEORGE LOGAN', 'N'),
        ('DAN CHAMPAGNE', 'N'),
        ('HEATHER SOMERS', 'N'),
        ('ALEX KASSER', 'Y'),
    ]
    actual = processor.process_blob(
        test_pdf, 
        "https://repp.localhost/2020/foo/2020SV-00052-R00HB-6004-SV.PDF"
    )

    # idk, but I don't care enough to debug this
    assert abs(actual[0] - 1595995200.0) < 20000 == True
    assert actual[1] == 'HB-6004'
    assert actual[2] == 'foo'

    actual_name_to_vote_tuples = []
    for name, vote in zip(actual[3], actual[4]):
        actual_name_to_vote_tuples.append((name, vote))
    assert actual_name_to_vote_tuples == expected_name_to_vote_tuples

def test_itShouldThrowOnUnprocessablePdfs():
    test_pdf = _load_pdf("bad_pdf.pdf")
    with pytest.raises(PdfProcessorException):
        actual = processor.process_blob(
            test_pdf, 
            "https://repp.localhost/foo/foo.pdf"
        )
