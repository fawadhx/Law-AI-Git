from app.data.federal_catalog.crpc import CRPC_RECORDS
from app.data.federal_catalog.peca import PECA_RECORDS
from app.data.federal_catalog.ppc import PPC_RECORDS


FEDERAL_LEGAL_SOURCES = [
    *PPC_RECORDS,
    *CRPC_RECORDS,
    *PECA_RECORDS,
]
