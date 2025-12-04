from Flight_Project.entities.User import User
from Flight_Project.entities.Country import Country
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.UsersRepository import UsersRepository


repo_manager = RepositoryManager()
countries_repo = CountriesRepository(repo_manager)
user_repo = UsersRepository(repo_manager, countries_repo)

countries_repo.create_table()
user_repo.create_table()

# country = Country(name="Bulgaria", country_code="BG")
# print(countries_repo.save(country))

user = User(
    "e@e",
    "123",
    "Emo",
    "Kolev",
    "12314324",
    countries_repo.fetch_one(1),
    "26:11:2002",
    "789234",
    "yesterday",
)
print(user_repo.save(user))

print(countries_repo.fetch_one(1))
print(user_repo.fetch_one(1))
