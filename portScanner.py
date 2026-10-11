
from concurrent.futures import ThreadPoolExecutor
import socket
import time

max_workers = 100


# Generate chunks of ports
def generate_port_chunks(port_range):
    parts = port_range.strip().split("-")

    if len(parts) != 2:
        raise ValueError("Enter the port range like 1-100")

    start, end = map(int, parts)

    if not (1 <= start <= end <= 65535):
        raise ValueError(
            "Ports must be between 1 and 65535, with start <= end"
        )

    total = end - start + 1
    chunk_size = (total + max_workers - 1) // max_workers

    chunks = []

    for i in range(start, end + 1, chunk_size):
        chunks.append(range(i, min(i + chunk_size, end + 1)))

    return chunks


# Scan one TCP port
def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex((target, port)) == 0
    except OSError:
        return False


# Scan one chunk of ports
def scan_chunk(target, chunk):
    open_ports = []

    for port in chunk:
        if scan_port(target, port):
            print(f"[+] {port}/tcp open", flush=True)
            open_ports.append(port)

    return open_ports


# Main function
def main():
    try:
        target = input("Target IP/host: ").strip()
        port_range = input("Port range (e.g. 1-100): ").strip()

        if not target:
            print("Error: Target cannot be empty.")
            return

        # Resolve hostname
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            print("Error: Could not resolve the hostname.")
            return

        # Validate and generate chunks
        try:
            chunks = generate_port_chunks(port_range)
        except ValueError as e:
            print(f"Error: {e}")
            return

        total_ports = sum(len(chunk) for chunk in chunks)

        print(f"\nTarget IP: {ip}")
        print(f"Ports to scan: {total_ports}")
        print(f"Worker threads: {max_workers}")
        print("Scanning started...\n", flush=True)

        start_time = time.perf_counter()

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            results = pool.map(
                lambda chunk: scan_chunk(ip, chunk),
                chunks
            )

            open_ports = [
                port
                for chunk_result in results
                for port in chunk_result
            ]

        elapsed = time.perf_counter() - start_time

        print("\n--- Scan Results ---")

        if open_ports:
            print("Open ports:", sorted(open_ports))
        else:
            print("No open TCP ports found.")

        print(f"Ports scanned: {total_ports}")
        print(f"Open ports found: {len(open_ports)}")
        print(f"Time taken: {elapsed:.2f} seconds")

    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    except (ValueError, OSError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
