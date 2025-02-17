ELECTIONS SCRAPER - Projekt 3

Tento projekt je určen pro scrapping volebních výsledků z webové stránky https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ a jejich uložení do souboru CSV.

Požadavky

Před spuštěním je třeba nainstalovat tyto knihovny:

requests

BeautifulSoup4

argparse

Pokud nejsou nainstalovány, můžete je doinstalovat pomocí:

pip install requests beautifulsoup4

Použití

Skript se spouští z terminálu a to pomocí dvou povinných argumentů:

python scraper.py <URL> <soubor.csv>

Argumenty

<URL> - URL adresa obsahující volební výsledky

<soubor.csv> - název CSV souboru, do kterého budou data uložena

Například:

python projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2111" "vysledky_pribram.csv"

Ukázka výstupu CSV souboru:

City Code;City Name;Registered Voters;Issued Ballots;Valid Votes;Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Strana svobodných občanů;Blok proti islam.-Obran.domova;Občanská demokratická aliance;Česká pirátská strana;Unie H.A.V.E.L.;Referendum o Evropské unii;TOP 09;ANO 2011;Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Č.s.str.lid.;Česká strana národně sociální;REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů
0,00;21;32;31,06;22;0;0,00;23;1;0,97;24;3;2,91;25;0;0,00;26;0;0,00;27;0;0,00;28;1;0,97;29;5;4,85;30;0;0,00
4,62;21;37;34,25;22;0;0,00;23;0;0,00;24;4;3,70;25;0;0,00;26;0;0,00;27;0;0,00;28;1;0,92;29;5;4,62;30;0;0,00
5,43;21;348;37,82;22;1;0,10;23;2;0,21;24;30;3,26;25;1;0,10;26;7;0,76;27;2;0,21;28;0;0,00;29;88;9,56;30;1;0,10
4,45;21;65;32,17;22;0;0,00;23;0;0,00;24;15;7,42;25;0;0,00;26;4;1,98;27;0;0,00;28;1;0,49;29;16;7,92;30;1;0,49
5,42;21;40;24,09;22;0;0,00;23;0;0,00;24;9;5,42;25;0;0,00;26;7;4,21;27;0;0,00;28;0;0,00;29;22;13,25;30;0;0,00

Dokumentace funkcí

validate_url(url: str) -> bool

Ověřuje, zda je URL platná a dostupná.

validate_command_line_arguments() -> tuple

Validuje argumenty předávané při spouštění skriptu.

scrape_city_names(url: str) -> tuple

Scrapuje kódy a názvy měst z webu.

get_city_urls(url: str) -> list

Získává URL adresy jednotlivých měst z hlavní stránky voleb.

collect_voter_turnout_data(city_urls: list) -> tuple

Sbírá údaje o volební účasti (počet registrovaných voličů, vydané hlasovací lístky, platné hlasy).

get_political_parties(city_url: str) -> list

Získá seznam politických stran.

collect_vote_counts(city_urls: list, num_parties: int) -> list

Sbírá počty hlasů pro jednotlivé strany.

write_to_csv(file_name: str, city_codes: list, city_names: list, data_collection: tuple, political_parties: list, total_votes: list) -> None

Zapíše výsledky do CSV souboru.

main() -> None

Hlavní funkce, která spouští proces scrappingu a exportu dat.