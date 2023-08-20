# cannabis-api
A fastapi that maintains a record of cannabis strains and basic information


# Running Locally
For now this is still in development, to run it locally you need docker and docker-compose.

This also is using [Doppler](https://doppler.com/join?invite=524473B9) for secrets/env management, you would need to set that up and do `doppler login` and `doppler setup` from the cli and select your dev env for example then run:

`doppler run -- docker-compose up -d --build` to bring up the stack and inject the env vars/secrets.

If you are not using doppler and don't want to, then just set all of the env vars in the `docker-compose.yml` file to actual values.

On first build of this code this had to be ran to create the version upgrade file:

`docker-compose exec api alembic revision --autogenerate -m "init"`

Once up you also need to run initial migrations for it to setup to the DB:

`docker-compose exec api alembic upgrade head`

Now if everything is working correctly you should be able to go to `http://localhost:8004/docs` and see the swagger API/docs for the project.

# Creating New Migration
If you are adding a new object to the schema, etc you will need to run:

`docker-compose exec api alembic revision -m "add whatever to schema"`

Then run the following to apply the migration:

`docker-compose exec api alembic upgrade head`

You can look at the [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html) for more information.
