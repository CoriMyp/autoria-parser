from api import fetch_phone


def get_data_from_templates(templates: list):
	result = {
		"images_count": 0,
		"car_number": ""
	}

	def find_by_id(source, tmpl_id):
		return next((t for t in source if t.get("id") == tmpl_id), {})

	main = find_by_id(templates, "main")
	col = find_by_id(main.get("templates", []), "col")

	for item in col.get("templates", []):
		item_id = item.get("id")

		if item_id == "photoSlider":
			result["images_count"] = len(item.get("elements", []))

		elif item_id == "badges":
			plate = find_by_id(item.get("templates", []), "badgesPlateNumber")
			elements = plate.get("elements", [])
			if elements:
				result["car_number"] = elements[0].get("content", "")

	return result


async def get_phone_number(session, auto_id: int, phone_data: list):
	data = await fetch_phone(session, auto_id, phone_data)
	if not data:
		return 0

	phone_str = data.get("additionalParams", {}).get("phoneStr", "")
	phone = phone_str.replace("(", "").replace(")", "").replace(" ", "")

	if not phone.isdigit():
		return 0

	return int("38" + phone)
