import pandas as pd
import requests

from typing import Optional, List, Dict, Union

BASE_URL = "https://fipe.parallelum.com.br/api/v2"


def make_request(endpoint: str) -> Union[Dict, List]:
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def get_brands() -> List[Dict]:
    response = make_request("/cars/brands")
    return response if isinstance(response, list) else []


def get_models(brand_id: str) -> List[Dict]:
    response = make_request(f"/cars/brands/{brand_id}/models")

    if isinstance(response, list):
        return response

    if isinstance(response, dict):
        return response.get("models", [])

    return []


def get_years(brand_id: str, model_id: str) -> List[Dict]:
    response = make_request(
        f"/cars/brands/{brand_id}/models/{model_id}/years"
    )

    return response if isinstance(response, list) else []


def get_fipe_price(
    brand_id: str,
    model_id: str,
    year_id: str
) -> Dict:
    response = make_request(
        f"/cars/brands/{brand_id}/models/{model_id}/years/{year_id}"
    )

    return response if isinstance(response, dict) else {}


def get_price_history(
    fipe_code: str,
    year_id: str
) -> List[Dict]:
    if not fipe_code or not year_id:
        return []

    response = make_request(
        f"/cars/{fipe_code}/years/{year_id}/history"
    )

    if isinstance(response, dict):
        return response.get("priceHistory", [])

    if isinstance(response, list):
        return response

    return []


def find_brand_id(brand_name: str) -> Optional[str]:
    for brand in get_brands():
        api_brand_name = str(brand.get("name", "")).strip().lower()

        if api_brand_name == brand_name.strip().lower():
            return brand.get("code")

    return None


def find_model_id(
    brand_id: str,
    model_name: str
) -> Optional[str]:
    for model in get_models(brand_id):
        api_model_name = str(model.get("name", "")).strip().lower()

        if model_name.strip().lower() in api_model_name:
            return model.get("code")

    return None


def find_year_id(
    brand_id: str,
    model_id: str,
    year: str
) -> Optional[str]:
    for vehicle_year in get_years(brand_id, model_id):
        year_name = str(vehicle_year.get("name", "")).strip()
        year_code = str(vehicle_year.get("code", "")).strip()

        if str(year).strip() in year_name:
            return year_code

    return None


def build_vehicle_history_result(
    vehicle_data: Dict,
    fipe_code: str,
    year_id: str,
    history_item: Dict
) -> Dict:
    return {
        "Brand": vehicle_data.get("brand"),
        "Model": vehicle_data.get("model"),
        "Year": vehicle_data.get("modelYear"),
        "Fuel": vehicle_data.get("fuel"),
        "FIPE Code": fipe_code,
        "Year ID": year_id,
        "Current FIPE Price": vehicle_data.get("price"),
        "Current Reference Month": vehicle_data.get("referenceMonth"),
        "History Month": history_item.get("month"),
        "History Price": history_item.get("price"),
        "History Reference": history_item.get("reference")
    }


def build_vehicle_without_history_result(
    vehicle_data: Dict,
    fipe_code: str,
    year_id: str
) -> Dict:
    return {
        "Brand": vehicle_data.get("brand"),
        "Model": vehicle_data.get("model"),
        "Year": vehicle_data.get("modelYear"),
        "Fuel": vehicle_data.get("fuel"),
        "FIPE Code": fipe_code,
        "Year ID": year_id,
        "Current FIPE Price": vehicle_data.get("price"),
        "Current Reference Month": vehicle_data.get("referenceMonth"),
        "History Month": "History not available",
        "History Price": "",
        "History Reference": ""
    }


def build_error_result(
    brand: str,
    model: str,
    year: str,
    error_message: str
) -> Dict:
    return {
        "Brand": brand,
        "Model": model,
        "Year": year,
        "Fuel": "",
        "FIPE Code": "",
        "Year ID": "",
        "Current FIPE Price": "",
        "Current Reference Month": "",
        "History Month": "",
        "History Price": "",
        "History Reference": "",
        "Error": error_message
    }


def process_spreadsheet(
    input_file_path: str,
    output_file_path: str
) -> None:
    dataframe = pd.read_excel(input_file_path)

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
    )

    required_columns = {"brand", "model", "year"}

    if not required_columns.issubset(dataframe.columns):
        missing_columns = required_columns - set(dataframe.columns)

        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    results = []

    for _, row in dataframe.iterrows():
        brand = str(row["brand"]).strip()
        model = str(row["model"]).strip()
        year = str(row["year"]).strip()

        try:
            brand_id = find_brand_id(brand)

            if not brand_id:
                results.append(
                    build_error_result(
                        brand,
                        model,
                        year,
                        "Brand not found"
                    )
                )
                continue

            model_id = find_model_id(brand_id, model)

            if not model_id:
                results.append(
                    build_error_result(
                        brand,
                        model,
                        year,
                        "Model not found"
                    )
                )
                continue

            year_id = find_year_id(
                brand_id,
                model_id,
                year
            )

            if not year_id:
                results.append(
                    build_error_result(
                        brand,
                        model,
                        year,
                        "Year not found"
                    )
                )
                continue

            vehicle_data = get_fipe_price(
                brand_id,
                model_id,
                year_id
            )

            fipe_code = vehicle_data.get("codeFipe")

            price_history = get_price_history(
                fipe_code,
                year_id
            )

            if price_history:
                for history_item in price_history:
                    results.append(
                        build_vehicle_history_result(
                            vehicle_data,
                            fipe_code,
                            year_id,
                            history_item
                        )
                    )
            else:
                results.append(
                    build_vehicle_without_history_result(
                        vehicle_data,
                        fipe_code,
                        year_id
                    )
                )

        except requests.exceptions.RequestException as request_error:
            results.append(
                build_error_result(
                    brand,
                    model,
                    year,
                    f"API Error: {str(request_error)}"
                )
            )

        except Exception as error:
            results.append(
                build_error_result(
                    brand,
                    model,
                    year,
                    str(error)
                )
            )

    result_dataframe = pd.DataFrame(results)

    result_dataframe.to_excel(
        output_file_path,
        index=False
    )

    print(f"Spreadsheet successfully generated: {output_file_path}")