import pandas as pd


# custom function to remove null values from data frame.
def drop_na(df: pd.DataFrame, subset: list | None = None) -> pd.DataFrame:
    if subset:
        return df.dropna(subset=subset)
    return df.dropna()

# custom function to remove duplicate entries from data frame.
def drop_duplicates(df: pd.DataFrame, subset: list | None = None) -> pd.DataFrame:
    if subset:
        return df.drop_duplicates(subset=subset)
    return df.drop_duplicates()

# base etl processor class that defines required variables & base etl methods for child classes.
class BaseETLProcessor:
    def __init__(self, file_path: str, engine, countries: list[str]):
        self.file_path = file_path
        self.engine = engine
        self.countries = countries

    def extract(self):
        return pd.read_csv(self.file_path, delimiter="|")

    def transform(self) -> pd.DataFrame:
        raise NotImplementedError(
            "Subclasses must implement the etl class for specific table types."
        )

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(
            name=self.table_name, con=self.engine, if_exists="append", index=False
        )

# child etl processor class designed to perform etl processes for country database table
class CountryETLProcessor(BaseETLProcessor):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        # mapping for country names that match to country codes
        country_codes = {
            "AD": "Andorra",
            "AE": "United Arab Emirates",
            "AF": "Afghanistan",
            "AG": "Antigua and Barbuda",
            "AI": "Anguilla",
            "AL": "Albania",
            "AM": "Armenia",
            "AO": "Angola",
            "AQ": "Antarctica",
            "AR": "Argentina",
            "AS": "American Samoa",
            "AT": "Austria",
            "AU": "Australia",
            "AW": "Aruba",
            "AX": "Aland Islands",
            "AZ": "Azerbaijan",
            "BA": "Bosnia and Herzegovina",
            "BB": "Barbados",
            "BD": "Bangladesh",
            "BE": "Belgium",
            "BF": "Burkina Faso",
            "BG": "Bulgaria",
            "BH": "Bahrain",
            "BI": "Burundi",
            "BJ": "Benin",
            "BL": "Saint Barthélemy",
            "BM": "Bermuda",
            "BN": "Brunei",
            "BO": "Bolivia",
            "BQ": "Caribbean Netherlands",
            "BR": "Brazil",
            "BS": "The Bahamas",
            "BT": "Bhutan",
            "BV": "Bouvet Island",
            "BW": "Botswana",
            "BY": "Belarus",
            "BZ": "Belize",
            "CA": "Canada",
            "CC": "Cocos (Keeling) Islands",
            "CD": "Democratic Republic of the Congo",
            "CF": "Central African Republic",
            "CG": "Republic of the Congo",
            "CH": "Switzerland",
            "CI": "Cote d'Ivoire",
            "CK": "Cook Islands",
            "CL": "Chile",
            "CM": "Cameroon",
            "CN": "China",
            "CO": "Colombia",
            "CR": "Costa Rica",
            "CU": "Cuba",
            "CV": "Cape Verde",
            "CW": "Curaçao",
            "CX": "Christmas Island",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DE": "Germany",
            "DJ": "Djibouti",
            "DK": "Denmark",
            "DM": "Dominica",
            "DO": "Dominican Republic",
            "DZ": "Algeria",
            "EC": "Ecuador",
            "EE": "Estonia",
            "EG": "Egypt",
            "EH": "Western Sahara",
            "ER": "Eritrea",
            "ES": "Spain",
            "ET": "Ethiopia",
            "FI": "Finland",
            "FJ": "Fiji",
            "FK": "Falkland Islands",
            "FM": "Federated States of Micronesia",
            "FO": "Faroe Islands",
            "FR": "France",
            "GA": "Gabon",
            "GB": "United Kingdom",
            "GD": "Grenada",
            "GE": "Georgia",
            "GF": "French Guiana",
            "GG": "Bailiwick of Guernsey",
            "GH": "Ghana",
            "GI": "Gibraltar",
            "GL": "Greenland",
            "GM": "The Gambia",
            "GN": "Guinea",
            "GP": "Guadeloupe",
            "GQ": "Equatorial Guinea",
            "GR": "Greece",
            "GS": "South Georgia and the South Sandwich Islands",
            "GT": "Guatemala",
            "GU": "Guam",
            "GW": "Guinea-Bissau",
            "GY": "Guyana",
            "HK": "Hong Kong",
            "HM": "Heard Island and McDonald Islands",
            "HN": "Honduras",
            "HR": "Croatia",
            "HT": "Haiti",
            "HU": "Hungary",
            "ID": "Indonesia",
            "IE": "Republic of Ireland",
            "IL": "Israel",
            "IM": "Isle of Man",
            "IN": "India",
            "IO": "British Indian Ocean Territory",
            "IQ": "Iraq",
            "IR": "Iran",
            "IS": "Iceland",
            "IT": "Italy",
            "JE": "Jersey",
            "JM": "Jamaica",
            "JO": "Jordan",
            "JP": "Japan",
            "KE": "Kenya",
            "KG": "Kyrgyzstan",
            "KH": "Cambodia",
            "KI": "Kiribati",
            "KM": "Comoros",
            "KN": "Saint Kitts and Nevis",
            "KP": "North Korea",
            "KR": "South Korea",
            "KW": "Kuwait",
            "KY": "Cayman Islands",
            "KZ": "Kazakhstan",
            "LA": "Lao People's Democratic Republic",
            "LB": "Lebanon",
            "LC": "Saint Lucia",
            "LI": "Liechtenstein",
            "LK": "Sri Lanka",
            "LR": "Liberia",
            "LS": "Lesotho",
            "LT": "Lithuania",
            "LU": "Luxembourg",
            "LV": "Latvia",
            "LY": "Libya",
            "MA": "Morocco",
            "MC": "Monaco",
            "MD": "Moldova",
            "ME": "Montenegro",
            "MF": "Collectivity of Saint Martin",
            "MG": "Madagascar",
            "MH": "Marshall Islands",
            "MK": "North Macedonia",
            "ML": "Mali",
            "MM": "Myanmar",
            "MN": "Mongolia",
            "MO": "Macau",
            "MP": "Northern Mariana Islands",
            "MQ": "Martinique",
            "MR": "Mauritania",
            "MS": "Montserrat",
            "MT": "Malta",
            "MU": "Mauritius",
            "MV": "Maldives",
            "MW": "Malawi",
            "MX": "Mexico",
            "MY": "Malaysia",
            "MZ": "Mozambique",
            "NA": "Namibia",
            "NC": "New Caledonia",
            "NE": "Niger",
            "NF": "Norfolk Island",
            "NG": "Nigeria",
            "NI": "Nicaragua",
            "NL": "Kingdom of the Netherlands",
            "NO": "Norway",
            "NP": "Nepal",
            "NR": "Nauru",
            "NU": "Niue",
            "NZ": "New Zealand",
            "OM": "Oman",
            "PA": "Panama",
            "PE": "Peru",
            "PF": "French Polynesia",
            "PG": "Papua New Guinea",
            "PH": "Philippines",
            "PK": "Pakistan",
            "PL": "Poland",
            "PM": "Saint Pierre and Miquelon",
            "PN": "Pitcairn Islands|Pitcairn",
            "PR": "Puerto Rico",
            "PS": "Palestine",
            "PT": "Portugal",
            "PW": "Palau",
            "PY": "Paraguay",
            "QA": "Qatar",
            "RE": "Reunion",
            "RO": "Romania",
            "RS": "Serbia",
            "RU": "Russia",
            "RW": "Rwanda",
            "SA": "Saudi Arabia",
            "SB": "Solomon Islands",
            "SC": "Seychelles",
            "SD": "Sudan",
            "SE": "Sweden",
            "SG": "Singapore",
            "SH": "Saint Helena, Ascension and Tristan da Cunha",
            "SI": "Slovenia",
            "SJ": "Svalbard and Jan Mayen",
            "SK": "Slovakia",
            "SL": "Sierra Leone",
            "SM": "San Marino",
            "SN": "Senegal",
            "SO": "Somalia",
            "SR": "Suriname",
            "SS": "South Sudan",
            "ST": "São Tomé and Príncipe",
            "SV": "El Salvador",
            "SX": "Sint Maarten",
            "SY": "Syria",
            "SZ": "Eswatini",
            "TC": "Turks and Caicos Islands",
            "TD": "Chad",
            "TF": "French Southern and Antarctic Lands",
            "TG": "Togo",
            "TH": "Thailand",
            "TJ": "Tajikistan",
            "TK": "Tokelau",
            "TL": "East Timor",
            "TM": "Turkmenistan",
            "TN": "Tunisia",
            "TO": "Tonga",
            "TR": "Turkey",
            "TT": "Trinidad and Tobago",
            "TV": "Tuvalu",
            "TW": "Taiwan, China",
            "TZ": "Tanzania",
            "UA": "Ukraine",
            "UG": "Uganda",
            "UM": "United States Minor Outlying Islands",
            "US": "United States",
            "UY": "Uruguay",
            "UZ": "Uzbekistan",
            "VA": "Vatican City",
            "VC": "Saint Vincent and the Grenadines",
            "VE": "Venezuela",
            "VG": "British Virgin Islands",
            "VI": "United States Virgin Islands",
            "VN": "Vietnam",
            "VU": "Vanuatu",
            "WF": "Wallis and Futuna",
            "WS": "Samoa",
            "YE": "Yemen",
            "YT": "Mayotte",
            "ZA": "South Africa",
            "ZM": "Zambia",
            "ZW": "Zimbabwe",
        }

        countries_df = df[df["GEO_ID"].isin(self.countries)]
        countries_df = countries_df.rename(columns={"GEO_ID": "country_code"})
        countries_df["country_code"] = countries_df["country_code"].str[-2:]
        countries_df["country_name"] = countries_df["country_code"].map(country_codes)
        country_code_df = drop_duplicates(df=countries_df, subset=["country_code"])
        country_code_df = country_code_df[["country_code", "country_name"]].reset_index(
            drop=True
        )
        return country_code_df

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(name="country", con=self.engine, if_exists="append", index=False)

    def process(self):
        print("Extracting data for country table...")
        txt_df = self.extract()

        print("Transforming data for country table...")
        transformed_df = self.transform(txt_df)
        # print(transformed_df)

        try:
            print("Loading country table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")

# child etl processor class designed to perform etl processes for population range database table
class PopulationRangeETLProcessor(BaseETLProcessor):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        range_variables = [
            "POP0_4",
            "POP5_9",
            "POP10_14",
            "POP15_19",
            "POP20_24",
            "POP25_29",
            "POP30_34",
            "POP35_39",
            "POP40_44",
            "POP45_49",
            "POP50_54",
            "POP55_59",
            "POP60_64",
            "POP65_69",
            "POP70_74",
            "POP75_79",
            "POP80_84",
            "POP85_89",
            "POP90_94",
            "POP95_99",
            "POP100_",
        ]
        countries_df = df[df["GEO_ID"].isin(self.countries)]
        range_df = countries_df[range_variables]
        range_df = drop_na(range_df, subset=range_variables)

        rename_mapping = {
            "POP0_4": "pop_range_0_4",
            "POP5_9": "pop_range_5_9",
            "POP10_14": "pop_range_10_14",
            "POP15_19": "pop_range_15_19",
            "POP20_24": "pop_range_20_24",
            "POP25_29": "pop_range_25_29",
            "POP30_34": "pop_range_30_34",
            "POP35_39": "pop_range_35_39",
            "POP40_44": "pop_range_40_44",
            "POP45_49": "pop_range_45_49",
            "POP50_54": "pop_range_50_54",
            "POP55_59": "pop_range_55_59",
            "POP60_64": "pop_range_60_64",
            "POP65_69": "pop_range_65_69",
            "POP70_74": "pop_range_70_74",
            "POP75_79": "pop_range_75_79",
            "POP80_84": "pop_range_80_84",
            "POP85_89": "pop_range_85_89",
            "POP90_94": "pop_range_90_94",
            "POP95_99": "pop_range_95_99",
            "POP100_": "pop_range_100",
        }

        range_df = range_df.rename(columns=rename_mapping)

        return range_df

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(
            name="population_range", con=self.engine, if_exists="append", index=False
        )

    def process(self):
        print("Extracting data for population range table...")
        txt_df = self.extract()

        print("Transforming data for population range table...")
        transformed_df = self.transform(txt_df)
        # print(transformed_df)

        try:
            print("Loading population range table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")

# child etl processor class designed to perform etl processes for population data database table
class PopulationDataETLProcessor(BaseETLProcessor):
    def extract(self) -> pd.DataFrame:
        with self.engine.connect() as connection:
            country_df = pd.read_sql(
                "select country_id, country_code from country", connection
            )
            range_df = pd.read_sql("select * from population_range", connection)

        full_df = pd.read_csv(self.file_path, delimiter="|")

        return country_df, range_df, full_df

    def transform(
        self, country_df: pd.DataFrame, range_df: pd.DataFrame, full_df: pd.DataFrame
    ):
        country_df = country_df.rename(columns={"country_code": "GEO_ID"})

        range_rename_mapping = {
            "pop_range_0_4": "POP0_4",
            "pop_range_5_9": "POP5_9",
            "pop_range_10_14": "POP10_14",
            "pop_range_15_19": "POP15_19",
            "pop_range_20_24": "POP20_24",
            "pop_range_25_29": "POP25_29",
            "pop_range_30_34": "POP30_34",
            "pop_range_35_39": "POP35_39",
            "pop_range_40_44": "POP40_44",
            "pop_range_45_49": "POP45_49",
            "pop_range_50_54": "POP50_54",
            "pop_range_55_59": "POP55_59",
            "pop_range_60_64": "POP60_64",
            "pop_range_65_69": "POP65_69",
            "pop_range_70_74": "POP70_74",
            "pop_range_75_79": "POP75_79",
            "pop_range_80_84": "POP80_84",
            "pop_range_85_89": "POP85_89",
            "pop_range_90_94": "POP90_94",
            "pop_range_95_99": "POP95_99",
            "pop_range_100": "POP100_",
        }

        range_df = range_df.rename(columns=range_rename_mapping)

        full_df = full_df[full_df["GEO_ID"].isin(self.countries)]
        full_df["GEO_ID"] = full_df["GEO_ID"].str[-2:]
        full_df = full_df.rename(
            columns={"#YR": "year", "MEDAGE": "median_age", "POP": "population_total"}
        )

        range_variables = [
            "POP0_4",
            "POP5_9",
            "POP10_14",
            "POP15_19",
            "POP20_24",
            "POP25_29",
            "POP30_34",
            "POP35_39",
            "POP40_44",
            "POP45_49",
            "POP50_54",
            "POP55_59",
            "POP60_64",
            "POP65_69",
            "POP70_74",
            "POP75_79",
            "POP80_84",
            "POP85_89",
            "POP90_94",
            "POP95_99",
            "POP100_",
        ]

        full_range_df = full_df.merge(
            range_df[["pop_range_id"] + range_variables], on=range_variables, how="left"
        )
        full_country_df = full_df.merge(
            country_df[["country_id", "GEO_ID"]], on="GEO_ID", how="left"
        )

        full_range_country_df = full_range_df.merge(
            full_country_df[["country_id", "GEO_ID"]], on="GEO_ID", how="inner"
        )
        full_range_country_df = full_range_country_df.drop_duplicates()
        final_df = full_range_country_df[
            ["year", "median_age", "population_total", "country_id", "pop_range_id"]
        ]
        final_df = final_df.drop_duplicates().dropna().reset_index(drop=True)

        return final_df

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(
            name="population_data", con=self.engine, if_exists="append", index=False
        )

    def process(self):
        print("Extracting data for population data table...")
        country_df, range_df, full_df = self.extract()

        print("Transforming data for population data table...")
        transformed_df = self.transform(
            country_df=country_df, range_df=range_df, full_df=full_df
        )

        try:
            print("Loading population data table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")
