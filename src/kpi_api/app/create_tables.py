from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os

class Base(DeclarativeBase):
    pass


class Kpi(Base):
    __tablename__ = "kpis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    month: Mapped[str] = mapped_column(String(50), nullable=False)

    nb_candidats_contactes: Mapped[int] = mapped_column(
        "Nb de candidats contactés",
        Integer,
        default=0,
    )

    nb_entretiens_candidats_salaries: Mapped[int] = mapped_column(
        "Nb d'entretiens candidats Salariés",
        Integer,
        default=0,
    )

    nb_entretiens_candidats_sous_traitants: Mapped[int] = mapped_column(
        "Nb d'entretiens candidats Sous-Traitants",
        Integer,
        default=0,
    )

    nb_candidats_recrutes_salaries: Mapped[int] = mapped_column(
        "Nb de candidats recrutés Salariés ",
        Integer,
        default=0,
    )

    nb_candidats_integres_sous_traitants: Mapped[int] = mapped_column(
        "Nb de candidats intégrés Sous Traitants ",
        Integer,
        default=0,
    )

    nombre_presentations_clients: Mapped[int] = mapped_column(
        "Nombre de présentations clients ",
        Integer,
        default=0,
    )

    nb_refus_cdi_salaries: Mapped[int] = mapped_column(
        "Nb de refus CDI Salariés ",
        Integer,
        default=0,
    )

    nombre_ko_candidat_presentation_client: Mapped[int] = mapped_column(
        "Nombre de KO candidat à la suite d'une présentation client ",
        Integer,
        default=0,
    )

    nombre_ko_client_presentation_client: Mapped[int] = mapped_column(
        "Nombre de KO client à la suite d'une présentation client ",
        Integer,
        default=0,
    )

db_user = os.getenv("DB_API_USER")
db_pwd = os.getenv("DB_API_PWD")
db_name = os.getenv("DB_API_NAME")

DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@database:5432/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)