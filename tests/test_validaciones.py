from validaciones import (
    validar_fecha, validar_temperatura, validar_humedad,
    validar_viento, validar_lluvia, validar_zona,
)


def test_fecha_invalida():
    assert validar_fecha("31/02/2026") is False   # no existe
    assert validar_fecha("2026-02-01") is False   # formato incorrecto
    assert validar_fecha("01/01/2999") is False   # futura
    assert validar_fecha("") is False


def test_fecha_valida():
    assert validar_fecha("15/03/2025") is True


def test_humedad_110_rechazada():
    assert validar_humedad(110) is False
    assert validar_humedad(-1) is False
    assert validar_humedad(55) is True


def test_temperatura_80_rechazada():
    assert validar_temperatura(80) is False
    assert validar_temperatura(-20) is True
    assert validar_temperatura(50) is True


def test_entradas_no_numericas():
    assert validar_temperatura("abc") is False
    assert validar_viento(None) is False
    assert validar_lluvia("") is False


def test_viento_y_lluvia():
    assert validar_viento(151) is False
    assert validar_viento(0) is True
    assert validar_lluvia(-0.1) is False
    assert validar_lluvia(0) is True


def test_zona():
    zonas = ["Centro", "Retiro"]
    assert validar_zona("retiro", zonas) is True
    assert validar_zona("Marte", zonas) is False
    assert validar_zona("", zonas) is False
