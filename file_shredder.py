import os
import secrets
import string


class FileShredder:
    """
    Securely overwrite and delete a file.
    Designed for GUI integration.
    """

    def __init__(
        self,
        passes=3,
        chunk_size=1024 * 1024,
        progress_callback=None,
        log_callback=None,
    ):
        self.passes = passes
        self.chunk_size = chunk_size
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def update_progress(self, value):
        if self.progress_callback:
            self.progress_callback(value)

    def random_chunk(self, size):
        return secrets.token_bytes(size)

    def rename_obfuscate(self, filepath):
        directory = os.path.dirname(filepath)

        random_name = "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(16)
        )

        new_path = os.path.join(directory, random_name)

        self.log("Obfuscating filename...")

        os.rename(filepath, new_path)

        return new_path

    def shred(self, filepath):

        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        file_size = os.path.getsize(filepath)

        self.log(f"File : {filepath}")
        self.log(f"Size : {file_size:,} bytes")
        self.log(f"Overwrite Passes : {self.passes}")

        with open(filepath, "r+b") as file:

            for current_pass in range(self.passes):

                file.seek(0)

                written = 0

                final_pass = current_pass == self.passes - 1

                if final_pass:
                    self.log(f"Pass {current_pass+1}: Writing zeros")
                else:
                    self.log(f"Pass {current_pass+1}: Writing random data")

                remaining = file_size

                while remaining > 0:

                    current_chunk = min(
                        self.chunk_size,
                        remaining,
                    )

                    if final_pass:
                        buffer = b"\x00" * current_chunk
                    else:
                        buffer = self.random_chunk(current_chunk)

                    file.write(buffer)

                    written += current_chunk
                    remaining -= current_chunk

                    overall_progress = int(
                        (
                            (
                                current_pass * file_size
                                + written
                            )
                            /
                            (file_size * self.passes)
                        )
                        * 100
                    )

                    self.update_progress(overall_progress)

                file.flush()
                os.fsync(file.fileno())

        self.log("Renaming file...")

        new_path = self.rename_obfuscate(filepath)

        self.log("Deleting file...")

        os.remove(new_path)

        self.update_progress(100)

        self.log("Secure deletion completed successfully.")