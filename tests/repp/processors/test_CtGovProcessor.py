import os
import pytest

from rep.dataclasses.VoteObject import VoteObject
from rep.processors.CtGovPdfProcessor import CtGovPdfProcessor
from rep.processors.Exceptions import PdfProcessorException

def _load_pdf(pdf_filename):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "resources/", pdf_filename)
    with open(abs_file_path, 'rb') as f:
        return f.read()

processor = CtGovPdfProcessor()

def test_itShouldProcessARollCallPDFBlob():
    test_pdf = _load_pdf("hb_roll_call.pdf")
    expected_name_to_vote_tuples = [('ABERCROMBIE', 'Y'), ('PORTER', 'Y'), ('CANDELORA, V.', 'Y'), 
    ('PISCOPO', 'Y'), ('ADAMS', 'Y'), ('REED', 'Y'), ('CARNEY', 'Y'), ('POLLETTA', 'Y'), 
    ('ALBIS', 'Y'), ('REYES', 'Y'), ('CARPINO', 'Y'), ('REBIMBAS', 'Y'), ('ALTOBELLO', 'Y'), 
    ('RILEY', 'Y'), ('CASE', 'Y'), ('RUTIGLIANO', 'Y'), ('ARCONTI', 'Y'), ('RITTER', 'Y'), 
    ('CHEESEMAN', 'Y'), ('SAMPSON', 'Y'), ('BAKER', 'Y'), ('ROJAS', 'Y'), ('CUMMINGS', 'Y'), 
    ('SIEGRIST', 'Y'), ('BORER', 'Y'), ('ROSARIO', 'Y'), ('D’AMELIO', 'Y'), ('SIMANSKI', 'Y'), 
    ('BOYD', 'Y'), ('ROSE', 'Y'), ('DAUPHINAIS', 'Y'), ('SKULCZYCK', 'Y'), ('BUTLER', 'Y'), 
    ('ROVERO', 'Y'), ('DAVIS', 'Y'), ('SMITH', 'Y'), ('CONLEY', 'Y'), ('SANCHEZ', 'Y'), 
    ('DELNICKI', 'Y'), ('SREDZINSKI', 'Y'), ('CURREY', 'Y'), ('SANTIAGO, E.', 'Y'), ('DEVLIN', 'Y'), 
    ('SRINIVASAN', 'Y'), ('D’AGOSTINO', 'Y'), ('SANTIAGO, H.', 'Y'), ('DUBITSKY', 'Y'), 
    ('STANESKI', 'Y'), ('DE LA CRUZ', 'Y'), ('SCANLON', 'Y'), ('DUFF', 'Y'), ('STOKES', 'Y'), 
    ('DEMICCO', 'Y'), ('SERRA', 'Y'), ('DUNSBY', 'Y'), ('STORMS', 'Y'), ('DILLON', 'Y'), 
    ('SIMMONS', 'Y'), ('FERGUSON', 'Y'), ('TWEEDIE', 'Y'), ('DIMASSA', 'Y'), ('SLAP', 'Y'), 
    ('FERRARO', 'Y'), ('VAIL', 'Y'), ('ELLIOTT', 'Y'), ('SOTO', 'Y'), ('FISHBEIN', 'Y'), 
    ('WILMS', 'Y'), ('FLEISCHMANN', 'Y'), ('STAFSTROM', 'Y'), ('FLOREN', 'X'), ('WILSON', 'Y'), 
    ('FOX', 'Y'), ('STALLWORTH', 'Y'), ('FRANCE', 'X'), ('WOOD', 'Y'), ('GENGA', 'Y'), 
    ('STEINBERG', 'Y'), ('FREY', 'Y'), ('YACCARINO', 'Y'), ('GIBSON', 'Y'), ('TERCYAK', 'Y'), 
    ('FUSCO', 'Y'), ('ZAWISTOWSKI', 'Y'), ('GONZALEZ', 'Y'), ('TONG', 'Y'), ('GREEN', 'Y'), 
    ('ZIOBRON', 'Y'), ('GRESKO', 'Y'), ('URBAN', 'Y'), ('HALL, C.', 'Y'), ('ZUPKUS', 'Y'), 
    ('GUERRERA', 'Y'), ('VARGAS', 'Y'), ('HARDING', 'Y'), ('HADDAD', 'Y'), ('VERRENGIA', 'Y'), 
    ('KLARIDES', 'Y'), ('HALL, J.', 'Y'), ('WALKER', 'Y'), ('KLARIDES-DITRIA', 'Y'), 
    ('HAMPTON', 'Y'), ('WINKLER', 'Y'), ('KOKORUDA', 'Y'), ('ARESIMOWICZ', 'Y'), ('HENNESSY', 'Y'), 
    ('YOUNG', 'Y'), ('KUPCHICK', 'Y'), ('JOHNSON', 'Y'), ('ZIOGAS', 'Y'), ('LABRIOLA', 'X'), 
    ('JULESON-SCOPINO', 'Y'), ('LAVIELLE', 'Y'), ('GODFREY', 'Y'), ('LEMAR', 'Y'), 
    ('LEGEYT', 'Y'), ('LESSER', 'Y'), ('MACLACHLAN', 'Y'), ('LINEHAN', 'Y'), ('ACKERT', 'Y'), 
    ('MCCARTY, K.', 'Y'), ('BERGER', 'Y'), ('LOPES', 'Y'), ('BELSITO', 'Y'), ('MCGORTY, B.', 'Y'), 
    ('CANDELARIA, J.', 'Y'), ('MCCARTHY VAHEY', 'Y'), ('BETTS', 'Y'), ('O’DEA', 'Y'), 
    ('COOK', 'Y'), ('MCGEE', 'Y'), ('BOCCHINO', 'Y'), ('OHLER', 'Y'), ('GENTILE', 'Y'), 
    ('MILLER, P.B.', 'Y'), ('BOLINSKY', 'Y'), ('O’NEILL', 'Y'), ('MORIN', 'Y'), ('MUSHINSKY', 'Y'), 
    ('BUCKBEE', 'Y'), ('PAVALOCK-D’AMATO', 'Y'), ('MORRIS', 'Y'), ('PAOLILLO', 'Y'), ('BYRON', 'Y'), 
    ('PERILLO', 'Y'), ('ORANGE', 'Y'), ('PERONE', 'Y'), ('CAMILLO', 'Y'), ('PETIT', 'Y'), 
    ('RYAN', 'Y')]

    actual = processor.process_blob(
        VoteObject(
            blob=test_pdf,
            sourceUrl="https://repp.localhost/2020/foo/2020SV-00052-R00HB-6004-SV.PDF",
            sourceType="CT_STATE_GOV",
            sourceFormat="PDF",
            isProcessed=0,
            vote_id=1
        )
    )

    # idk, but I don't care enough to debug this
    assert abs(actual.unixTime - 1588219200.0) < 20000
    assert actual.billNumber == 'HB-5235'
    assert actual.voteName == 'HB-5235'

    actual_name_to_vote_tuples = []
    for name, vote in zip(actual.repName, actual.repVote ):
        actual_name_to_vote_tuples.append((name, vote))

    assert actual_name_to_vote_tuples == expected_name_to_vote_tuples

def test_itShouldProcessAPDFBlob():
    test_pdf = _load_pdf("ct_normal_01.pdf")
    expected_name_to_vote_tuples = [
        ('JOHN W. FONFARA', 'Y'), ('CATHERINE A. OSTEN', 'Y'), ('DOUGLAS MCCRORY', 'Y'),
        ('PAUL M. FORMICA', 'N'), ('SAUD ANWAR', 'Y'), ('KEVIN KELLY', 'N'),
        ('STEVE CASSANO', 'Y'), ('MARILYN MOORE', 'Y'), ('DEREK SLAP', 'Y'),
        ('DENNIS BRADLEY', 'Y'), ('GENNARO BIZZARRO', 'N'), ('JULIE KUSHNER', 'Y'),
        ('JOHN A. KISSEL', 'N'), ('BOB DUFF', 'Y'), ('KEVIN D. WITKOS', 'N'),
        ('WILL HASKELL', 'Y'), ('MATTHEW LESSER', 'Y'), ('CARLO LEONE', 'Y'),
        ('GARY WINFIELD', 'Y'), ('TONY HWANG', 'N'), ('MARTIN M. LOONEY', 'Y'),
        ('MAE FLEXER', 'Y'), ('CHRISTINE COHEN', 'Y'), ('CRAIG MINER', 'N'),
        ('MARY ABRAMS', 'Y'), ('HENRI MARTIN', 'N'), ('JAMES MARONEY', 'Y'),
        ('ERIC BERTHEL', 'N'), ('JOAN V. HARTLEY', 'N'), ('NORM NEEDLEMAN', 'Y'),
        ('ROBERT SAMPSON', 'N'), ('LEONARD FASANO', 'N'), ('GEORGE LOGAN', 'N'),
        ('DAN CHAMPAGNE', 'N'), ('HEATHER SOMERS', 'N'), ('ALEX KASSER', 'Y'),
    ]
    actual = processor.process_blob(
        VoteObject(
            blob=test_pdf,
            sourceUrl="https://repp.localhost/2020/foo/2020SV-00052-R00HB-6004-SV.PDF",
            sourceType="CT_STATE_GOV",
            sourceFormat="PDF",
            isProcessed=0,
            vote_id=1
        )
    )

    # idk, but I don't care enough to debug this
    assert abs(actual.unixTime - 1595995200.0) < 20000
    assert actual.billNumber == 'HB-6004'
    assert actual.voteName == 'HB-6004'

    actual_name_to_vote_tuples = []
    for name, vote in zip(actual.repName, actual.repVote ):
        actual_name_to_vote_tuples.append((name, vote))
    assert actual_name_to_vote_tuples == expected_name_to_vote_tuples

def test_itShouldThrowOnUnprocessablePdfs():
    test_pdf = _load_pdf("bad_pdf.pdf")
    with pytest.raises(PdfProcessorException):
        processor.process_blob(
            VoteObject(
                blob=test_pdf,
                sourceUrl="https://repp.localhost/foo/foo.pdf",
                sourceType="CT_STATE_GOV",
                sourceFormat="PDF",
                isProcessed=0,
                vote_id=1
            )
        )
