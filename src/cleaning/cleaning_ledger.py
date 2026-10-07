"""
Cleaning ledger that records REAL transformation counts.

Every cleaning operation must call ledger.log() with the actual
number of rows affected. No hardcoded example strings.
"""
import json
import os
from datetime import datetime


class CleaningLedger:
    """Append-only ledger of data transformations with real counts."""

    def __init__(self, path=None):
        if path is None:
            path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "data", "processed", "cleaning_ledger.json"
            )
        self.path = path
        self.entries = []
        if os.path.exists(path):
            with open(path) as f:
                self.entries = json.load(f)

    def log(self, dataset, column, transformation, reason,
            total_rows, affected_rows, unmatched_rows=0,
            format_profile=None, example_before=None, example_after=None):
        """Log a single cleaning transformation with verified counts.

        Args:
            dataset: Name of dataset (e.g. 'DataScience Jobs')
            column: Column name transformed
            transformation: What was done (e.g. 'parse_lakhs_to_float')
            reason: Why (e.g. 'Salary stored as "7.8L" text, needs numeric')
            total_rows: Total rows in column
            affected_rows: Rows that were actually changed
            unmatched_rows: Rows that could not be parsed
            format_profile: Dict of {format: count} from profiling
            example_before: Raw sample value before
            example_after: Parsed sample value after
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "dataset": dataset,
            "column": column,
            "transformation": transformation,
            "reason": reason,
            "total_rows": int(total_rows),
            "affected_rows": int(affected_rows),
            "unmatched_rows": int(unmatched_rows),
            "success_rate": round(affected_rows / total_rows * 100, 1) if total_rows > 0 else 0,
        }
        if format_profile:
            entry["format_profile"] = format_profile
        if example_before is not None:
            entry["example_before"] = str(example_before)
        if example_after is not None:
            entry["example_after"] = str(example_after)

        self.entries.append(entry)
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def summary(self):
        """Print a summary of all transformations."""
        print(f"\n{'='*70}")
        print(f"CLEANING LEDGER SUMMARY ({len(self.entries)} transformations)")
        print(f"{'='*70}")
        print(f"{'Dataset':<20} {'Column':<20} {'Affected':>8} {'Total':>8} {'Rate':>6}")
        print(f"{'-'*70}")
        for e in self.entries:
            print(f"{e['dataset']:<20} {e['column']:<20} "
                  f"{e['affected_rows']:>8} {e['total_rows']:>8} "
                  f"{e['success_rate']:>5.1f}%")
