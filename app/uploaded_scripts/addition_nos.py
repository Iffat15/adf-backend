import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    try:
        logging.info("Starting script: addition_nos.py")

        # Your logic here
        a, b = 5, 7
        result = a + b
        logging.info(f"Result of addition: {result}")

        logging.info("Script completed successfully.")

    except Exception as e:
        logging.error("An error occurred:")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()
