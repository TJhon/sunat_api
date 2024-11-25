from sqlmodel import Field, Session, SQLModel as sql, create_engine
from typing import List, Optional


class CotizationBase(sql):
    user: str
    hscode: str = Field(default=None, index=True)
    units: float
    price_unit: float
    total_kg: float
    cbm: float
    province: bool
    first_import: bool

    # trans_fee: float
    # handling: float
    # good_check: float
    # storage: float
    # shipmet_supervision: float
    # superevicion de embarque
    # custom_agent: float

    # operating_cost: float
    tc: float
    price_cbm: float
    desconsolidation_ton: float
    transport_local_province: float
    # no incluye igv
    transport_local_ton: float
    perception_percent: float
    insurage_percent: float
    ad_valorem_percent: float
    igv_percent: float
    ipm_percent: float
    antidupping_percent: float


class Cotization(CotizationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default="Now Python")


class CotizationResultBase(sql):
    user: str
    fob: float
    cif: float
    units: float
    insurage: float
    freight: float
    freight_taxes: float
    ad_valorem: float
    igv: float
    ipm: float
    antidupping: float
    perception: float
    total_taxes: float
    desconsolidation: float
    transport_local: float
    province: bool
    province_transport: float
    total_logistic: float
    first_import: float
    hscode: str = Field(index=True)


class CotizationResult(CotizationResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default="now python")
