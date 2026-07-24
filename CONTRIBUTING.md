# Contributing

Thank you for helping improve Industry Deep Research Report.

## Good contributions

- Add or refine an industry evidence pack.
- Improve source-use boundaries or prohibited inferences.
- Add a reproducible validator failure case.
- Fix report validation or PDF export defects.
- Improve concise installation and usage documentation.

## Before opening a pull request

1. Keep the 10-section report format and existing export interfaces compatible.
2. Keep validator changes within the Python standard library.
3. Do not commit real `.research/` archives, generated reports, credentials, or personal data.
4. Run `python industry-deep-research-report/scripts/validate_report.py --help`.
5. Parse every JSON file in `references/industry-packs/`.
6. Explain the decision problem, evidence rule, and compatibility impact.

## Adding an industry pack

Use an existing JSON pack as the schema reference. Include required claim types, source combinations, operating metrics, scope traps, prohibited inferences, query groups, and L1-L4 thresholds.

One report may load only one primary and one secondary pack. Conflicting requirements must resolve to the stricter rule.

## Security

Do not disclose credentials, private research archives, or sensitive source data in a public issue. Contact the maintainer privately through GitHub when disclosure could harm users.
