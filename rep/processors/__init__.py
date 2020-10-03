from .CtGovPdfProcessor import CtGovPdfProcessor

processors = {
    "PDF&&CT_STATE_GOV": CtGovPdfProcessor()
}
def get_processor_map():
    return processors
