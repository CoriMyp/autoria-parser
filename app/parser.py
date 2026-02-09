import asyncio
import random as rd
from datetime import datetime as dt

import api, utils
	

async def process_auto(session, auto_id: int, auto_link: str):
	await asyncio.sleep(rd.uniform(0.1, 1.0))

	data = await api.fetch_auto(session, auto_id, auto_link)
	if not data: return

	auto = {
		"auto_id": auto_id,
		"url": "",
		"title": "",
		"price_usd": 0,
		"odometer": 0,
		"username": "",
		"phone_number": 0,
		"image_url": "",
		"images_count": 0,
		"car_number": "",
		"car_vin": "",
		"datetime_found": dt.now().date()
	}

	templates = data.get("templates", [])
	additionalParams = data.get("additionalParams", {})
	ldJSON = data.get("ldJSON", {})

	phone_data = additionalParams.get("phone", {}).get("data", [])
	templates_data = utils.get_data_from_templates(templates)

	auto["url"] = additionalParams.get("link", "")
	auto["title"] = additionalParams.get("title", "")
	auto["price_usd"] = ldJSON.get("offers", {}).get("price", 0)
	auto["odometer"] = ldJSON.get("mileageFromOdometer", {}).get("value", 0)
	auto["username"] = additionalParams.get("owner", {}).get("name", "")
	auto["phone_number"] = await utils.get_phone_number(session, auto_id, phone_data)
	auto["image_url"] = additionalParams.get("mainPhoto", {}).get("src", "")
	auto["images_count"] = templates_data.get("images_count", 0)
	auto["car_number"] = templates_data.get("car_number", "")
	auto["car_vin"] = ldJSON.get("autoIdentificationNumber", "")

	return auto


async def process_page(session, page_num: int):
	data = await api.fetch_page(session, page_num)
	if not data:
		return []

	auto_ids = {
		int(v["id"].replace("Auto", "")): v["component"]["advertisementCard"]["data"]["link"]
		for v in data
		if v["id"].startswith("Auto")
	}

	return auto_ids


async def process_all_autos(session, auto_ids: list):
	tasks = [process_auto(session, vid, vlink) for vid, vlink in auto_ids.items()]
	results = await asyncio.gather(*tasks, return_exceptions=True)

	return [v for v in results if v and not isinstance(v, Exception)]
