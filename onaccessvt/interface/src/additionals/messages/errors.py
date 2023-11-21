INVALID_ARGV = (
    "Invalid arguments - Function {fun}() raised the following exception: \n -> {e}\nCheck the data inserted and see the USAGE page for more info"
)
INVALID_FIFO_PATH="FIFO Path inserted is not valid!"
EXCEPTION = "Exception occured - Function {fun}() raised the following exception({file}:{line}): \n -> {e}\n\n"
SCAN = "An error occured during scanning of file: {file}\n -> {e}"
SCAN_TITLE = "OnAccessVT - Scan Error"
TIMEOUT_REACHED = "Partially downloaded file {file} could not be scanned\n -> Timeout reached({timeout} minutes)"
TIMEOUT_EXCEPTION = (
    "Timeout cannot be higher than {max_m} minutes or lower than {min_m} minutes"
)
BUF_LEN = "The length of raw_data isn't what was expected."
ENTRY_NOT_EXISTS = "Entry does not exists anymore"
