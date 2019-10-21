# corporateZ
Analyzing open data of Ministry of Corporate Affairs **( M.C.A. )**, Govt. of India to get deeper insight ( in District, State & Country Level ), with :heart:

## Data Source
All data upon which following analysis work will be done, is collected from [here](https://data.gov.in/).

Dataset upon which I'm working, was last updated on _21-04-2018_ ( as mentioned on Open Data Portal of India ).

## Analysis
- [x] [Haryana](docs/haryana.md)
- [x] [Himachal Pradesh](docs/himachalpradesh.md)
- [x] [Jammu & Kashmir](docs/jammuandkashmir.md)
- [x] [Jharkhand](docs/jharkhand.md)
- [x] [Karnataka](docs/karnataka.md)
- [x] [Karala](docs/kerala.md)
- [x] [Lakshadweep](docs/lakshadweep.md)
- [x] [MadhyaPradesh](docs/madhyapradesh.md)
- [x] [Maharashtra](docs/maharashtra.md)
- [x] [Manipur](docs/manipur.md)
- [x] [Meghalaya](docs/meghalaya.md)
- [x] [Mizoram](docs/mizoram.md)
- [x] [Nagaland](docs/nagaland.md)
- [x] [Odisha](docs/odisha.md)
- [x] [Puducherry](docs/puducherry.md)
- [x] [Punjab](docs/punjab.md)
- [x] [Rajasthan](docs/rajasthan.md)
- [x] [Sikkim](docs/sikkim.md)
- [x] [Tamilnadu](docs/tamilnadu.md)
- [x] [Telengana](docs/telengana.md)
- [x] [Tripura](docs/tripura.md)
- [x] [Uttarakhand](docs/uttarakhand.md)
- [x] [Uttar Pradesh](docs/uttarpradesh.md)
- [x] [West Bengal](docs/westbengal.md)


## Status of Companies all over India
Below is a list of company statuses, which show percentage of its presence in different state(s) in form of BAR chart _( as of 21-04-2018 )_
### Active
![active_companies_all_over_India](allCompanyStatusPlots/mca_all_active_companies.png)
### Strike Off
![strike_off_companies_all_over_India](allCompanyStatusPlots/mca_all_strike_off_companies.png)
### Under Process of Striking Off
![under_process_of_striking_off_companies_all_over_India](allCompanyStatusPlots/mca_all_under_process_of_striking_off_companies.png)
### Not Available for e-Filing
![not_available_for_efiling_companies_all_over_India](allCompanyStatusPlots/mca_all_not_available_for_efiling_companies.png)
### Amalgamated
![amalgamated_companies_all_over_India](allCompanyStatusPlots/mca_all_amalgamated_companies.png)
### Under Liquidation
![under_liquidation_companies_all_over_India](allCompanyStatusPlots/mca_all_under_liquidation_companies.png)

## Email Service(s) used by Companies in India
Following PIE chart tries to pictorially depict, which email service provider(s) are in use at which percentage by **1407239**
companies _( for which we had Ministry of Corporate Affairs, Govt. of India open data regarding all companies registered in various states of India )_ spread across several parts of India.

For keeping things simple, I extracted top 10 email service provider(s) being used by Companies & generated a PIE chart for them, showing their percentage of usage.

![email_service_used_by_companies_in_India](./plots/mca_email_service_used_by_companies.png)

## Companies Registered under various RoC(s)
Here I tried to extract how many companies are registered under which RoC _( Registrar of Companies )_ 
and plotted that into BAR chart

Currently our dataset is having **27 RoCs** across India. Percentage of companies registered across these RoCs is as follows

- RoC-Delhi ( 20.4109% )
- RoC-Mumbai ( 16.3580% )
- RoC-Kolkata ( 11.2028% )
- RoC-Hyderabad ( 7.1035% )
- RoC-Chennai ( 6.2814% )
- RoC-Bangalore ( 5.9830% )
- RoC-Ahmedabad ( 5.4137% )
- RoC-Kanpur ( 5.2838% )
- RoC-Pune ( 3.5978% )
- RoC-Jaipur ( 3.0764% )
- ROC-Ernakulam ( 2.6974% )
- RoC-Chandigarh ( 2.4802% )
- RoC-Gwalior ( 2.0502% )
- RoC-Patna ( 1.6143% )
- RoC-Coimbatore ( 1.4225% )
- RoC-Cuttack ( 1.3115% )
- RoC-Shillong ( 0.8016% )
- RoC-Jharkhand ( 0.7005% )
- RoC-Chhattisgarh ( 0.5282% )
- RoC-Goa ( 0.4871% )
- RoC-Uttarakhand ( 0.3875% )
- RoC-Himachal Pradesh ( 0.3281% )
- RoC-Jammu ( 0.2914% )
- RoC-Pondicherry ( 0.1822% )
- RCAND ( 0.0058% )
- RCDMM ( 0.0004% )
- RCSRI ( 0.0001% )

![companies_registered_under_various_RoC(s)](./plots/mca_company_registration_under_roc.png)

## Registration of Companies around Years ( all over India )
Following diagram shows, rate of companies being registered over the years _( starting from 1900 )_ across different states of India
![registration_of_companies_around_years_across_different_states_India](./plots/registration_of_companies_around_years_all_india.png)

**More to come ...** :wink:
