# Simulation Tooling
### Freek Gerrits Jans & Thijs van den Berg

## Verkeerslicht simulaties op een kruispunt
Deze code simuleert het veranderen van een stoplicht van `groen` naar `geel` naar `rood`.
Tevens wordt het oversteken van auto's gesimuleerd. Het systeem let op of auto's door rood rijden
en of zijn langer dan een bepaalde tijd door rood rijden.

Voor het stoplicht zijn voor ieder van de drie _states_ de duur in te stellen.
Voor het stoplicht is de waarde `grens` standaard ingesteld op `2`.
Dit wilt zeggen dat iedere auto die na meer dan `2` perioden nog steeds in rood is, de grens heeft overschreden.
Het overschrijden van de grens kan op verschillende manieren worden geïnterpreteerd.
Nét door rood rijden vormt bijvoorbeeld geen significant risico terwijl een langere tijd door
rood rijden wel gevaarlijk kan zijn. Deze waarde is vrij voor de gebruiker om aan te passen.

Voor iedere auto kan het aantal levens worden ingesteld. Dit maakt het, in combinatie met de andere
mee te geven argumenten, mogelijk om verschillende scenario's te testen en simuleren. 

Iedere auto sluit achteraan aan in de `wachtrij`. Het stoplicht heeft een capaciteit welke
door de gebruiker kan worden aangepast. Zodra het stoplicht groen is, kunnen niet meer auto's
tegelijk oversteken dan in de `wachtrij` is gedefinieerd. Zodra een auto is overgestoken, schuift
de wachtrij een plekje op.

## Bronvermelding:
- [https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html]
