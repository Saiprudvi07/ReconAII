ReconAI — Reconciliation Control Brief
1. Who

The Finance Operations or Reconciliation Analyst is responsible for running the reconciliation process. The Finance Controller or an authorized reviewer investigates exceptions and approves the final reconciliation report.

2. What

ReconAI compares two input sources:

ledger.csv: internal accounting ledger transactions.
settlement.csv: transactions reported by the payment processor or settlement provider.

The process validates input data, calculates control totals, detects duplicate and missing transactions, and identifies amount or date differences.

3. When

The reconciliation runs after both input files have been received and their reporting periods have been confirmed. It can be executed manually in the initial version and scheduled after testing and approval.

4. Where

The project runs locally using Python in Visual Studio Code. Input files are stored in the data/ directory, matching and validation logic is stored in src/, and reports are saved in the project directory.

5. Why

Reconciliation helps establish completeness and accuracy between internal ledger records and external settlement records. Exceptions may indicate missing transactions, duplicate processing, incorrect amounts, invalid data, or timing differences. Exceptions must be investigated rather than silently ignored.

6. How

Python validates each row, calculates control totals, indexes records using dictionaries, detects duplicates using sets, and applies deterministic matching rules.

The Python matcher—not AI—decides match status. A transaction is matched only when its defined reference, currency, date-window, and amount-tolerance rules pass. Unresolved records are reported as exceptions.

The analyst reviews the output, investigates exceptions, and documents corrections. The authorized Finance Controller or reviewer approves the final report. The program does not approve transactions or post accounting adjustments automatically.

Matching and control rules
Reference and currency must identify a candidate transaction.
The absolute date difference must be within 3 calendar days.
The absolute amount difference must not exceed 0.01 in the transaction currency.
Required-field failures and duplicate records are exceptions.
Control totals must be reviewed before the reconciliation is approved.
Outputs
schema_manifest.json
validation_results.json
control_total_report.json
Matching and exception results
Scope and limitations

This is a local learning prototype using CSV files. Production use would require access controls, audit logging, secure file handling, formal approval evidence, and additional testing.