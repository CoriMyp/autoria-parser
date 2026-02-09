from pydantic_settings import BaseSettings, SettingsConfigDict
import fake_useragent as fake_ua


class Settings(BaseSettings):
	POSTGRES_USER: str = "postgres"
	POSTGRES_PASSWORD: str = "postgres"
	POSTGRES_DB: str = "postgres"
	POSTGRES_HOST: str = "localhost"
	DATABASE_URL: str | None = None

	PAGES_COUNT: int = 5000
	CARS_COUNT: int = 500
	TIME_HOURS: int = 12
	TIME_MINS: int = 0


	model_config = SettingsConfigDict(env_file=".env", extra="ignore")

	def get_database_url(self) -> str:
		if self.DATABASE_URL:
			return self.DATABASE_URL
		return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"


settings = Settings()

HEADERS = {
	"Accept": "*/*",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Referer": "https://auto.ria.com/",
	"x-ria-source": "vue3-1.42.2",
	"Sec-GPC": "!",
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-origin",
	"Connection": "keep-alive",
	"Cookie": """ab_redesign=1; ab_test_new_pages=1; g_state={"i_l":1,"i_ll":1770329781830,"i_b":"L9i8R8GQb2pGgboAmh3PXDO3LevNoBI9Fhq2EhPHS/Q","i_e":{"enable_itp_optimization":17}}; ui=db89fb0e287810f2; bffState={"videoData":[{"id":"38429539","type":"UsedAuto"},{"id":"36825857","type":"UsedAuto"},{"id":"39064943","type":"UsedAuto"},{"id":"38203854","type":"UsedAuto"},{"id":"38024388","type":"UsedAuto"},{"id":"37591365","type":"UsedAuto"}]}; PSP_ID=5d1aababcda6a4613fee9febea27b8df037bcd0bf2bf1bd37eacd9301d6b54bc16145584; showNewFeatures=7; extendedSearch=1; gdpr=[2,3]; chk=1; _504c2=http://10.42.16.171:3000; ria_sid=29092264711745; informerIndex=1; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiI1ZDFhYWJhYmNkYTZhNDYxM2ZlZTlmZWJlYTI3YjhkZjAzN2JjZDBiZjJiZjFiZDM3ZWFjZDkzMDFkNmI1NGJjMTYxNDU1ODQiLCJ1c2VySWQiOjE2MTQ1NTg0LCJpYXQiOjE3NzA2NTEyNjYsImV4cCI6MTc3MDY1NDg2Nn0.UslnVgDNey2xsMcbbB0CUmNJ4UHdyeKfZHRIJ-o9Bms; PHPSESSID=eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjM2ODMyNTMwMDYsIndlYkNsaWVudENvZGUiOjY3ODk1NzI5OCwid2ViQ2xpZW50Q29va2llIjoiZGI4OWZiMGUyODc4MTBmMiIsIl9leHBpcmUiOjE3NzA3Mzc2NzU1NjUsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==""",
	"Priority": "u=4",
	"TE": "trailers",
	"User-Agent": fake_ua.UserAgent().random
}
