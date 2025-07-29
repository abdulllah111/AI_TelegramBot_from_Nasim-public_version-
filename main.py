import logging
from src.bot import main
from src.database import initialize_database

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    initialize_database()
    main()