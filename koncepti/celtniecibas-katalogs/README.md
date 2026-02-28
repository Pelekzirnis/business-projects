# Celtniecibas tehnikas AI katalogs
**Statuss:** Analizets, ilgtermina projekts
**Sakums:** 2026
## Galvena ideja
AI-powered mekletajs celtniecibas tehnikai ar NLP.
Piemers:
Input: "Velos izkast gravi, 2m dzili, 100m gars"
Output: "Jums vajag mini ekskavators 2-3 tonnas"
## Dati avoti
- Technitis katalogs (500-1000 produktu)
- OpenCatalogs/Wikidata
- Producenta PDF (Yanmar, BOMAG, Gehl)
## Arhitektura
Katalogs (JSON) -> Elasticsearch/Weaviate -> LLM Router -> Web UI/API
## Kas jau ir izdarits?
- Dati avoti identificeti
- JSON schema vel nav
- Elasticsearch vel nav uzstadits
## Nakamais solis (3-4 nedelas)
1. Datu vakšana (1 ned.)
2. Elasticsearch setup (2 ned.)
3. UI un LLM router (1 ned.)
## Pedejais updates
28. febr. 2026: Koncepta stadija, dati vel nav vakti
