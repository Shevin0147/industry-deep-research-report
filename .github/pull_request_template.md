## Decision problem

What research decision or failure mode does this change address?

## Evidence and implementation

Describe the evidence rule, source boundary, industry-pack change, validator behavior, or documentation improvement.

## Compatibility

- [ ] The 10-section report format is unchanged.
- [ ] Existing export interfaces remain compatible.
- [ ] Schema 1.0 compatibility is preserved or the migration is documented.
- [ ] Validator changes use the Python standard library only.

## Validation

- [ ] `python -m unittest discover -s tests -v`
- [ ] Industry-pack JSON files parse successfully.
- [ ] No credentials, private `.research/` archives, or generated reports are included.
