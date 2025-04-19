#!/usr/bin/env python3

import re
import os
import logging
from collections import defaultdict
import datetime

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting smartd_exporter")

    syslog_path = os.getenv("SYSLOG_PATH", "/var/log/syslog")
    output_path = os.getenv("OUTPUT_PATH", "/var/lib/node_exporter/textfile_collector/smartd.prom")
    timedelta_minutes = int(os.getenv("TIMEDELTA_MINUTES", 10))

    if not os.path.exists(syslog_path):
        raise FileNotFoundError(f"Syslog file not found: {syslog_path}")

    error_counts = defaultdict(int)
    logging.info(f"Reading syslog from: {syslog_path}")
    logging.info(f"Writing metrics to: {output_path}")

    now = datetime.datetime.now()
    scope_since = now - datetime.timedelta(minutes=timedelta_minutes)
    with open(syslog_path) as f:
        for line in f:
            syslog_timestamp = " ".join(line.split()[0:3])
            try:
                log_time = datetime.datetime.strptime(syslog_timestamp, "%b %d %H:%M:%S")
            except ValueError:
                continue
            log_time = log_time.replace(year=now.year)
            if log_time < scope_since:
                continue
            if "smartd" in line and "Currently unreadable (pending) sectors" in line:
                logging.info(f"Processing line: {line.strip()}")
                m = re.search(r'Device: (/dev/\w+)', line)
                if m:
                    dev = m.group(1)
                    error_counts[dev] += 1

    logging.info(f"Found unreadable sectors on {len(error_counts)} device(s)")

    with open(output_path, "w") as f:
        f.write("# HELP smartd_unreadable_sectors Number of unreadable sectors per device\n")
        f.write("# TYPE smartd_unreadable_sectors gauge\n")
        for dev, count in error_counts.items():
            f.write(f'smartd_unreadable_sectors{{device="{dev}"}} {count}\n')

    logging.info("Metrics file written successfully.")

if __name__ == "__main__":
    main()