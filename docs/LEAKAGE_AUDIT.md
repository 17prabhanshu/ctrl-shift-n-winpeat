# Leakage Audit

## Overview
This document outlines the potential sources of data leakage across the processing pipeline.

## Rule
DO NOT join datasets that share no individual-level identifier.

## Checks Performed
- Validated that `DataScience Jobs` and `Analytics Jobs` are treated as independent distributions, as they have no shared primary keys.
- Confirmed no overlapping feature generation that would leak target variables.
