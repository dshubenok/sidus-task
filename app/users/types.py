from sqlalchemy import event
from sqlalchemy.databases import postgres
from sqlmodel import SQLModel

prefix = "usr"

usr_gender_type = postgres.ENUM(
    "male",
    "female",
    name=f"{prefix}_gender"
)


@event.listens_for(
    SQLModel.metadata, "before_create"
)
def _create_enums(metadata, conn, **kw):  # noqa: indirect usage
    usr_gender_type.create(conn, checkfirst=True)
