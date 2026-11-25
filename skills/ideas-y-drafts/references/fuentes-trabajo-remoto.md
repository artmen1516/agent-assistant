# Fuentes de vacantes remotas — verificación

Base para la idea `Búsqueda de trabajo remoto — monitoreo y reporte`
(senior/lead/staff, 100% remoto, MX/US/CA). Estos boards cambian sin aviso:
re-verificar conteos al usarlos antes de construir sobre ellos.

## Con API/RSS que funcionan

- **RemoteOK** — `https://remoteok.com/api`
  JSON, ~100 vacantes por fetch. El primer elemento del array es un aviso legal, descartarlo.
  Pide attribution con link a Remote OK (lo exige su ToS).
- **We Work Remotely** — `https://weworkremotely.com/categories/remote-programming-jobs.rss`
  RSS por categoría (~25 ítems cada una); hay más categorías (full-stack, devops, design).
  El elemento `<region>` trae la zona permitida.
- **Himalayas** — `https://himalayas.app/jobs/rss`
  RSS con las ~20 más recientes. `<himalayasJobs:locationRestriction>` trae UN país por vacante:
  el filtro MX/US/CA es directo contra ese campo.
- **Jobicy** — `https://jobicy.com/api/v2/remote-jobs?count=50`
  JSON y el único con seniority normalizado (`jobLevel`: Senior, Director…)
  más `jobGeo`. Parámetros: `count`, `industry`, `geo`.

## Degradadas o sin API

- **Remotive** — su API pública (`/api/remote-jobs`) quedó limitada: ignora `limit`/`search`/
  `category` y devuelve ~14 vacantes totales. No usar como fuente principal; si se recupera,
  era `?category=software-dev&limit=N`.
- **LinkedIn Jobs** — no hay API pública y el scraping va contra sus términos (bloquea y
  suspiende). Vía realista: búsquedas guardadas + alertas por correo (ese correo sí se puede
  parsear), más revisión manual.
- **Wellfound, YC Work at a Startup, HN Who is hiring** — sin API; revisión manual o parsing
  puntual del thread de HN.

## Filtro de geografía (regla práctica)

- «USA only» exige autorización de trabajo en EU: excluir por defecto.
- Aceptan: Worldwide, Anywhere, Americas, LATAM, North America, Mexico,
  y menciones explícitas de contratación en México (EOR o entidad local).
- «Europe only» u otro continente: excluir.
