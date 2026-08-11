# BUSINESS REQUIREMENTS DOCUMENT
# Tipo: Sistema nuevo
# Arquetipos: Proceso, Recursos escasos
# Fecha: 2026-03-04
# Versión: 2.0 (APROBADA — 3 revisiones de lectura pasadas)

## 1. Objetivo de negocio
[OB-001] Que la panadería reciba y despache pedidos por encargo sin perder ninguno en papel. [CONFIRMADO]

## 2. Alcance
[AL-001] Dentro: toma de pedido, agenda de retiro, aviso al cliente. [CONFIRMADO]
[AL-F-001] Fuera: reparto a domicilio. [CONFIRMADO]

## 3. Actores
[AC-001] Primario: la persona del mostrador. [CONFIRMADO]
[AC-002] Cliente que encarga. [CONFIRMADO]

## 4. Procesos
[PR-001] El cliente encarga por teléfono o en el mostrador. [CONFIRMADO] | MoSCoW: M
[PR-002] Se registra el pedido con producto, cantidad y fecha de retiro. [CONFIRMADO] | MoSCoW: M
[PR-003] Se confirma el pedido al cliente. [CONFIRMADO] | MoSCoW: M
[PR-004] Se entrega el pedido y se cierra. [CONFIRMADO] | MoSCoW: M
[PR-EXC-001] Si el producto se agotó, se avisa y se ofrece cambio de fecha. [CONFIRMADO]

## 5. Reglas de negocio
[RN-001] Un pedido no se acepta con menos de 24 horas de anticipación. [CONFIRMADO] | MoSCoW: M
[RN-002] Los pedidos de más de 20 unidades requieren anticipo. [CONFIRMADO] | MoSCoW: M
[RN-003] El cliente elige nombre, teléfono y forma de aviso desde la lista cerrada de formas de aviso disponibles. [CONFIRMADO] | MoSCoW: M
[RN-004] Un pedido no retirado dentro de las 48 horas siguientes a su fecha se considera abandonado y el producto se libera para venta en vitrina, salvo que el cliente haya pagado anticipo, en cuyo caso se conserva 72 horas y se le avisa por la forma de aviso que eligió, y si tampoco lo retira se registra como pérdida y se descuenta del inventario del día siguiente informando a la persona del mostrador. [CONFIRMADO] | MoSCoW: M
[RN-005] El horario de atención se publica en la puerta. [CONFIRMADO] | MoSCoW: S

## 6. Datos
[DA-IN-001] Pedido: producto, cantidad, fecha de retiro, nombre y teléfono. [CONFIRMADO]
[DA-OUT-001] Comprobante de encargo. [CONFIRMADO]

## 7. Casos borde
[CB-001] El cliente encarga y no deja teléfono. [CONFIRMADO]
[CB-002] Dos clientes encargan lo último disponible al mismo tiempo. [CONFIRMADO]

## 8. Criterios de éxito
[CE-001] Ningún pedido registrado se pierde. [CONFIRMADO] | MoSCoW: M

## 9. Priorización
[PZ-001] La toma de pedido va primero. [CONFIRMADO]

## 10. Restricciones
[RE-001] El mostrador atiende de 7 a 20 horas. [CONFIRMADO]

## 11. Supuestos
[SA-001] La panadería tiene un teléfono fijo operativo. [SUPUESTO]

## 12. Riesgos
[RG-001] Si el mostrador está solo, registrar el pedido compite con atender la fila. [RIESGO]

## 13. Pendientes
(ninguno)

## 14. Bloqueos y alternativas
(ninguno)

## 15. Criterios de aceptación
[CA-001] (cubre: CB-001) Dado un encargo sin teléfono, cuando se intenta registrar, entonces el sistema exige un teléfono antes de aceptarlo. [CONFIRMADO]
[CA-002] (cubre: CB-002) Dado dos encargos simultáneos sobre la última unidad, cuando ambos se confirman, entonces solo uno queda aceptado y el otro recibe el aviso de agotado. [CONFIRMADO]
[CA-003] (cubre: PR-EXC-001) Dado un producto agotado, cuando se avisa al cliente, entonces se le ofrece cambio de fecha. [CONFIRMADO]
[CA-004] (cubre: RN-001) Dado un encargo para dentro de 12 horas, cuando se intenta registrar, entonces se rechaza. [CONFIRMADO]

## 16. Trazabilidad
| OB-001 a RG-001 | §1-§12 | CONFIRMADO |
| SA-001 | §11 | SUPUESTO |

## 17. Handoff
### Arquitectura de Software
- §3 (Actores), §4 (Procesos), §5 (Reglas), §15 (Criterios)

## 18. Registro de investigaciones
(sin investigación)

## 19. Historial de cambios (post-aprobación)
| 2026-03-04 | 2.0 | todos | Aprobación inicial | dueño |
