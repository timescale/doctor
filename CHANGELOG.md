# Changelog

## [0.2.0](https://github.com/timescale/doctor/compare/v0.1.1...v0.2.0) (2023-11-02)


### Features

* add options to list rules ([8e8a6b1](https://github.com/timescale/doctor/commit/8e8a6b130e0b7c5ee515d711b1ff58d3a4730e8a)), closes [#37](https://github.com/timescale/doctor/issues/37)
* add rule dependencies ([#31](https://github.com/timescale/doctor/issues/31)) ([e9411ae](https://github.com/timescale/doctor/commit/e9411aeb3b65fab29e4e428298f8710c7bbf094e))
* add unit tests ([4c9e843](https://github.com/timescale/doctor/commit/4c9e84366b537cde230241a15b702ac8a4a14168))


### Bug Fixes

* only check permission for existing chunks ([1e5362d](https://github.com/timescale/doctor/commit/1e5362d390298f9ca7c48172c3ee2789d9944b0a)), closes [#26](https://github.com/timescale/doctor/issues/26)

## [0.1.1](https://github.com/timescale/doctor/compare/v0.1.0...v0.1.1) (2023-09-21)


### Bug Fixes

* use getpass.getuser() instead of os.getlogin() ([978cb9a](https://github.com/timescale/doctor/commit/978cb9a7ee500f36c81c1b8d0161af0835824444))


### Miscellaneous

* fix version bump in release-please ([c62419d](https://github.com/timescale/doctor/commit/c62419dfba165f01ac62fcf8b772b1eef2a7c479))

## 0.1.0 (2023-09-21)


### Features

* add rule to check index usage ([efa8f78](https://github.com/timescale/doctor/commit/efa8f783c02d83039cb46f543eb89b100a8f3485))
* add rule to check pointless segment-by column ([1f3c259](https://github.com/timescale/doctor/commit/1f3c259d939f1a55e2a10bde85fc17add359b40d))
* add rule to detect bad segmentby column ([351ea7c](https://github.com/timescale/doctor/commit/351ea7c04743034d7015614e8a307e6ef246430a))
* add rule to report on bad chunk permissions ([e428c14](https://github.com/timescale/doctor/commit/e428c14ff5c67dd5dca8ba12d9e4b116232ddada)), closes [#3](https://github.com/timescale/doctor/issues/3)


### Bug Fixes

* use parent table stats for segmentby ([f7a117e](https://github.com/timescale/doctor/commit/f7a117ec3e79df4337cf96e650cc61b06903b36a))


### Miscellaneous

* use release-please and publish to pypi ([b68e516](https://github.com/timescale/doctor/commit/b68e516889b23c7cbfba0aa462c1d412d99591cf))
