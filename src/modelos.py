from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Colaborador:
    id: str
    nome: str
    centro_custo: str


@dataclass(frozen=True)
class Periodo:
    competencia: str
    inicio: str
    fim: str


@dataclass(frozen=True)
class Despesa:
    id: str
    data: str
    categoria: str
    descricao: str
    fornecedor: str
    valor: Decimal
    tem_nota_fiscal: bool
    indice: int = 0


@dataclass
class ResultadoDaDespesa:
    id: str
    data: str
    categoria: str
    valor_declarado: float
    valor_reembolsavel: float
    valor_nao_reembolsavel: float
    status: str
    motivo: str


@dataclass
class Resumo:
    total_declarado: float
    total_reembolsavel: float
    total_nao_reembolsavel: float
    total_rejeitado: float
    quantidade_despesas: int


@dataclass
class Alerta:
    tipo: str
    despesas: list[str] = field(default_factory=list)
