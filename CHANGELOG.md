# Changelog

## [1.4.0] - Unreleased

### Added

- IPv6 configuration in the example FRR config.
- Full solution diagram.
- Minimal HTTP API.

## [1.3.0] - 2025-05-08

### Added

- Support for specifying neighbor port number.

## [1.2.3] - 2025-04-28

### Fixed

- Fix scheduled rebuilds.

## [1.2.2] - 2025-04-18

### Changed

- Relax base image version to MAJOR.MINOR.
- Specify `dotenv` version artifact as string to improve compatibility with
  `gitlab-ci-local`.

## [1.2.1] - 2025-04-17

### Fixed

- Add missing `SOURCE_DATE_EPOCH` image build arg.

## [1.2.0] - 2025-04-16

### Changed

- Move packages into `src/`.
- Enable stricter Ruff checks.

## [1.1.2] - 2025-04-16

### Changed

- Only run pipelines for MRs on push.

## [1.1.1] - 2025-04-16

### Fixed

- Fix image build args.

## [1.1.0] - 2025-04-15

### Changed

- Refactor CI.

## [1.0.0] - 2025-03-30

### Added

- Initial implementation.
