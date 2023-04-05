# Previous Detections Step

## Description

Parses the `extra_fields` of the incoming detections to retrieve the binary field `prv_candidates` if the alert comes from ZTF. Otherwise, it does nothing.
This step returns a list with the processed objects, including their `aid`, previous candidates, detections without the `extra_fields` field and their non_detections.

#### Previous step:

- [Sorting Hat](https://github.com/alercebroker/sorting_hat_step)

#### Next steps:

- [Lightcurve Step](https://github.com/alercebroker/lightcurve-step)

## Database interactions

 - Writes into the non_detection collection (via Scribe)

## Code architecture

The step calls all the logic from the **core** folder, which contains all the main logic of the step.
