# The South African Gov-ZA SONA multilingual corpus

Give Feedback 📑: [DSFSI Resource Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSf7S36dyAUPx2egmXbFpnTBuzoRulhL5Elu-N1eoMhaO7v10w/formResponse)

## About Dataset
The data set contains state of the nation address from the South African government, maintained by the [Government Communication and Information System (GCIS)](https://www.gcis.gov.za/). Data was scraped from the governments website:
https://www.gov.za/state-nation-address

The datasets contain government cabinet statements in 11 languages, namely:

|  Language  | Code |  Language  | Code |
|------------|------|------------|------|
| English    | (eng) | Sepedi     | (nso) |
| Afrikaans  | (afr) | Setswana   | (tsn) |
| isiNdebele | (nbl) | Siswati    | (ssw) |
| isiXhosa   | (xho) | Tshivenda  | (ven) |
| isiZulu    | (zul) | Xitstonga  | (tso) |
| Sesotho    | (sot) |

The dataset is split by year in text files (/data/raw).

## Number of Aligned Pairs with Cosine Similarity Score >= 0.65

| Pair | Above 0.65 | Pair | Above 0.65 |
| ---- | ---------- | ---- | ------ |
| xho-zul | 3461 | sot-tsn | 3317 |
| sot-nso | 3214 | ssw-zul | 3169 |
| ssw-xho | 3115 | afr-xho | 3178 |
| nso-tsn | 3183 | afr-xho | 3178 |
| ssw-tsn | 2986 | afr-zul | 3009 |
| nbl-ven | 2854 | eng-sot | 3010 |
| nso-tso | 2833 | sot-tso | 2814 |
| sot-xho | 2754 | tso-xho | 2701 |
| eng-nso | 2950 | eng-tsn | 2916 |
| eng-xho | 2826 | eng-zul | 2879 |
| afr-sot | 2711 | sot-zul | 2590 |
| tsn-zul | 2610 | eng-tso | 2803 |
| sot-ssw | 2511 | tsn-xho | 2563 |
| nso-xho | 2519 | tso-zul | 2596 |
| nso-zul | 2534 | tsn-tso | 2497 |
| eng-ssw | 2555 | afr-ssw | 2501 |
| afr-tso | 2346 | afr-nso | 2346 |
| nso-ssw | 2110 | afr-tsn | 2063 |
| afr-eng | 1753 | afr-nbl | 331 |
| afr-ven | 328 | sot-ven | 303 |
| tso-ven | 220 | eng-ven | 218 |
| tsn-ven | 202 | ven-xho | 184 |
| nso-ven | 190 | nbl-ssw | 159 |
| ssw-ven | 147 | nbl-xho | 128 |
| nbl-sot | 118 | ven-zul | 117 |
| nbl-tso | 103 | eng-nbl | 95  |
| nbl-zul | 94  | nbl-tsn | 79  |
| nbl-nso | 71  |

## Disclaimer
This dataset contains machine-readable data extracted from online cabinet statements from the South African government, provided by the Government Communication Information System (GCIS). While efforts were made to ensure the accuracy and completeness of this data, there may be errors or discrepancies between the original publications and this dataset. No warranties, guarantees or representations are given in relation to the information contained in the dataset. The members of the Data Science for Societal Impact Research Group bear no responsibility and/or liability for any such errors or discrepancies in this dataset. The Government Communication Information System (GCIS) bears no responsibility and/or liability for any such errors or discrepancies in this dataset. It is recommended that users verify all information contained herein before making decisions based upon this information.

## Authors
- Vukosi Marivate - [@vukosi](https://twitter.com/vukosi)
- Richard Lastrucci

## Licences
* License for Data - [CC 4.0 BY](LICENSE_data.md)
* Licence for Code - [MIT License](LICENSE)