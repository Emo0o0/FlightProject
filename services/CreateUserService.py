from Flight_Project.entities.Country import Country
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.UsersRepository import UserRepository

repo_manager = RepositoryManager()
countries_repo = CountriesRepository(repo_manager)
user_repo = UserRepository(repo_manager, countries_repo)

countries_repo.create_table()
user_repo.create_table()

# country = Country(name="Bulgaria", country_code="BG")
# print(countries_repo.save(country))
print(countries_repo.fetch_one(1))
