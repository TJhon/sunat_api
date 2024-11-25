from sqlmodel import create_engine

sqlite_file_name = "data/t3.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args=connect_args,
)
