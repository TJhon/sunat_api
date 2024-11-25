from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class FixedCostTotal:
    trans_fee: float = 51
    handling: float = 0
    # no incluye igv
    good_check: float = 141
    storage: float = 200
    shipmet_supervision: float = 100
    # superevicion de embarque
    custom_agent: float = 120 * 1.18
    operating_cost: float = 35 * 1.18
    tc: float = 3.81


@dataclass
class VariableCosts:
    price_cbm: float = 35
    desconsolidation_ton: float = 47.2
    transport_local_province: float = 450

    # no incluye igv
    transport_local_ton: float = 65


@dataclass
class TaxesHSCode:
    perception_percent: float = 10
    insurage_percent: float = 2
    ad_valorem_percent: float = 4
    igv_percent: float = 16
    ipm_percent: float = 2
    antidupping_percent: float = 0


@dataclass
class InputForm:
    user: str = "User"
    hscode: str = None
    units: float = None
    price_unit: float = None
    total_kg: float = None
    cbm: float = None
    province: bool = False
    first_import: bool = False


@dataclass
class Info:
    units: float = None
    price_unit: float = None
    total_kg: float = None
    cbm: float = None
    province: bool = False
    # flete + seguro
    price_cbm: float = None
    insurage_percent: float = None
    # Transport Local
    desconsolidation_ton: float = 47.2
    transport_local_ton: float = 65
    transport_local_province: float = 450
    # Taxes
    ad_valorem_percent: float = 6
    igv_percent: float = 16
    ipm_percent: float = 2
    antidupping_percent: float = 0
    perception_percent: float = 10
    first_import: bool = False
    # tc
    tc: float = 3.81
    hscode: str = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def run_all(self):
        self.calculate_fob()
        self.calculate_cif()
        self.calculate_taxes()
        self.logistic_cost_local()

    def calculate_fob(self):
        self.fob = self.units * self.price_unit

    def calculate_cif(self):
        insurage = self.insurage_percent / 100 * self.fob
        freight = self.price_cbm * self.cbm
        cif = insurage + freight + self.fob
        self.insurage = insurage
        self.freight = freight
        self.freigth_taxes = insurage + freight
        self.cif = cif

    def calculate_taxes(self):
        cif = self.cif
        ad_valorem = cif * self.ad_valorem_percent / 100
        igv = cif * self.igv_percent / 100
        ipm = cif * self.ipm_percent / 100
        antidupping = cif * self.antidupping_percent / 100

        CIF = cif + ad_valorem + igv + ipm + antidupping
        if not self.first_import:
            self.perception_percent = 3.5
        perception = CIF * self.perception_percent / 100

        total_taxes = CIF + perception - cif

        self.ad_valorem = ad_valorem
        self.igv = igv
        self.ipm = ipm
        self.antidupping = antidupping
        self.perception = perception

        self.total_taxes = total_taxes

    def logistic_cost_local(self):
        total_kg = self.total_kg
        if total_kg is None:
            total_kg = self.units
        ton = total_kg / 1000
        desconsolidation = ton * self.desconsolidation_ton
        transport_local = ton * self.transport_local_ton * (1.18)
        province_transport = 0
        if self.province:
            dolar_ton_province = self.transport_local_province / self.tc
            province_transport = ton * dolar_ton_province

        total_logistic_local_transport = (
            province_transport
            + desconsolidation
            + transport_local
            + self.freight
            + self.insurage
        )

        self.desconsolidation = desconsolidation
        self.transport_local = transport_local
        self.province_transport = province_transport
        self.total_logistic = total_logistic_local_transport

    def summary(self):
        self.run_all()
        return {
            "hscode": self.hscode,
            "fob": self.fob,
            "cif": self.cif,
            "insurage": self.insurage,
            "freight": self.freight,
            "freight_taxes": self.freigth_taxes,
            "ad_valorem": self.ad_valorem,
            "igv": self.igv,
            "ipm": self.ipm,
            "antidupping": self.antidupping,
            "perception": self.perception,
            "total_taxes": self.total_taxes,
            "desconsolidation": self.desconsolidation,
            "transport_local": self.transport_local,
            "province": self.province,
            "province_transport": self.province_transport,
            "total_logistic": self.total_logistic,
            "first_import": self.first_import,
            "units": self.units,
            "user": self.user,
        }


variable = asdict(VariableCosts())
taxes = asdict(TaxesHSCode())
form = asdict(
    InputForm(
        None,
        1000,
        4.85,
        1000,
        2.5,
    )
)

# a = Info(**form, **taxes, **variable).summary()
# print(a)
