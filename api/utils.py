import io
import selectors
import subprocess
import sys


def run_cmd(subprocess_args: list[str]):
    # stolen from:
    # https://gist.github.com/nawatts/e2cdca610463200c12eac2a14efc0bfb#file-capture-and-print-subprocess-output-py

    # Start subprocess
    # bufsize = 1 means output is line buffered
    # universal_newlines = True is required for line buffering
    print(f"Running cmd {subprocess_args}")
    process = subprocess.Popen(
        subprocess_args,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    # Create callback function for process output
    buf = io.StringIO()

    def handle_output(stream, mask):
        # Because the process' output is line buffered, there's only ever one
        # line to read when this function is called
        line = stream.readline()
        buf.write(line)
        sys.stdout.write(line)

    # Register callback for an "available for read" event from subprocess' stdout stream
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, handle_output)

    # Loop until subprocess is terminated
    while process.poll() is None:
        # Wait for events and handle them with their registered callbacks
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

        while True:
            line = process.stdout.readline()
            if not line:
                break
            buf.write(line)
            sys.stdout.write(line)

    # Get process return code
    return_code = process.wait()
    selector.close()

    success = return_code == 0

    # Store buffered output
    output = buf.getvalue()
    buf.close()

    return success, output
