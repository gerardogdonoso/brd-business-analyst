# BUSINESS REQUIREMENTS DOCUMENT
# Tipo: Sistema nuevo
# Arquetipos: Recursos escasos, Regulado
# Fecha: 2026-05-11
# Versión: 4.3 (APROBADA)

## 1. Objetivo de negocio
[OB-001] Que la clínica llene las horas libres que hoy quedan vacías por inasistencia. [CONFIRMADO]

## 2. Alcance
[AL-001] Dentro: agenda, recordatorio, lista de espera. [CONFIRMADO]
[AL-F-001] Fuera: ficha clínica y resultados de exámenes. [CONFIRMADO]

## 3. Actores
[AC-001] Primario: recepción. [CONFIRMADO]
[AC-002] Paciente. [CONFIRMADO]

## 4. Procesos
[PR-001] El paciente reserva hora. [CONFIRMADO] | MoSCoW: M
[PR-002] Se envía recordatorio antes de la hora. [CONFIRMADO] | MoSCoW: M
[PR-003] Si el paciente cancela, la hora se ofrece a la lista de espera. [CONFIRMADO] | MoSCoW: M

## 5. Reglas de negocio
[RN-001] Una hora cancelada con menos de 2 horas de anticipación cuenta como inasistencia. [CONFIRMADO] | MoSCoW: M
[RN-002] El recordatorio se envía una sola vez, 24 horas antes de la hora, y no se repite. [CONFIRMADO] | MoSCoW: M
[RN-003] Tres inasistencias en seis meses suspenden la reserva en línea. [CONFIRMADO] | MoSCoW: M

## 6. Datos
[DA-IN-001] Reserva: paciente, profesional, fecha, hora, canal de aviso. [CONFIRMADO]
[DA-OUT-001] Recordatorio enviado, con fecha y canal. [CONFIRMADO]

## 7. Casos borde
[CB-001] El paciente cambia de teléfono entre la reserva y el recordatorio. [CONFIRMADO]

## 8. Criterios de éxito
[CE-001] Menos horas vacías por inasistencia que antes del sistema. [CONFIRMADO] | MoSCoW: M

## 9. Priorización
[PZ-001] El recordatorio va antes que la lista de espera. [CONFIRMADO]

## 10. Restricciones
[RE-001] No se contacta a pacientes fuera de horario hábil. [CONFIRMADO]

## 11. Supuestos
[SA-001] La clínica mantiene los teléfonos actualizados. [SUPUESTO]

## 12. Riesgos
[RG-001] Un recordatorio que no llega se ve igual que uno ignorado. [RIESGO]

## 13. Pendientes
[PE-001] Confirmar con el abogado si el recordatorio requiere consentimiento previo. [PENDIENTE] | Bloquea: PR-002

## 14. Bloqueos y alternativas
(ninguno)

## 15. Criterios de aceptación
[CA-001] (cubre: RN-001) Dado una cancelación con 1 hora de anticipación, cuando se registra, entonces cuenta como inasistencia. [CONFIRMADO]
[CA-002] (cubre: RN-003) Dado un paciente con tres inasistencias en seis meses, cuando intenta reservar en línea, entonces el sistema no se lo permite. [CONFIRMADO]
[CA-003] (cubre: RN-002) Dado un paciente que no confirmó el primer recordatorio, cuando faltan 3 horas para la hora, entonces se le envía un segundo recordatorio. [CONFIRMADO]
[CA-004] (cubre: CB-001) Dado un paciente que cambió de teléfono, cuando se envía el recordatorio, entonces sale al teléfono vigente. [CONFIRMADO]

## 16. Trazabilidad
| OB-001 a PE-001 | §1-§13 | CONFIRMADO |
| SA-001 | §11 | SUPUESTO |

## 17. Handoff
### Arquitectura de Software
- §3 (Actores), §4 (Procesos), §5 (Reglas), §15 (Criterios)

## 18. Registro de investigaciones
(sin investigación)

## 19. Historial de cambios (post-aprobación)
| 2026-05-11 | 4.0 | todos | Aprobación inicial | dueño |
| 2026-06-02 | 4.3 | RN-002 | El dueño decide que el recordatorio se envía UNA sola vez y no se repite: dos recordatorios molestaban y no subían la asistencia. Antes decía que se reenviaba a las 3 horas si el paciente no confirmaba. | dueño |
