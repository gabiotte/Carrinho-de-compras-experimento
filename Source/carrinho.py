from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


CENTAVO = Decimal("0.01")


def _valor_monetario(valor):
    try:
        resultado = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as erro:
        raise ValueError("O preço deve ser um número não negativo.") from erro

    if not resultado.is_finite() or resultado < 0:
        raise ValueError("O preço deve ser um número não negativo.")

    return resultado


class Carrinho:
    def __init__(self):
        self._itens = []

    def adicionar_item(self, nome, preco, quantidade=1):
        if (
            isinstance(quantidade, bool)
            or not isinstance(quantidade, int)
            or quantidade <= 0
        ):
            raise ValueError("A quantidade deve ser um inteiro positivo.")

        preco_decimal = _valor_monetario(preco)

        for item in self._itens:
            if item["nome"] == nome:
                item["quantidade"] += quantidade
                return

        self._itens.append(
            {
                "nome": nome,
                "preco": float(preco_decimal),
                "quantidade": quantidade,
            }
        )

    def remover_item(self, nome):
        for indice, item in enumerate(self._itens):
            if item["nome"] == nome:
                del self._itens[indice]
                return

        raise ValueError(f"Item não encontrado: {nome}")

    def show(self):
        return [item.copy() for item in self._itens]

    def total(self):
        subtotal = sum(
            (
                _valor_monetario(item["preco"]) * item["quantidade"]
                for item in self._itens
            ),
            Decimal("0"),
        ).quantize(CENTAVO, rounding=ROUND_HALF_UP)

        if not subtotal:
            return 0.00

        frete = Decimal("0.00") if subtotal >= Decimal("150") else Decimal("20.00")
        total = (subtotal + frete).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        return float(total)
