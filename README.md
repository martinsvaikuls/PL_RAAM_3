Grupas Projekts

Projekta Apraksts (Visjaunākā versija, jo vieglāk kopā strādāt):
https://docs.google.com/document/d/1RupNSbhbTdmFWhBfS7ib3eVyIZ9KbkIEJG7z2fsYb4Q/edit?usp=sharing

# PROJEKTĒŠANAS PĀRSKATS

## IEVADS

### Problēmas nostādne

Kreklu apdrukas uzņēmums saņem pasūtījumus, katrā no tiem ir:
- krekla izmērs (S, M, L, XL);
- krāsa;
- daudzums;
- pasūtījuma izpildes termiņš.


Ir pieejamas vairākas apdrukas iekārtas, katra ar savu veiktspēju un izmaksu lielumu, tāpēc jāplāno resursu patēriņš tā, lai ievērotu termiņu, izpildītu pasūtījumu pilnvērtīgi un samazinātu izmaksas un apdrukas iekārtu gaidīšanu. Rezultātā ir jāatrod optimālais pasūtījumu izpildes plāns, kurš nosaka, kā jādarbina iekārtas, lai sasniegtu šo mērķi.

### Darba un novērtēšanas mērķis

#### Darba mērķis
Izveidot risinājumu problēmai, veicot analīzi par esošajiem risinājumiem, algoritmiem, tehnoloģijas stekiem.

#### Novērtēšanas mērķis


## LĪDZĪGO RISINĀJUMU PĀRSKATS

### Printful
Printful ir drukas pēc pieprasījuma (print-on-demand) uzņēmums, kas piedāvā uzņēmumiem drēbju, krūzes un mākslas darbu printēšanu un piegādi uz pasūtītāja adresi no jebkura interneta veikala.

**Darbības princips** - lietotājs izveido dizainu, izvēlas produktu, uz kura drukāt dizainu, veic pasūtījumu, kas automātiski tiek nosūtīts Printful sistēmai. Printful izgatavo dizainu savā ražotnē vai sadarbības centrā un piegādā to gala klientam.

Printful ir iespējams integrēt ar Shopify, Etsy, eBay, Amazon, kā arī izveidot API integrācijas.

### Printify
Printify ir drukas pēc pieprasījuma (print-on-demand) uzņēmums, kas ļauj uzņēmumiem un e-komercijas veikalu īpašniekiem pārdot produktus ar savu dizainu bez nepieciešamības pašiem uzturēt noliktavu vai printerus.

**Darbības princips** - lietotājs izveido dizainu, augšupielādē to sistēmā, izvēlas produktu uz kā vēlas drukāt augšupielādēto dizainu - t-kreklus, krūzes, somas, apavus u.c. Kad klients veic pasūtījumu, Printify automātiski nodod informāciju izvēlētajam drukas partnerim (Print Provider). Produkts tiek izgatavots un piegādāts gala klientam. Pārdevējam nav jāuzglabā krājumi vai jāapstrādā piegādes.

Printify ir iespējams integrēt ar e-komercijas platformām, piemēram, Shopify, Etsy, eBay u.c. Ir iespējams arī izveidot API integrācijas, ja ir nepieciešams savienot ar pielāgotu sistēmu vai CRM.

### TeeSpring (Spring)
TeeSpring, pārdēvēts par Spring, ir drukas pēc pieprasījuma un sociālās komercijas platforma, kas ir orientēta satura radītājiem (YouTube, TikTok, influenceriem), jo ļauj viegli radīt personalizētus produktus, integrējot tos ar populārām sociālo tīklu platformām. Lietotāji var paši veidot savu dizainu priekš t-krekla.

**Darbības princips** - lietotājs izveido vai augšupielādē savu dizainu, izvēlas produktu, uz kura drukāt, izveido tiešsaistes veikalu, kur publicēt gatavos produktus. Kad tiek saņemts pasūtījums, Spring nodrošina tā drukāšanu, piegādi un klientu apkalpošanu, taču klientam pašam vajag reklamēt savu produktu.

Spring ir iespējams integrēt ar YouTube Merch Shelf, TikTok Shopping, Instagram Shopping u.c. Arī iespējams veidot API integrācijas.

### CopyPro
CopyPro ir viens no vadošajiem drukas un poligrāfijas pakalpojumu sniedzējiem Latvijā. Copy Pro piedāvā gan klasiskos drukas pakalpojumus - dažādi kopēšanas, drukāšanas, iesiešanas, laminēšanas un citi ikdienai, mācībām un biznesam noderīgi pakalpojumi, gan arī modernus risinājumus - reklāmai, zīmolvadībai un vizuālajai komunikācijai - T kreklu apdruka korporatīvajiem pasākumiem, ballītēm, dāvanām un arī ikdienai.

Krekli tiek apdrukāti DTG drukas tehnoloģijā, kas nodrošina apģērbu noturīgu un kvalitatīvu apdruku, vai karstā transfēra tehnikā. Apdrukas tehnoloģija tiek izvēlēta atkarībā no apģērba specifikas, auduma sastāva, apdrukas dizaina niansēm u.c. faktoriem. Var izvēlēties kādu no sagatavotajiem dizainiem vai izveidot citu nosūtot failu uz e-pastu ar norādītu krekla krāsu, modeli un izmēru.

Atsķirībā no iepriekšējiem uzņēmumiem CopyPro darbojas kā tiešs drukas pakalpojumu sniedzējs, līdz ar ko integrācijas veidot nav iespējams, taču ir iespējams veidot pielāgotus risinājumus pēc pieprasījuma.

## TEHNISKAIS RISINĀJUMS

### Prasības
a

### Algoritms
a

### Konceptu modelis
a

### Tehnologiju steks
| a | b |
|-------------------|----------------|
| FrontEnd          | 100            |
| BackEnd           | PythonFlask    |
| Datubāze          | google Sheets  |
| Serveris          | Linux Ubunut   |
| Versiju kontrole  | Github         |



### Programmatūras apraksts
a

## NOVĒRTĒJUMS

### Novērtēšanas plāns

Ieejas parametri:

A - krekla izmērs (S M L XL)
B - krāsa (gaiša, tumša)
C - N kreklu daudzums
D - krekla bilde (gaiša, tumša)

Pasūtījuma veidi:

A - A(S), B(gaiša), C(100,1000,10000), D(tumša)

B - A(S), B(tumša), C(100,1000,10000), D(gaiša)

C - A(XL), B(tumša), C(100,1000,10000), D(tumša)

D - A(XL), B(gaiša), C(100,1000,10000), D(gaiša)


| NR | N Kreklu daudzums | Pasūtījuma veids | Vid. Peļņa par kreklu (eur) | Laiks (min) |
|----|-------------------|------------------|-----------------------|-------|
| 1  | 100               |        A          |                       |       |
| 2  | 1 000             |         A         |                       |       |
| 3  | 10 000            |          A        |                       |       |
| 4  | 100               |           B       |                       |       |
| 5  | 1 000             |            B      |                       |       |
| 6  | 10 000            |             B     |                       |       |

### Novērtēšanas rezultāti
a

## SECINĀJUMI
