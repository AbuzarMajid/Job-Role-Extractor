import logging

logging.basicConfig(
    format="[ %(asctime)s ] %(filename)s %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Create a console handler and set the level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("[ %(asctime)s ] %(filename)s %(lineno)d %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
