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
Novērtēt pasūtījuma izpildes plāna efektivitāti, balstoties uz iekārtu vidējo noslodzi un pasūtījumu gaidīšanas laiku, atkarībā no pasūtījumu apjoma un iekārtu skaita.

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

### Algoritms
![alt text](https://github.com/martinsvaikuls/PL_RAAM_3/blob/front-end/PicturesForREADME/blokshema.png?raw=true)

### Konceptu modelis
![alt text](https://github.com/martinsvaikuls/PL_RAAM_3/blob/front-end/PicturesForREADME/KonceptuModelis.png?raw=true)

### Tehnologiju steks
| Tehnoloģija | Tehnologijas nosaukums |
|-------------------|----------------|
| FrontEnd          | Javascript     |
| BackEnd           | PythonFlask    |
| Datubāze          | Google Sheets  |
| Serveris          | Azure Web App  |
| Versiju kontrole  | GitHub         |

## NOVĒRTĒJUMS

### Novērtēšanas plāns

Ieejas mainīgie: Pasūtījumu skaits, pieejamo iekārtu skaits.
Novērtēšanas mēri:
	-Vidējais pasūtījuma gaidīšanas laiks;
	-Vidējā kopējā ierīču noslodze;

| Nr. | Pasūtījumu skaits | Printeru skaits | Algoritma ātrums, s | Gaidīšanas laiks, min | Iekārtu noslodze, % |
|-----|-------------------|-----------------|---------------------|-----------------------|---------------------|
| 1.  | 10                | 2               | 0.0025              | 568.22                | 95.45               |
| 2.  | 100               | 5               | 0.0090              | 2325.96               | 98.10               |
| 3.  | 1000              | 10              | 0.1429              | 9741.75               | 99.57               |

### Novērtēšanas rezultāti
Aplūkojot testu rezultātus, var redzēt, ka algoritms iekārtu noslodzi kontrolē ar augtu efektivitāti, visos testos virs 95%. Tomēr pie milzīga pasūtījumu skaita (1000) iekārtu noslodze pietuvojas ļoti tuvu robežai, 99.57%, un ņemot vērā gaidīšanas darbu izpildes sākumā un beigās, var pieņemt, ka pie 1000 pasūtījumiem tiek sasniegts teorētisks limits sistēmai, uz ko norāda arī straujāks pieaugums gaidīšanas laikam, ar vidējo laiku sasniedzam 9741.75 min, jeb aptuveni 6.7 dienas, pat ar palielinātu printeru skaitu. Aplūkojot pārējos gaidīšanas laikus, 1. gadījumā tas sasniedz nieka 568.22 min, jeb 0.39 dienas, bet 2. gadījumā tas sasniedz nu jau daudz augstāku 2325.96 min, jeb 1.61 dienu, kas ir aptuveni četru reižu pieaugums. Lai uzlabotu gaidīšanas laiku, vajadzētu palielināt printeru skaitu, vai izmantot printerus ar augstākiem printēšanas ātrumiem.
